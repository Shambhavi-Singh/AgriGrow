from flask import Flask, request, jsonify, render_template
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('app.html')


if __name__ == '__main__':
    print("starting python flask server for Best Crop Prediction")
    app.run(debug=True, host='0.0.0.0')
