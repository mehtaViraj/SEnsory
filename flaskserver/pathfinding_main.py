from movement.servo_handler import ServoHandler
import movement.pathfinding_test_2 as p
import threading
from multiprocessing import Process
from flask import *
import os

# p.move_straight("yellow")

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()

isMoving = False

#mover = p.Pathfinding()
#moverRaw = ServoHandler(21,23)
#print(mover)

def thread_controller(sec, cycle):
    global isMoving
    isMoving = True
    mover = p.Pathfinding()
    mover.test(sec, cycle)
    mover.release_servo()
    isMoving = False

def thread_controllercalib(sec):
    global isMoving
    isMoving = True
    mover = p.Pathfinding()
    mover.calibrate(sec)
    mover.release_servo()
    isMoving = False

@app.route('/', methods=['GET'])
def index():
    return jsonify({'reply': 'Alive'})

@app.route('/movetest', methods=['GET'])
def start(sec=None, cycle=None):
    if sec==None:
        sec = int(request.args.get("sec"))
        fcycle = float(request.args.get("fcycle"))
        bcycle = float(request.args.get("bcycle"))
    #to_find = 'yellow'
    movement_thread = Process(target=thread_controller, args=(sec, (fcycle, bcycle)))
    # movement_thread.setDaemon(True)
    movement_thread.start()

    return jsonify({'reply': 'Success'})

@app.route('/calibrate', methods=['GET'])
def calibrate(sec=None):
    if sec==None:
        sec = int(request.args.get("sec"))
    #to_find = 'yellow'
    #movement_thread = Process(target=thread_controllercalib, args=(sec,))
    # movement_thread.setDaemon(True)
    thread_controllercalib(sec)
    #movement_thread.start()

    return jsonify({'reply': 'Success'})

@app.route('/raw', methods=['GET'])
def raw(sec=None):
    if sec==None:
        sec = int(request.args.get("sec"))
    #moverRaw = ServoHandler(21,23)
    moverRaw.calibrate_loop(10)
    #moverRaw.release()

#calibrate(10)
app.run(debug=True, port=8080, host='0.0.0.0')