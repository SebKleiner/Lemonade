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

    def represents_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

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
        df_ = pd.DataFrame(columns=structure)
        final = []

        if state == '' or postcode == '' or policies == '' or age == '' or coast == '' or form == '' or fire == ''\
                or fire_prox == '' or payment == '' or burglar == '' or portable == '' or \
                represents_int(postcode) is False or represents_int(age) is False:
            return render_template('index.html', message='Please enter required fields')
        else:
            final.append(int(postcode))
            final.append(fire)
            final.append(burglar)
            final.append(portable)
            final.append(int(age))
            final.append(int(policies))

            states = [i[i.index("_") + len("_"):] for i in structure if i.startswith('state_')]

            for j, item in enumerate(states):
                if item == state or state not in states and j == len(states) - 1:
                    final.append(1)
                elif j < len(states):
                    final.append(0)

            forms = [i[i.index("_") + len("_"):] for i in structure if i.startswith('form_')]

            for j, item in enumerate(forms):
                if item == form:
                    final.append(1)
                else:
                    final.append(0)

            coasts = [i[i.index("_") + len("_"):] for i in structure if i.startswith('coast_')]

            for j, item in enumerate(coasts):
                if item == coast or coast not in coasts and j == len(coasts) - 1:
                    final.append(1)
                elif j < len(coasts):
                    final.append(0)

            fires = [i[i.rfind("_") + len("_"):] for i in structure if i.startswith('fire_housing_proximity_')]

            for j, item in enumerate(fires):
                if item == fire_prox or fire_prox not in fires and j == len(fires) - 1:
                    final.append(1)
                elif j < len(fires):
                    final.append(0)

            policies_count = [i[i.rfind("_") + len("_"):] for i in structure if i.startswith('previous_policies_')]

            for j, item in enumerate(policies_count):
                if item == policies or policies not in policies_count and j == len(policies_count) - 1:
                    final.append(1)
                elif j < len(policies_count):
                    final.append(0)

            payments = [i[i.rfind("_") + len("_"):] for i in structure if i.startswith('card_type_')]

            for j, item in enumerate(payments):
                if item == payment:
                    final.append(1)
                else:
                    final.append(0)

            a_series = pd.Series(final, index=structure)
            df_ = df_.append(a_series, ignore_index=True)

            x_target = sc.transform(df_)

            prediction = model.predict_classes(x_target)[0]

            if prediction == 0:
                return render_template('index.html', message='Your submission has been processed!')
            else:
                return render_template('index.html', message='Oh! :( There has been an error with your submission. '
                                                             'Please, contact a Lemonade assistant')


if __name__ == '__main__':
    app.run()
