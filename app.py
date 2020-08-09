from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/test/')
def test():
    return render_template('lamba.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    # Redirects to user page
    if request.method == 'POST':
        user_name = request.form['nm']
        return redirect(url_for('user', usr=user_name))
    # Displays login page
    else:
        return render_template('login.html')



@app.route('/<usr>/')
def user(usr):
    return f'<h1>{usr}</h1>'


if __name__ == '__main__':
    app.run(debug=True)