import movement.servo_handler as servo_handler
import movement.ultrasonic_sensors as ultrasonic_sensors
import time
import movement.colour.colour_in_shape_filtered as cl

THRESHOLD_DISTANCE = 35

indicator = 0  # stores 0 or 1 to indicate if moving straight is an option

ultra = ultrasonic_sensors.UltrasonicHandler([38, 40], [37, 35], [29, 31])
#ultra.start_measuring()
servo = servo_handler.ServoHandler(21, 23)
#cam = c_detect.colour.CameraHandler("192.168.148.82")
cam = cl.CameraHandler("192.168.179.236")

colour = "yellow"


coordinates = []
moves = []
indexes = []


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


def check_coordinates(coordinates, turn_indicator):

    print("Reached Check Coordinates")

    if len(coordinates) < 3:
        print("Initial Condition")
        servo.stop_move_forever()
        right_turn()
        moves.append("right")
        ultra.front = ultra._update_distance(
            ultra.front_trigger, ultra.front_echo)
        move_straight(colour)

    for i in range(len(coordinates)):
        coord_count = 0
        for j in range(len(coordinates)):
            # check the list for duplicate x co-ordinates
            if turn_indicator == 1:
                print("Moving in x axis")
                if coordinates[i][1][0] == coordinates[j][1][0]:
                    coord_count += 1

            # check the list for duplicate y co-ordinates
            if turn_indicator == 2:
                print("Moving in y axis")
                if coordinates[i][1][1] == coordinates[j][1][1]:
                    coord_count += 1

        if coord_count > 1:
            print("Found out bad direction")
            cur_coord = servo.pos
            servo.stop_move_forever()
            if cur_coord[0]-servo.pos[0] > 0:
                servo.rotate(-90)
                moves.append("right")

                ultra.front = ultra._update_distance(
                    ultra.front_trigger, ultra.front_echo)
                move_straight(colour)
            else:
                servo.rotate(90)
                ultra.front = ultra._update_distance(
                    ultra.front_trigger, ultra.front_echo)
                move_straight(colour)

        else:
            right_turn()
            moves.append("right")

        indexes.append(len(moves)-1)


def retrace(indexes):
    desired_index = indexes[-1]
    number_of_moves = (len(moves)-1)-desired_index

    servo.move_forever()
    for i in range(number_of_moves):

        if moves[len(moves)-i-1] == "right" and ultra.front < THRESHOLD_DISTANCE and ultra.right < THRESHOLD_DISTANCE:
            servo.stop_move_forever()
            left_turn()
            if i == number_of_moves-1:
                servo.stop_move_forever()
            else:
                servo.move_forever()
        elif moves[len(moves)-i-1] == "right" and ultra.front < THRESHOLD_DISTANCE and ultra.right < THRESHOLD_DISTANCE:
            servo.stop_move_forever()
            right_turn()
            if i == number_of_moves-1:
                servo.stop_move_forever()
            else:
                servo.move_forever()


def move_straight(colour, robot_state=1, isFound=False):
    #global indicator
    # time.sleep(1)

    servo.move_forever()

    turn_counter = 0

    while(ultra.front > THRESHOLD_DISTANCE):
        print("Front: "+str(ultra.front)
              [:6]+" | Left: "+str(ultra.left)[:6]+"| Right: "+str(ultra.right)[:6]+"  -  NEW")
        found_objects = cam.find_obj(colour)
        # print(found_objects)
        if not isFound and (len(found_objects) != 0):
            # servo.stop_move_forever()

            # del_file(r'/home/pi/sensory/SEnsory/flaskserver/movement/saved_images')
            # servo.stop_move_forever()
            cam.save_picture()
            isFound = True
            robot_state = 0
            #move_straight(colour, 0, isFound)
        if isFound and (len(found_objects) == 0):
            isFound = False

        time.sleep(0.4)

    # moving right
    '''
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
                final_dist = ultra.right'''

    if ultra.left <= THRESHOLD_DISTANCE and ultra.right > THRESHOLD_DISTANCE:
        print("Going right")
        servo.stop_move_forever()
        right_turn()
        moves.append("right")
        #indicator = 0
        ultra.front = ultra._update_distance(
            ultra.front_trigger, ultra.front_echo)
        move_straight(colour, isFound)

    # moving left
    elif ultra.right <= THRESHOLD_DISTANCE and ultra.left > THRESHOLD_DISTANCE:
        print("Going left")
        servo.stop_move_forever()
        left_turn()
        moves.append("left")
        print("Moves:")
        print(moves)
        #indicator = 0
        ultra.front = ultra._update_distance(
            ultra.front_trigger, ultra.front_echo)
        move_straight(colour, isFound)

    elif ultra.right > (THRESHOLD_DISTANCE) and ultra.left > (THRESHOLD_DISTANCE):
        '''print("Free space. Go right")
        coordinates.append([servo.pos, 90])
        print(coordinates)
        right_turn()
        #indicator = 0
        ultra.front = ultra._update_distance(
            ultra.front_trigger, ultra.front_echo)
        move_straight(colour, isFound)'''

        print("Free space. Take decision")
        # currently the y co-ordinate is changing
        if servo.heading % 180 == 0:
            # check the list for duplicate x co-ordinates
            check_coordinates(coordinates, 1)
        else:
            check_coordinates(coordinates, 2)

        coordinates.append([servo.pos, 90])
        print(coordinates)
        #indicator = 0
        ultra.front = ultra._update_distance(
            ultra.front_trigger, ultra.front_echo)
        move_straight(colour, isFound)

    elif ultra.right < THRESHOLD_DISTANCE and ultra.left < THRESHOLD_DISTANCE:
        print("Deadend. Retracing....")
        servo.stop_move_forever()
        servo.rotate(180)
        retrace(indexes)
        move_straight(colour, isFound)

    '''else:
        print("Free space. Go right")
        coordinates.append([servo.pos, 90])
        print(coordinates)

        right_turn()
        #indicator = 0
        #ultra.front = ultra._update_distance(ultra.front_trigger, ultra.front_echo)
        move_straight(colour, isFound)'''

    # while robot_state == 0:
    #     servo.stop_move_forever


if __name__ == '__main__':
    move_straight(colour, isFound=False)
