#!/usr/bin/python3
"""Importing the necessary module for running the app."""
from flask import Flask, render_template, redirect, request, session
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

"""Github OAuth Configuration"""
github_client_id = os.environ.get('GITHUB_CLIENT_ID')
github_client_secret = os.environ.get('GITHUB_CLIENT_SECRET')
github_redirect_uri = 'http://localhost:5000/callback'
github_scope = 'user'


@app.route('/login/', strict_slashes=False)
def login():
    """Creating a loging route."""
    if not github_client_id or not github_client_secret:
        return "Please set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET environment variables"
    auth_url = f"https://github.com/login/oauth/authorize?client_id={github_client_id}&redirect_uri={github_redirect_uri}&scope={github_scope}"
    return redirect(auth_url)


@app.route('/callback', strict_slashes=False)
def callback():
    """"Creating a callback route."""
    code = request.args.get('code')
    if not code:
        return redirect('/'), 400  # Client-side error: Missing code parameter in the query string
    if not github_client_id or not github_client_secret:
        return "Please set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET environment variables", 500  # Server-side error: Missing client_id or client_secret environment variables
    data = {
        'code': code,
        'client_id': github_client_id,
        'client_secret': github_client_secret,
    }
    headers = {'Accept': 'application/json'}
    response = requests.post('https://github.com/login/oauth/access_token', data=data, headers=headers)
    """The response should look like this:
        {
        "access_token": "e72e16c7e42f292c6912e7710c838347ae178b4a",
        "token_type": "bearer",
        "scope": "repo,gist"
        }
    """
    if response.status_code != 200:
        return 'An error occurred while retrieving your access token', 500  # Server-side error: Missing client_id or client_secret environment variables
    access_token = response.json().get('access_token')
    if not access_token:
        return 'Access token not receieved from GithHub.', 500  # Server-side error: Missing client_id or client_secret environment variables
    session['access_token'] = access_token
    return redirect('/profile')  ## need to be changed in case needed


@app.route('/profile/', strict_slashes=False)
def profile():
    if 'access_token' not in session:
        return "User not authenticated.", 401
    user_info = get_github_user_info()
    repo_info = get_user_repos()
    return render_template('profile.html', user_info=user_info, repo_info=repo_info)


def get_github_user_info():
    access_token = session.get('access_token')
    if not access_token:
        return "Access token not found in session.", 500
    headers = {'Authorization': f"token {access_token}"}
    response = requests.get('https://api.github.com/user', headers=headers)
    if response.status_code != 200:
        return "Failed to fetch user information from GitHub.", 500
    data = response.json()
    user_info = {
        'username': data.get('login'),
        'total_repos': data.get('total_repos'),
        'followers': data.get('followers'),
        'following': data.get('following'),
        'location': data.get('location')
    }
    return user_info


def get_user_repos():
    """Function to retrieve the user's repositories."""
    access_token = session.get('access_token')
    if not access_token:
        return "Access token not found in session.", 500
    headers = {'Authorization': f"token {access_token}"}
    repos_url = 'https://api.github.com/user/repos'
    repo_info = []
    while repos_url:
        response = requests.get(repos_url, headers=headers)
        if response.status_code != 200:
            return "Failed to fetch user information from GitHub.", 500
        data = response.json()
        for repo in data:
            repo_info.append({
                'name': repo['name'],
                'description': repo['description'],
                'forks_count': repo['forks_count'],
                'stargazers_count': repo['stargazers_count']
            })
        repos_url = response.links['next']['url'] if 'next' in response.links else None
    return repo_info



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)