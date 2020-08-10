from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'hello'
app.permanent_session_lifetime = timedelta(days=5) # Stores session data for 30 days

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


@app.route('/user/')
def user():
    if 'user' in session:
        user = session['user']
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in", "info")
        return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    flash(f'You have been logged out!', 'info')
    # Removes user data from session
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)