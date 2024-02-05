#!/usr/bin/python3
"""Firebase sign up"""
import pyrebase
from flask import redirect, render_template, request, session, url_for
from web_flask import app_views, app
from web_flask.config import Config

app_config = Config()
firebaseConfig = app_config.FIREBASE_CONFIG

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


@app_views.route("/signup", strict_slashes=False)
def sign_up():
    return render_template("sign-up.html")


@app_views.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            session["is_logged_in"] = True
            session["email"] = user["email"]
            session["uid"] = user["localId"]
            session["username"] = username

            data = {"username": username, "email": email}
            db.child("users").child(session["uid"]).set(data)

            return redirect(url_for('app_views.profile', uid=session["uid"]))

        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return redirect(url_for('app_views.signup'))

    else:
        if 'is_logged_in' in session and session['is_logged_in']:
            return redirect(url_for('app_views.profile', uid=session["uid"]))
        else:
            return render_template("signup.html")
