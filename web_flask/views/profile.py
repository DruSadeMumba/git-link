#!/usr/bin/python3
"""Firebase user profile"""
from flask import Flask, redirect, render_template, url_for
import pyrebase

from web_flask import app_views
from web_flask.config import Config

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']
firebaseConfig = app.config['FIREBASE_CONFIG']

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
firebase_user = {"is_logged_in": False, "username": "", "email": "", "uid": ""}
db = firebase.database()


@app_views.route("/profile/")
def my_profile():
    if firebase_user["is_logged_in"]:
        return redirect(url_for('profile', uid=firebase_user["uid"]))
    else:
        return redirect(url_for('login'))


@app_views.route("/profile/<uid>")
def profile(uid):
    if firebase_user["is_logged_in"]:
        return render_template("profile.html", uid=uid, email=firebase_user["email"],
                               username=firebase_user["username"])
    else:
        return redirect(url_for('login'))
