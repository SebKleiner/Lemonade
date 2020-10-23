from flask import Flask, render_template, request
from joblib import load
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pickle
import pandas as pd


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        postcode = request.form['postcode']
        state = request.form['state']
        policies = request.form['policies']
        age = request.form['age']
        coast = request.form['coast']
        form = request.form['form']
        fire = request.form['fire']
        fire_prox = request.form['fire_prox']
        payment = request.form['payment']
        burglar = request.form['burglar']
        portable = request.form['portable']

        with open('structure.pkl', 'rb') as f:
            structure = pickle.load(f)

        sc = load('scaler.joblib')
        model = load_model('oversample_model.h5')

        if state == '' or postcode == '' or policies == '' or age == '' or coast == '' or form == '' or fire == ''\
                or fire_prox == '' or payment == '' or burglar == '' or portable == '':
            return render_template('index.html', message='Please enter required fields')
        else:
            return render_template('index.html', message='Your submission has been processed!')


if __name__ == '__main__':
    app.run()
