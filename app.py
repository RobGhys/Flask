from flask import Flask, redirect, url_for, render_template, request,session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'hello'
app.permanent_session_lifetime = timedelta(days=30) # Stores session data for 30 days

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
        session.permanent = True # Needed in order to store session data
        user_name = request.form['nm']
        session['user'] = user_name
        return redirect(url_for('user'))

    # Displays login page
    else:
        # Redirects to user page if the user is already logged-in
        if 'user' in session:
            return redirect(url_for('user'))
        return render_template('login.html')

@app.route('/logout/')
def logout():
    # Removes user data from session
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/user/')
def user():
    if 'user' in session:
        user_name = session['user']
        return f'<h1>{user_name}</h1>'
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)