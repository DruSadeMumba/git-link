#!/usr/bin/python3
"""Firebase user profile"""
from firebase_admin import db
from flask import redirect, url_for, render_template
from web_flask import app_views


@app_views.route("/profile", strict_slashes=False)
def my_profile():
    return redirect(url_for('app_views.profile'))


@app_views.route("/profile/<uid>", strict_slashes=False)
def profile(uid):
    uid_ref = db.reference('users/' + uid)
    uid_data = uid_ref.get()
    if uid_data:
        return render_template('profile.html', uid=uid)
    else:
        return 'UID not found in the database', 404


@app_views.route("/logout")
def logout():
    return redirect(url_for('app_views.search'))
