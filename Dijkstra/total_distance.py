
import math
class robot:
    def __init__(self, rpm, radius):
        self.rpm = rpm
        self.distance_traveled = 0
        self.radius = radius




def cal_total(robot, t): # input: an object robot, the time in second; output: distance in meters;
    rps = robot.rpm / float(60)
    distance = rps * robot.radius * 2 * math.pi * t
    return distance


