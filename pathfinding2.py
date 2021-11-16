import math
import servo_handler
import ultrasonic_sensors

THRESHOLD_DISTANCE = 0.1

indicator = 0  # stores 0 or 1 to indicate of moving straight is an option

servo = servo_handler.ServoHandler
ultra = ultrasonic_sensors.UltrasonicHandler


def left_turn():
    indicator = 1
    servo.rotate(270)


def right_turn():
    indicator = 1
    # if distance from the front and left are small
    servo.rotate(90)


def move_straight():
    while(indicator == 0):
        servo.move(1)

    if indicator == 1:


def object_in_path():
    # if we're travaeling in a atraight line, but we see a thing
    # turn 90
    servo.rotate(90)
    revs = 0  # store the number of revoultions we went forward
    # go straight by 3 revs
