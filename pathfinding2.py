import math
import servo_handler
import ultrasonic_sensors

THRESHOLD_DISTANCE = 20

indicator = 0  # stores 0 or 1 to indicate if moving straight is an option

servo = servo_handler.ServoHandler
ultra = ultrasonic_sensors.UltrasonicHandler
coordinates = []


def left_turn():
    servo.rotate(270)
    indicator = 0


def right_turn():
    # if distance from the front and left are small
    servo.rotate(90)
    indicator = 0


def move_straight():
    global indicator
    while(indicator == 0):
        servo.move_forever()
        if ultra.front <= THRESHOLD_DISTANCE:
            indicator = 1
            break

    if indicator == 1:
        servo.stop_move_forever()

        # moving right
        if ultra.left <= THRESHOLD_DISTANCE and ultra.right > THRESHOLD_DISTANCE*2:
            right_turn()
            move_straight()

        # moving right
        elif ultra.right <= THRESHOLD_DISTANCE and ultra.left > THRESHOLD_DISTANCE*2:
            left_turn()
            move_straight()

        elif ultra.right > (THRESHOLD_DISTANCE)*2 and ultra.left <= (THRESHOLD_DISTANCE)*2:
            coordinates.append([servo.pos, 90])
            right_turn()
            indicator = 0
            move_straight()


'''def object_in_path():
    # if we're travaeling in a atraight line, but we see a thing
    # turn 90
    servo.rotate(90)
    revs = 0  # store the number of revoultions we went forward
    # go straight by 3 revs
'''
