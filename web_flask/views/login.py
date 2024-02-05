#!/usr/bin/python3
"""Firebase login"""
import pyrebase
from flask import redirect, render_template, request, session, url_for

from web_flask import app_views
from web_flask.config import Config

app_config = Config()
firebaseConfig = app_config.FIREBASE_CONFIG

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


@app_views.route("/login", strict_slashes=False)
def log_in():
    return render_template("login.html")


@app_views.route("/login", methods=["POST", "GET"], strict_slashes=False)
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session["is_logged_in"] = True
            session["email"] = user["email"]
            session["uid"] = user["localId"]

            data = db.child("users").get()
            session["username"] = data.val()[session["uid"]]["username"]

            return redirect(url_for('app_views.profile', uid=session["uid"]))

        except Exception as e:
            print(f"Error logging in user: {str(e)}")
            return redirect(url_for('app_views.login'))

    else:
        if 'is_logged_in' in session and session['is_logged_in']:
            return redirect(url_for('app_views.profile', uid=session["uid"]))
        else:
            return redirect(url_for('app_views.login'))
