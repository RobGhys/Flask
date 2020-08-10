from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from data_base_be import *

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=5) # Stores session data for 30 days

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100)) # Uses variable name to give a name to the column in database
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    # Redirects to user page
    if request.method == 'POST':
        session.permanent = True # Needed in order to store session data
        user = request.form['nm']
        session['user'] = user
        flash(f"Logged in successful, {user}", "info")
        return redirect(url_for('user'))

    # Displays login page
    else:
        # Redirects to user page if the user is already logged-in
        if 'user' in session:
            flash("Already logged in", "info")
            return redirect(url_for('user'))
        return render_template('login.html')


@app.route('/user/', methods=["POST", "GET"])
def user():
    email = None
    if 'user' in session:
        user = session['user']

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email recorded successfuly", "info")
        else:
            if "email" in session:
                email = session["email"]
        # Passes email and displays it
        return render_template("user.html", user=user, email=email)
    else:
        flash("You are not logged in", "info")
        return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    flash(f'You have been logged out!', 'info')
    # Removes user and email data from session
    session.pop('user', None)
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)