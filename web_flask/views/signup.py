#!/usr/bin/python3
"""Firebase sign up"""
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


@app_views.route("/signup")
def sign_up():
    return render_template("sign-up.html")


@app_views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            global firebase_user
            firebase_user["is_logged_in"] = True
            firebase_user["email"] = user["email"]
            firebase_user["uid"] = user["localId"]
            firebase_user["username"] = username

            data = {"username": username, "email": email}
            db.child("users").child(firebase_user["uid"]).set(data)

            return redirect(url_for('app_views.profile', uid=firebase_user["uid"]))

        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return redirect(url_for('app_views.signup'))

    else:
        if session.get("is_logged_in"):
            return redirect(url_for('app_views.profile', uid=session["uid"]))
        else:
            return redirect(url_for('app_views.signup'))
