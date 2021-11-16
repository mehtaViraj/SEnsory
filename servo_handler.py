import time
import RPi.GPIO as GPIO
import math
import threading

class ServoHandler:
    def __init__(self, pin1, pin2):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin1,GPIO.OUT)
        GPIO.setup(pin2,GPIO.OUT)

        self.pos = (0,0)
        self.heading = 0

        self.pin1 = GPIO.PWM(pin1,50)
        self.pin2 = GPIO.PWM(pin2,50)
        self.pin1.start(0)
        self.pin2.start(0)

        self.thread = None
        self.isRunning = False
        self.isManualMoving = True

    def multithreader(self, func):
        def wrapper(*args, **kwargs):
            if self.isStarted or self.isManualMoving:
                print("Thread already running")
            else:
                self.thread = threading.Thread(target=func, args=(*args, *kwargs))
                self.thread.setDaemon(True)
                self.thread.start()
                #self.isRunning = True
        return wrapper


    def move(self, units, reverse=False):
        self.isManualMoving = True
        #CONSTANTS
        forward_cycle = 12.5
        backward_cycle = 0.6
        time_1_rev = 1.143
        #CONSTANTS

        if (not reverse):
            s1_cycle = forward_cycle
            s2_cycle = backward_cycle
        else:
            s2_cycle = forward_cycle
            s1_cycle = backward_cycle

        self.pin1.ChangeDutyCycle(s1_cycle)
        self.pin2.ChangeDutyCycle(s2_cycle)
        time.sleep(time_1_rev * units)
        self.pin1.ChangeDutyCycle(0)
        self.pin2.ChangeDutyCycle(0)
        time.sleep(0.2)

        self.pos = ( self.pos[0] +  units*math.cos(math.radians(self.heading)) , self.pos[1] +  units*math.sin(math.radians(self.heading)) )
        print(" - New Position: {}, {}".format(self.pos[0], self.pos[1]))

        self.isManualMoving = False
    
    def rotate(self, theta):
        self.isManualMoving = True
        #CONSTANTS
        forward_cycle = 12.5
        backward_cycle = 0.6
        time_rot_90 = 1.125
        time_rot_180 = 1.1575
        time_rot_270 = 1.17
        time_rot_360 = 1.4
        #time_rot_45 = time_rot_90/2
        #CONSTANTS

        if theta % 90 != 0:
            if theta > 90:
                print("CAN ONLY ROTATE IN 90 DEGREE STEPS")
                return None
            else:
                pass

        cycle = backward_cycle if theta < 0 else forward_cycle
        abs_theta = abs(theta)
        if abs_theta <=90:
            time_rot = time_rot_90
        elif abs_theta <=180:
            time_rot = time_rot_180
        elif abs_theta <=270:
            time_rot = time_rot_270
        else:
            time_rot = time_rot_360

        time_rot_theta = (abs_theta/90) * time_rot
        self.pin1.ChangeDutyCycle(cycle)
        self.pin2.ChangeDutyCycle(cycle)
        time.sleep(time_rot_theta)
        self.pin1.ChangeDutyCycle(0)
        self.pin2.ChangeDutyCycle(0)
        time.sleep(0.4)

        self.heading = (self.heading + theta) % 360
        print(" - New Heading: {}".format(self.heading))

        self.isManualMoving = False

    def set_heading(self, newheading):
        self.isRunning = True
        theta = newheading -  self.heading
        self.rotate(theta)
        print(" - (Rotated {})".format(theta))
        self.isRunning = False

    def set_position_rect(self, newpos):
        self.isRunning = True

        x_travel = newpos[0] - self.pos[0]
        x_dir = 0 if x_travel >= 0 else 180

        y_travel = newpos[1] - self.pos[1]
        y_dir = 90 if y_travel >= 0 else -90

        print("Heading {} Move {}".format(x_dir, abs(x_travel)))
        self.set_heading(x_dir)
        self.move(abs(x_travel))

        print("Heading {} Move {}".format(y_dir, abs(y_travel)))
        self.set_heading(y_dir)
        self.move(abs(y_travel))

        self.isRunning = False

    def release(self):
        self.pin1.stop()
        self.pin1.stop()

#MAIN

servo = ServoHandler(21, 23)

# servo.move(2)
# servo.rotate(-90)
# servo.move(2)
# servo.rotate(-90)
# servo.move(1)
# servo.rotate(0)
# servo.move(1)
# servo.rotate(-90)
# servo.move(2)

servo.set_position_rect((2,2))
# servo.set_position_rect((2,1))
servo.set_position_rect((0,0))

# servo.rotate(90)
# servo.rotate(-90)

#servo.rotate(180)
#servo.rotate(-180)

#servo.rotate(270)
#servo.rotate(-270)

servo.release()