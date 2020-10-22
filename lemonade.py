from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        state = request.form['state']
        policies = request.form['policies']

        if customer == '' or state == '':
            return render_template('index.html', message='Please enter required fields')
        else:
            return render_template('index.html', message='Your submission has been processed!')


if __name__ == '__main__':
    app.run()