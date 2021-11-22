import os
from flask import Flask, flash, request, redirect, url_for, jsonify, send_file
from os import listdir
from os.path import isfile, join
from delete_file import del_file
import movement.pathfinding_test as pathfinding_test

app = Flask(__name__)


app.secret_key = os.urandom(12).hex()
#app.config['UPLOAD_FOLDER'] = 'C:\Waterloo\1A\SEnsory\SEnsory\oop\inner\\'
#app.config["CLIENT_IMAGES"] = 'C:\Waterloo\1A\SEnsory\SEnsory\colour_detection\saved_images'

voice_folder = r'/home/pi/sensory/SEnsory/oop/inner'
del_file(voice_folder)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'reply': 'Alive'})


@app.route('/audio', methods=['POST', 'GET'])
def upload_file():
    print("Reached /post")
    print(request)

    # check if the post request has the file part

    if request.method == 'POST':

        voice_folder = r'/home/pi/sensory/SEnsory/oop/inner'
        del_file(voice_folder)

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

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        '''if file.filename == '':
            flash('No selected file')
            return redirect(request.url) '''
        filename = file.filename
        savepath = r'/home/pi/sensory/SEnsory/oop/inner/' + filename
        file.save(savepath)
        response = {"result": "success", "filename": filename}

        del_file(r'/home/pi/sensory/SEnsory/flaskserver/movement/saved_images')

        pathfinding_test.move_straight("yellow", isFound=False)

        return response


@app.route('/images', methods=['POST', 'GET'])
def send_data():
    print("reached GET")

    img_list = os.listdir(
        r'/home/pi/sensory/SEnsory/flaskserver/movement/saved_images/')
    img_dict = {}

    img_dict["imgs"] = img_list

    robot_state = 0
    img_dict["state"] = robot_state
    return_json = jsonify(img_dict)
    print(return_json)

    if request.method == 'GET':
        return return_json


@app.route('/encoded', methods=['GET'])
def send_images():

    directory = r'/home/pi/sensory/SEnsory/flaskserver/movement/saved_images/'

    if request.method == 'GET':
        filename = request.args.get("image_name")

        return send_file(directory+filename)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
