#!/usr/bin/python3
from flask import Flask, redirect, render_template, request, url_for
import pyrebase

app = Flask(__name__)
app.url_map.strict_slashes = False

firebaseConfig = {'apiKey': "AIzaSyAk2bynVPfj-5rW4y0K6256LdSE62cXDB0",
                  'authDomain': "git-link-d9cc9.firebaseapp.com",
                  'databaseURL': "https://trialauth-7eea1.firebaseio.com",
                  'projectId': "git-link-d9cc9",
                  'storageBucket': "git-link-d9cc9.appspot.com",
                  'messagingSenderId': "911947476553",
                  'appId': "1:911947476553:web:e8dbbbe137c97b524fd998",
                  'measurementId': "G-27ZGX5VGJS"
                  }

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
firebase_user = {"is_logged_in": False, "username": "", "email": "", "uid": ""}
db = firebase.database()


@app.route("/")
def splash():
    return render_template("index.html")


@app.route("/signup")
def sign_up():
    return render_template("sign-up.html")


@app.route("/login")
def log_in():
    return render_template("login.html")


@app.route("/git-user")
def fetch_user():
    return render_template("user.html")


@app.route("/profile")
def profile():
    if firebase_user["is_logged_in"]:
        return render_template("profile.html", email=firebase_user["email"], username=firebase_user["username"])
    else:
        return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
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

            return redirect(url_for('profile'))
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return redirect(url_for('signup'))

    else:
        if firebase_user["is_logged_in"]:
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('signup'))


@app.route("/login", methods=["POST", "GET"])
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
            return redirect(url_for('profile'))
        except auth.AuthError as e:
            print(f"Error logging in user: {str(e)}")
            return redirect(url_for('login'))
    else:
        if firebase_user["is_logged_in"]:
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
