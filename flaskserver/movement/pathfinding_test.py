from delete_file import del_file
import movement.servo_handler as servo_handler
import movement.ultrasonic_sensors as ultrasonic_sensors
import time
import colour.colour_in_shape_filtered as cl

THRESHOLD_DISTANCE = 40

indicator = 0  # stores 0 or 1 to indicate if moving straight is an option

ultra = ultrasonic_sensors.UltrasonicHandler([38, 40], [37, 35], [29, 31])
ultra.start_measuring()
servo = servo_handler.ServoHandler(21, 23)
#cam = c_detect.colour.CameraHandler("192.168.148.82")
cam = cl.CameraHandler("192.168.62.236")


coordinates = []


def rotate_away(num):
    if num == 1:
        servo.rotate(5)  # turn left
    elif num == 0:
        servo.rotate(5)  # turn right


def left_turn():
    servo.rotate(90)
    #indicator = 0


def right_turn():
    # if distance from the front and left are small
    servo.rotate(-90)
    #indicator = 0


def move_straight(colour, robot_state=1, isFound=False):
    #global indicator
    # time.sleep(1)
    colour = "yellow"

    while robot_state == 1:

        servo.move_forever()

        while(ultra.front > THRESHOLD_DISTANCE):
            #print("Front: "+str(ultra.front)[:6]+" | Left: "+str(ultra.left)[:6]+"| Right: "+str(ultra.right)[:6])
            found_objects = cam.find_obj(colour)
            # print(found_objects)
            if not isFound and (len(found_objects) != 0):
                # servo.stop_move_forever()

                del_file(
                    r'/home/pi/sensory/SEnsory/flaskserver/movement/saved_images')
                servo.stop_move_forever()
                cam.save_picture()
                isFound = True
                robot_state = 0
                move_straight(colour, 0, isFound)
            if isFound and (len(found_objects) == 0):
                isFound = False

            time.sleep(0.4)

        # moving right

        time_taken = 1
        time_count = 0

        if ultra.right <= 15:
            init_dist = ultra.right
            final_dist = 0
            while(final_dist - init_dist >= 0):
                time_start = time.time()
                rotate_away(1)
                if time.time() - time_start == 0.1:
                    init_dist = final_dist
                    final_dist = ultra.right

        if ultra.left <= 15:
            init_dist = ultra.left
            final_dist = 0
            while(final_dist - init_dist >= 0):
                time_start = time.time()
                rotate_away(0)
                if time.time() - time_start == 0.1:
                    init_dist = final_dist
                    final_dist = ultra.right

        if ultra.left <= THRESHOLD_DISTANCE and ultra.right > THRESHOLD_DISTANCE*2:
            print("Going right")
            right_turn()
            #indicator = 0
            ultra.front = ultra._update_distance(
                ultra.front_trigger, ultra.front_echo)
            move_straight(colour, 1, isFound)

        # moving left
        elif ultra.right <= THRESHOLD_DISTANCE and ultra.left > THRESHOLD_DISTANCE*2:
            print("Going left")
            left_turn()
            #indicator = 0
            ultra.front = ultra._update_distance(
                ultra.front_trigger, ultra.front_echo)
            move_straight(colour, 1, isFound)

        elif ultra.right > (THRESHOLD_DISTANCE)*2 and ultra.left > (THRESHOLD_DISTANCE)*2:
            print("Free space. Go right")
            coordinates.append([servo.pos, 90])
            print(coordinates)
            right_turn()
            #indicator = 0
            ultra.front = ultra._update_distance(
                ultra.front_trigger, ultra.front_echo)
            move_straight(colour, 1, isFound)
        else:
            print("Free space. Go right")
            coordinates.append([servo.pos, 90])

            right_turn()
            #indicator = 0
            #ultra.front = ultra._update_distance(ultra.front_trigger, ultra.front_echo)
            move_straight(colour, 1, isFound)

    while robot_state == 0:
        servo.stop_move_forever
