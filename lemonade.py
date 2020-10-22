from flask import Flask, render_template, request

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

        if state == '':
            return render_template('index.html', message='Please enter required fields')
        else:
            return render_template('index.html', message='Your submission has been processed!')


if __name__ == '__main__':
    app.run()