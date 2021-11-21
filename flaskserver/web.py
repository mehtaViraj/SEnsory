import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.wrappers import response


app = Flask(__name__)

app.secret_key = os.urandom(12).hex()
app.config['UPLOAD_FOLDER'] = 'C:\Waterloo\1A\SEnsory\SEnsory\oop'


@app.route('/', methods=['GET'])
def index():
    return 'Hello world'


@app.route('/post', methods=['POST', 'GET'])
def upload_file():
    print("Reached /post")
    print(request)

    # check if the post request has the file part
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            print("No file")
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        '''if file.filename == '':
            flash('No selected file')
            return redirect(request.url) '''
        filename = file.filename
        savepath = "C:\Waterloo\\1A\SEnsory\SEnsory\oop\\" + filename
        file.save(savepath)
        response = {"result": "success", "filename": filename}
        return response


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
