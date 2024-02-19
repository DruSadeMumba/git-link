#!/usr/bin/python3
"""Retrieve GitHub info"""
from flask import render_template, request, redirect, url_for
import os
import requests
import time
from web_flask import app, app_views
from web_flask.config import Config

app.config.from_object(Config)
app.url_map.strict_slashes = False
"""token = os.getenv('GITHUB_TOKEN')"""
token = app.config['GITHUB_TOKEN']
headers = {'Authorization': f'token {token}'}


@app_views.route("/search/github", methods=['GET'])
def search():
    """Search GitHub user (default: github)"""
    username = 'github'
    user_info = get_github_user_info(username)
    repo_info = get_user_repos(username)
    return render_template('user.html', user_info=user_info, repo_info=repo_info)


@app_views.route("/404", methods=['GET'])
def not_found():
    """404 page"""
    return render_template('404.html')


@app_views.route("/search", methods=['POST'])
def fetch_user():
    """Fetch GitHub user"""
    if request.method == 'POST':
        username = request.form.get('username')
        user_info = get_github_user_info(username)
        if user_info:
            return redirect(url_for('app_views.return_user', username=username))
        else:
            return render_template('404.html')


@app_views.route("/search/<username>", methods=['GET'])
def return_user(username):
    """Return GitHub user"""
    user_info = get_github_user_info(username)
    if user_info:
        repo_info = get_user_repos(username)
        if repo_info:
            return render_template('user.html', user_info=user_info, repo_info=repo_info)
        else:
            return None
    else:
        return render_template('404.html')


def get_github_user_info(username):
    """Retrieve GitHub user info"""
    response = requests.get(f'https://api.github.com/users/{username}', headers=headers)
    if response.status_code != 200:
        return None
    data = response.json()
    user_info = {
        'username': data.get('login'),
        'bio': data.get('bio'),
        'total_repos': data.get('public_repos'),
        'followers': data.get('followers'),
        'following': data.get('following'),
        'location': data.get('location'),
        'avatar_url': data.get('avatar_url'),
        'html_url': data.get('html_url')
    }
    handle_rate_limit(response)
    return user_info


def get_user_repos(username):
    """Retrieve GitHub user repos"""
    url = f'https://api.github.com/users/{username}/repos'
    repo_info = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        data = response.json()
        for repo in data:
            repo_info.append({
                'name': repo['name'],
                'description': repo['description'],
                'forks_count': repo['forks_count'],
                'stargazers_count': repo['stargazers_count'],
                'html_url': repo['html_url']
            })
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None
        handle_rate_limit(response)
    return repo_info


def handle_rate_limit(response):
    """Handle GitHub API rate limit"""
    if int(response.headers.get('X-RateLimit-Remaining', 0)) <= 0:
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        sleep_time = reset_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
