import ultra_refresh
import time

sensors = ultra_refresh.UltrasonicHandler([38, 40], [37, 35], [29, 31])
sensors.start_measuring()

try:
    while True:
        print("Front: "+str(sensors.front)[:4]+" | Left: "+str(sensors.left)[:4]+"| Right: "+str(sensors.right)[:4])
        #print("Front: "+str(sensors.front)[:4]+" | Right: "+str(sensors.right)[:4]+"| Left: "+str(sensors.left)[:4])
        time.sleep(0.4)
except KeyboardInterrupt:
    print("Exiting..... abruptly")