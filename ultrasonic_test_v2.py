import ultrasonic_sensors
import time

sensors = ultrasonic_sensors.UltrasonicHandler([38, 40], [37, 35], [29, 31])
sensors.start_measuring()

try:
    while True:
        print("Front: "+str(sensors.front)[:4]+" | Left: "+str(sensors.left)[:4])
        time.sleep(0.4)
except KeyboardInterrupt:
    print("Exiting..... abruptly")