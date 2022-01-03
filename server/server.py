import imghdr
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template
import pickle
import os
import pandas as pd
from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
from PIL import Image
import numpy as np
import json
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(APP_ROOT, "./crop_rec_model.pickle")
LOCATION_PATH = os.path.join(APP_ROOT, "./location.csv")
CROP_MODEL_PATH = os.path.join(APP_ROOT,"./crop.h5")
CROP_WEIGHTS_PATH = os.path.join(APP_ROOT,"./crop_weights.h5")
UPLOAD_FOLDER_PATH = os.path.join(APP_ROOT,"./temp")

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

def prepare_image(img_file):
    img_file.save(os.path.join(APP_ROOT,"./temp", img_file.filename))

    img_path = UPLOAD_FOLDER_PATH + '/' + img_file.filename
    print(img_path)
    img = image.load_img(img_path, target_size=(256, 256))
    x = image.img_to_array(img)
    x = x/255
    return tf.expand_dims(x, axis=0)

@app.route('/')
def hello():
    return render_template('app.html')


@app.route('/get_crop_info', methods=['GET', 'POST'])
def crop():
    model = pickle.load(open(MODEL_PATH, 'rb'))
    predictions = model.predict([[request.args.get("nitrogen"), request.args.get("phosphorus"), request.args.get(
        "potassium"), request.args.get("temprature"), request.args.get("humidity"), request.args.get("PH"), request.args.get("rainfall")]])
    Response = jsonify({"prediction": predictions[0]})
    Response.headers.add('Access-Control-Allow-Origin', '*')
    return Response


@app.route('/location', methods=['GET', 'POST'])
def location():

    location_df = pd.read_csv(LOCATION_PATH)
    State_Name = request.args.get("state")
    District_Name = request.args.get("district")
    print([State_Name,District_Name])
    print(location_df.head())
    crop = location_df[(location_df["State_Name"] ==
                        State_Name) & (location_df["District_Name"] == District_Name.upper())]["Crop"]
    crop = crop.reset_index(drop=True)
    if(crop.size == 0):
        Response = jsonify({"prediction": "state or district does not exist"})
        Response.headers.add('Access-Control-Allow-Origin', '*')

        return Response
    Response = jsonify({"prediction": str(crop[0])})
    Response.headers.add('Access-Control-Allow-Origin', '*')

    return Response

@app.route('/disease', methods=['POST'])
def disease_prediction():
    allowed_extensions = ['.jpg', '.png', '.gif','.jpeg']
    
    if 'file' not in request.files:
        return 'there is no file in form!'
    file = request.files['file']
    filename = secure_filename(file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in allowed_extensions or file_ext != validate_image(file.stream):
            return "Wrong file!"
    Classes = ["Tomato___Bacterial_spot","Tomato___Early_blight","Tomato___Late_blight","Tomato___Leaf_Mold","Tomato___Septoria_leaf_spot","Tomato___Spider_mites Two-spotted_spider_mite","Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus","Tomato___healthy"]
    model=load_model(CROP_MODEL_PATH)
    model.load_weights(CROP_WEIGHTS_PATH)
    result = np.argmax(model.predict([prepare_image(file)]), axis=-1)
    answer = Classes[int(result)]
    print(answer)
    return json.dumps({'result': answer})


if __name__ == '__main__':
    print("starting python flask server for Best Crop Prediction")
    app.run(debug=True, host='0.0.0.0')
