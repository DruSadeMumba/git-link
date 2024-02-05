#!/usr/bin/python3
"""Firebase user profile"""
import pyrebase
from flask import redirect, url_for, session, render_template
from web_flask import app_views
from web_flask.config import Config

app_config = Config()
firebaseConfig = app_config.FIREBASE_CONFIG

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


@app_views.route("/profile", methods=["POST", "GET"], strict_slashes=False)
def my_profile():
    if 'is_logged_in' in session and session['is_logged_in']:
        return render_template('profile.html', uid=session["uid"])
    else:
        return redirect(url_for('app_views.login'))


@app_views.route("/profile/<uid>", methods=["POST", "GET"], strict_slashes=False)
def profile(uid):
    if 'is_logged_in' in session and session['is_logged_in']:
        return render_template('profile.html', uid=uid, email=session["email"],
                               username=session["username"])
    else:
        return redirect(url_for('app_views.login'))


@app_views.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('app_views.gituser'))
