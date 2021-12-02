import movement.colour.colour_in_shape_filtered as c 
import time

cam = c.CameraHandler("192.168.179.82")
time.sleep(1)

try:
    while True:
        objects_found = cam.find_obj("yellow")
        if len(objects_found) == 0:
            print("Not Found")
        else:
            print(objects_found)
except KeyboardInterrupt:
    cam.release()