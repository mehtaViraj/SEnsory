
import cv2
import numpy as np
from collections import OrderedDict


class ColorLabelerHSV:
    def __init__(self, colors):
        hsv_LS = np.zeros((len(colors), 1, 3), dtype="uint8")
        unsorted_hsvnames = []
        for (i, (name, hsv)) in enumerate(colors.items()):
            hsv_LS[i] = hsv
            unsorted_hsvnames.append(name)
        hsv_LS = cv2.cvtColor(hsv_LS, cv2.COLOR_RGB2HSV)

        # Convert to python list for simplicity, as we dont need the saturation and values
        unsorted_hue_LS = [hsv_LS[i][0][0]
                           for i in range(len(unsorted_hsvnames))]

        '''
		for i in range(len(unsorted_hsvnames)):
			print("{}: {}".format(unsorted_hsvnames[i], unsorted_hue_LS[i]))
		print("---------------------------")
		'''

        # SimpleSort. Very slow, but easy.
        hsvNames = []
        hue_LS = []
        for i in range(len(unsorted_hsvnames)):
            index = unsorted_hue_LS.index(min(unsorted_hue_LS))
            hue_LS.append(unsorted_hue_LS.pop(index))
            hsvNames.append(unsorted_hsvnames.pop(index))

        # Add colour entries so that it is circular
        hue_LS.append(hue_LS[0]+180)
        hsvNames.append(hsvNames[0])
        hue_LS.insert(0, (hue_LS[-2]-180))
        hsvNames.insert(0, hsvNames[-2])

        # Develop thresholds based on hues
        hue_thresholds = []
        for i in range(1, len(hsvNames)-1 - 1):
            lower_angle = (hue_LS[i]/2 + hue_LS[i-1]/2)
            upper_angle = (hue_LS[i]/2 + hue_LS[i+1]/2)
            hue_thresholds.append((lower_angle, upper_angle))

            '''
			if lower_angle >= upper_angle:
				print("--------------------------")
				print("WARN: ALGO FUCKED UP")
				print("{} -> Lower: {} , Upper: {}".format(hsvNames[i], lower_angle, upper_angle))
			else:
				print("--------------------------")
				print("{} -> Lower: {} , Upper: {}".format(hsvNames[i], lower_angle, upper_angle))\
			'''

        # Handle final colour
        lower_angle = (hue_LS[i]/2 + hue_LS[i-1]/2)
        upper_angle = (hue_LS[i]/2 + 180)
        hue_thresholds.append((lower_angle, upper_angle))

        # Remove the extra names
        del hsvNames[0]
        del hsvNames[-1]

        # Constrain within the hue ranges for accurate range size measurements
        corrupted_indexes = []
        for i in range(len(hsvNames)):
            if hue_thresholds[i][0] >= hue_thresholds[i][1]:
                corrupted_indexes.append(i)
                continue
            if hue_thresholds[i][0] < 0:
                hue_thresholds[i] = (0.0, hue_thresholds[i][1])
            if hue_thresholds[i][1] > 180:
                hue_thresholds[i] = (hue_thresholds[i][0], 180.0)

        index_correction = 0
        for i in corrupted_indexes:
            #print("{} -> {} for len {}".format(i, i - index_correction, len(hue_thresholds)))
            del hue_thresholds[i - index_correction]
            del hsvNames[i - index_correction]
            index_correction = index_correction + 1

        # Limit range width
        for i in range(len(hsvNames)):
            width = hue_thresholds[i][1] - hue_thresholds[i][0]
            max_width = 27
            if width > max_width:
                trim = (width - max_width)/2
                hue_mid = (hue_thresholds[i][0] + hue_thresholds[i][1])/2
                hue_thresholds[i] = (hue_mid - trim, hue_mid + trim)

        # Convert to Dict
        self.colour_ranges = {}
        for i in range(len(hsvNames)):
            self.colour_ranges[hsvNames[i]] = hue_thresholds[i]

        '''
		print("---------------------------")
		for i in range(len(hsvNames)):
			print("{}: {}".format(hsvNames[i], hue_thresholds[i]))
		'''

    def showHues(self):
        return self.colour_ranges

    def colourMasker(self, image, colour, s_lower=87, h_lower=111):
        lower = np.array([self.colour_ranges[colour][0],
                         s_lower, h_lower], np.uint8)
        upper = np.array([self.colour_ranges[colour][1], 255, 255], np.uint8)
        mask = cv2.inRange(image, lower, upper)

        kernal = np.ones((5, 5), "uint8")
        mask = cv2.dilate(mask, kernal)
        colour_only = cv2.bitwise_and(image, image, mask=mask)

        return colour_only

    '''
	def colourFinderOLD(self, image, c):

		mask = np.zeros(image.shape[:2], dtype="uint8")
		cv2.drawContours(mask, c, -1, 255, -1)
		mask = cv2.erode(mask, None, iterations=2)
		mean = cv2.mean(image, mask=mask)[:3]
		colour_index = None

		for i in range(len(hsvNames)):
			if int(mean[0]) <= int(hue_thresholds[i][1]):
				if int(mean[0]) > int(hue_thresholds[i][0]):
					colour_index = i
					break
			
			h_variance = abs(int(mean[0]) - int(self.hsv_LS[i][0][0]))
			if h_variance <= 30:
				minDist = (h_variance,i)
				break
			

		accurate = True

		if colour_index != None:
			returnLabel = hsvNames[colour_index]
		else:
			return("Not Found", False, (None, ))
		
		if (mean[1] < 30 and mean[2] < 30):
			returnLabel = "Black"
		if (mean[1] < 30 and mean[2] > 180):
			returnLabel = "White"
		
		
		def fn_circle(x, h, k, r, flip=False):
			flipVal = -1 if flip else 1
			return ((flipVal*math.sqrt((r*r)-((x-h)*(x-h)))) +k)
		try:
			#s_tolerance = (((mean[2]*(mean[2]-510))/255) +255)  # Quadratic equation to make the threshold more reasonable
			#s_tolerance = fn_circle(mean[2], 255, 255, 255, True)
			#s_tolerance = fn_circle(mean[2], -35, -35, 255, False)
			#s_tolerance = 255-mean[2]
			s_tolerance = 81
		except ValueError:
			s_tolerance = 300
			#print("! Domain Error excepted")
		
		if mean[1] < s_tolerance:
			accurate = False

		return(returnLabel, accurate, (mean, str(s_tolerance)[:5]))
	'''

#-------------------------------------------------------------------------------------------#
# Main test function
# Comment out when using module
#-------------------------------------------------------------------------------------------#

if __name__=='__main__':

    colors = OrderedDict({
        # "dark blue": (0, 0	, 255),
        # "red": (255, 0, 0),
        # "green": (0, 255, 0),
        "yellow": (255, 255, 0),
        "purple": (255, 0, 255),
        "cyan": (0, 255, 255),
    })
    cl_hsv = ColorLabelerHSV(colors)

    hueList = cl_hsv.showHues()

    for i in hueList:
        print(i, ': ', hueList[i])
