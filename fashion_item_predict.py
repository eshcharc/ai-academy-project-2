import os
from flask import Flask, flash, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from keras.models import load_model
from keras.utils import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import preprocess_input
import numpy as np
from class_names import class_names

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

model = load_model('./fashion_mnist.hd5', compile=False)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image):
    image = img_to_array(image)
    image = np.array([image])
    image = preprocess_input(image, mode='tf')
    return image

def predict_class(image):
    yhat = model.predict(image)
    percentage = max(yhat[0])
    predict_index = np.argmax(yhat[0])
    prediction = class_names[predict_index]
    percentage = '%.2f%%' % (percentage*100)
    return prediction, percentage

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if(not os.path.exists(UPLOAD_FOLDER)):
    os. makedirs(UPLOAD_FOLDER)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            image = load_img(file_path, target_size=(28, 28), color_mode='grayscale')
            image = preprocess_image(image)
            prediction, percentage = predict_class(image)
            return f'''
            <!doctype html>
            <html>
                <head>
                    <title>Fashion Item Prediction</title>
                    <link rel="icon" type="image/ico" href="static/icon.ico">
                    <style>
                        .wrapper {{
                            position: absolute;
                            top: 0;
                            bottom: 0;
                            left: 0;
                            right: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                        }}
                        .panel {{
                            border-radius: 10px;
                            padding: 20px;
                            background-color: #ffc30033;
                            box-shadow: 1px 1px 7px #9e9e9e;
                            user-select: none;
                        }}
                        .back_btn {{
                            color: white;
                            text-decoration: none;
                            font-weight: bold;
                            border: 1px solid grey;
                            border-radius: 3px;
                            padding: 3px 5px;
                            background-color: #888;
                            box-shadow: 4px 2px 7px #482e2e;
                        }}

                        .pred {{
                            font-weight: bold;
                        }}
                    </style>
                </head>
                <body>
                    <div class="wrapper">
                        <div class="panel">
                            <div>
                                <span>My prediction is: <span class="pred">{prediction}</span></span>&nbsp<span>(with {percentage} precision)</span>
                            </div>
                            <div style="margin-top: 20px;">
                                <a href="/" class="back_btn">Try Again</a>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
            '''

    return f'''
    <!doctype html>
    <html>
        <head>
            <title>Predict Fashion Item</title>
            <link rel="icon" type="image/ico" href="static/icon.ico">
            <style>
                .wrapper {{
                    position: absolute;
                    top: 0;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}

                .panel {{
                    border-radius: 10px;
                    padding: 20px;
                    background-color: #ffc30033;
                    box-shadow: 1px 1px 7px #9e9e9e;
                }}

                h1 {{
                    margin: 0 0 20px 0;
                    color: #bb2020;
                }}
            </style>
        </head>
        <body class="wrapper">
            <div class="panel">
                <h1>Upload New Picture</h1>
                <form method=post enctype=multipart/form-data>
                    <input type=file name=file accept=".png, .jpg, .jpeg, .gif">
                    <input type=submit value=Upload>
                </form>
            </div>
        </body>
    </html>
    '''

app.run(host='0.0.0.0', debug=True)