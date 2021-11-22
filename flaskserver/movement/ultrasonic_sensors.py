import RPi.GPIO as GPIO
import time
import threading

class UltrasonicHandler:
    def __init__(self, front_pins, left_pins, right_pins):  #Each dir_pins is a tuple of (triggerpin, echopin)
        #Save the pins
        self.front_trigger = front_pins[0]
        self.front_echo = front_pins[1]
        self.left_trigger = left_pins[0]
        self.left_echo = left_pins[1]
        self.right_trigger = right_pins[0]
        self.right_echo = right_pins[1]
        #Setup the pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.front_trigger, GPIO.OUT)
        GPIO.setup(self.front_echo, GPIO.IN)
        GPIO.setup(self.left_trigger, GPIO.OUT)
        GPIO.setup(self.left_echo, GPIO.IN)
        GPIO.setup(self.right_trigger, GPIO.OUT)
        GPIO.setup(self.right_echo, GPIO.IN)

        self.front = 500
        self.left = 500
        self.right = 500
        self.isStarted = False
        self.measurement_thread = None

        print("Front: {}, {} | Left: {}, {} | Right: {}, {}".format(self.front_trigger,self.front_echo,self.left_trigger,self.left_echo,self.right_trigger,self.right_echo))

    def _update_distance(self, trigger, echo):
        GPIO.output(trigger, GPIO.LOW)
        time.sleep(0.4) #Wait for sensor to settle

        # set Trigger to HIGH
        GPIO.output(trigger, GPIO.HIGH)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(trigger, GPIO.LOW)

        StartTimeOG = time.time()
        StartTime = time.time()
        StopTime = time.time()
        # save StartTime
        while GPIO.input(echo) == 0:
            StartTime = time.time()
            if time.time() - StartTimeOG > 1:
                return 500
        # save time of arrival
        while GPIO.input(echo) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        #print(distance)
        return distance
    
    def _thread_loop(self):
        while True:
            self.front = self._update_distance(self.front_trigger, self.front_echo)
            self.left =  self._update_distance(self.left_trigger, self.left_echo)
            self.right = self._update_distance(self.right_trigger, self.right_echo)
    
    def start_measuring(self):
        if self.isStarted:
            print("Thread already running")
        else:
            self.measurement_thread = threading.Thread(target=self._thread_loop)
            self.measurement_thread.setDaemon(True)
            self.measurement_thread.start()
            self.isStarted = True