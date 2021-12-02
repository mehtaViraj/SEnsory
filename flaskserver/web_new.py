import os
from flask import Flask, flash, request, redirect, jsonify, send_file
from movement.delete_file import del_file
import movement.audio_predict as voice_recognition
import movement.pathfinding_test_2 as pf
import threading
import time

app = Flask(__name__)

voice_predicter = voice_recognition.VoiceRecognition()

app.secret_key = os.urandom(12).hex()
#app.debug = True
#app.config['UPLOAD_FOLDER'] = 'C:\Waterloo\1A\SEnsory\SEnsory\oop\inner\\'
#app.config["CLIENT_IMAGES"] = 'C:\Waterloo\1A\SEnsory\SEnsory\colour_detection\saved_images'

voice_folder = r'/home/pi/sensory/SEnsory/oop/inner'
del_file(voice_folder)

isMoving = False

@app.route('/', methods=['GET'])
def index():
    return jsonify({'reply': 'Alive'})

@app.route('/movetest', methods=['GET'])
def move_test():
    seconds = int(request.args.get("sec"))
    movetest_mover(seconds)
    return jsonify({'reply': 'Success'})
###^^^^ above's movemement function
def movetest_mover(seconds):
    global isMoving
    isMoving = True
    mover = pf.Pathfinding()
    mover.test(seconds)
    mover.release_all()
    isMoving = False

@app.route('/audio', methods=['POST', 'GET'])
def upload_file():
    print("Reached /audio")
    #print(request)

    global isMoving

    # check if the post request has the file part

    if request.method == 'POST':
        #print(1)

        if isMoving:
            return jsonify({'result': 'fail: is already moving'})

        voice_folder = r'/home/pi/sensory/SEnsory/oop/inner'
        del_file(voice_folder)
        #print(2)
        if 'file' not in request.files:
            flash('No file part')
            print("No file")
            return redirect(request.url)

        '''for filename in os.listdir(voice_folder):
            file_path = os.path.join(voice_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except:
                print("Failed to delete audio files") '''

        file = request.files['file']
        print(file.filename)
        #print(3)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        '''if file.filename == '':
            flash('No selected file')
            return redirect(request.url) '''
        filename = file.filename
        savepath = r'/home/pi/sensory/SEnsory/oop/inner/' + filename
        file.save(savepath)
        #print(4)
        to_find = voice_predicter.predict()
        to_find = 'yellow'
        print("--->{}".format(to_find))

        response = {"result": "success","filename": filename, "colour": to_find}

        del_file(r'/home/pi/sensory/SEnsory/flaskserver/movement/saved_images')
        print(5)
        movement_thread = threading.Thread(target=movement_thread_handler, args=(to_find,))
        #movement_thread.setDaemon(True)
        movement_thread.start()

        del_file(r'/home/pi/sensory/SEnsory/flaskserver/movement/saved_images')

        print(response)
        return jsonify(response)
###^^^^ above's movemement thread
def movement_thread_handler(to_find):
    global isMoving
    isMoving = True
    mover = pf.Pathfinding()
    mover.move_straight(to_find)
    mover.release_servo()
    isMoving = False

@app.route('/images', methods=['POST', 'GET'])
def send_data():
    print("reached GET")

    img_list = os.listdir(
        r'/home/pi/sensory/SEnsory/flaskserver/movement/saved_images/')
    img_dict = {}

    img_dict["imgs"] = img_list

    robot_state = 1
    img_dict["state"] = robot_state

    if not isMoving:
        img_dict['imgs'] = []

    return_json = jsonify(img_dict)
    print(return_json)

    if request.method == 'GET':
        print(img_dict)
        return return_json


@app.route('/encoded', methods=['GET'])
def send_images():

    directory = r'/home/pi/sensory/SEnsory/flaskserver/movement/saved_images/'

    if request.method == 'GET':
        filename = request.args.get("image_name")

        return send_file(directory+filename)


if __name__ == '__main__':
    #pf.start('yellow')
    app.run(debug=True, port=8080, host='0.0.0.0')
    #print("!"*50)