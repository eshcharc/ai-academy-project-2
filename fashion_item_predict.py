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
            flash('No selected file')
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
            <title>Fashion Item Prediction</title>
            <div>
                <span>{prediction}</span><span>({percentage})</span>
            </div>
            '''

    return f'''
    <!doctype html>
    <title>Predict Fashion Item</title>
    <h1>Upload New Picture</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept=".png, .jpg, .jpeg, .gif">
      <input type=submit value=Upload>
    </form>
    '''

app.run(host='0.0.0.0', debug=True)