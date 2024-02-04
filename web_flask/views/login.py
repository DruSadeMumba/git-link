#!/usr/bin/python3
"""Firebase login"""
import pyrebase
from flask import redirect, render_template, request, session, url_for
from web_flask import app_views, app
from web_flask.config import Config


app.config.from_object(Config)
firebaseConfig = app.config['FIREBASE_CONFIG']
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
firebase_user = {"is_logged_in": False, "username": "", "email": "", "uid": ""}
db = firebase.database()


@app_views.route("/login")
def log_in():
    return render_template("login.html")


@app_views.route("/login", methods=["POST", "GET"])
def login():
    render_template("login.html")
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            global firebase_user
            firebase_user["is_logged_in"] = True
            firebase_user["email"] = user["email"]
            firebase_user["uid"] = user["localId"]

            data = db.child("users").get()
            firebase_user["username"] = data.val()[firebase_user["uid"]]["username"]

            return redirect(url_for('profile', uid=firebase_user["uid"]))

        except Exception as e:
            print(f"Error logging in user: {str(e)}")
            return redirect(url_for('login'))
    else:
        if session.get("is_logged_in"):
            return redirect(url_for('profile', uid=session["uid"]))
        else:
            return redirect(url_for('login'))
