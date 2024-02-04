#!/usr/bin/python3
"""Firebase user profile"""
import pyrebase
from flask import redirect, url_for
from web_flask import app_views, app
from web_flask.config import Config

app.config.from_object(Config)
firebaseConfig = app.config['FIREBASE_CONFIG']
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
firebase_user = {"is_logged_in": False, "username": "", "email": "", "uid": ""}
db = firebase.database()


@app_views.route("/profile")
def my_profile():
    if firebase_user["is_logged_in"]:
        return redirect(url_for('app_views.profile', uid=firebase_user["uid"]))
    else:
        return redirect(url_for('app_views.login'))


@app_views.route("/profile/<uid>")
def profile(uid):
    if firebase_user["is_logged_in"]:
        return redirect(url_for('app_views.profile', uid=uid, email=firebase_user["email"],
                                username=firebase_user["username"]))
    else:
        return redirect(url_for('app_views.login'))
