from flask import Flask, request, jsonify, render_template
import pickle
import os
import pandas as pd
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(APP_ROOT, "./crop_rec_model.pickle")
LOCATION_PATH = os.path.join(APP_ROOT, "./location.csv")


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


if __name__ == '__main__':
    print("starting python flask server for Best Crop Prediction")
    app.run(debug=True, host='0.0.0.0')
