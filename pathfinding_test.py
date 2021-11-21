import math
import servo_handler
import ultrasonic_sensors
import time
import colour_in_shape_filtered as cl

THRESHOLD_DISTANCE = 60

indicator = 0  # stores 0 or 1 to indicate if moving straight is an option

ultra = ultrasonic_sensors.UltrasonicHandler([38, 40], [37, 35], [29, 31])
ultra.start_measuring()
servo = servo_handler.ServoHandler(21, 23)
#cam = c_detect.colour.CameraHandler("192.168.148.82")
cam = cl.CameraHandler("192.168.148.236")

coordinates = []


def rotate_away(num):
    if num == 1:
        servo.rotate(15)  # turn left
    elif num == 0:
        servo.rotate(-15)  # turn right


def left_turn():
    servo.rotate(90)
    #indicator = 0


def right_turn():
    # if distance from the front and left are small
    servo.rotate(-90)
    #indicator = 0


def move_straight(isFound=False):
    #global indicator
    # time.sleep(1)
    servo.move_forever()

    #--------#
    colour = 'yellow'
    #--------#

    while(ultra.front > THRESHOLD_DISTANCE):
        #print("Front: "+str(ultra.front)[:6]+" | Left: "+str(ultra.left)[:6]+"| Right: "+str(ultra.right)[:6])
        found_objects = cam.find_obj(colour)
        # print(found_objects)
        if not isFound and (len(found_objects) != 0):
            # servo.stop_move_forever()
            servo.stop_move_forever()
            cam.save_picture()
            isFound = True
        if isFound and (len(found_objects) == 0):
            isFound = False

        time.sleep(0.4)

    print("Stopping")
    servo.stop_move_forever()

    # moving right
    if ultra.right <= 15:
        print("Too Close, turning left")
        rotate_away(1)

        ultra.front = ultra._update_distance(
            ultra.front_trigger, ultra.front_echo)
        move_straight(isFound)

    if ultra.left <= 15:
        print("Too Close, turning right")
        rotate_away(0)

        ultra.front = ultra._update_distance(
            ultra.front_trigger, ultra.front_echo)
        move_straight(isFound)

    if ultra.left <= THRESHOLD_DISTANCE and ultra.right > THRESHOLD_DISTANCE*2:
        print("Going right")
        right_turn()
        #indicator = 0
        ultra.front = ultra._update_distance(
            ultra.front_trigger, ultra.front_echo)
        move_straight(isFound)

    # moving left
    elif ultra.right <= THRESHOLD_DISTANCE and ultra.left > THRESHOLD_DISTANCE*2:
        print("Going left")
        left_turn()
        #indicator = 0
        ultra.front = ultra._update_distance(
            ultra.front_trigger, ultra.front_echo)
        move_straight(isFound)

    elif ultra.right > (THRESHOLD_DISTANCE)*2 and ultra.left > (THRESHOLD_DISTANCE)*2:
        print("Free space. Go right")
        coordinates.append([servo.pos, 90])
        right_turn()
        #indicator = 0
        ultra.front = ultra._update_distance(
            ultra.front_trigger, ultra.front_echo)
        move_straight(isFound)
    else:
        print("Free space. Go right")
        coordinates.append([servo.pos, 90])
        right_turn()
        #indicator = 0
        #ultra.front = ultra._update_distance(ultra.front_trigger, ultra.front_echo)
        move_straight(isFound)


'''def object_in_path():
    # if we're travaeling in a atraight line, but we see a thing
    # turn 90
    servo.rotate(90)
    revs = 0  # store the number of revoultions we went forward
    # go straight by 3 revs
'''

move_straight()
servo.release()

'''
while True:
    servo.rotate(90)
    print("Front: "+str(ultra.front)[:6]+" | Left: "+str(ultra.left)[:6]+"| Right: "+str(ultra.right)[:6])
'''
