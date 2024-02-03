#!/usr/bin/python3
"""Importing the necessary module for running the app."""
from flask import Flask, render_template, redirect, request, session
import os
import requests
import time
app = Flask(__name__)


@app.route('/search', methods=['POST'], strict_slashes=False)
def search():
    username = request.form.get('username')
    user_info = get_github_user_info(username)
    if user_info is None:
        return render_template('404.html'), 404
    repo_info = get_user_repos(username)
    if repo_info is None:
        return render_template('404.html'), 404
    return render_template('user.html', user_info=user_info, repo_info=repo_info)


def get_github_user_info(username):
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'}
    response = requests.get(f'https://api.github.com/users/{username}', headers=headers)
    if response.status_code != 200:
        return "Failed to fetch user information from GitHub.", 500
    data = response.json()
    user_info = {
        'username': data.get('login'),
        'bio': data.get('bio'),
        'total_repos': data.get('public_repos'),
        'followers': data.get('followers'),
        'following': data.get('following'),
        'location': data.get('location')
    }
    return user_info


def get_user_repos(username):
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'}
    url = f'https://api.github.com/users/{username}/repos'
    repo_info = []
    while url:
        response = requests.get(url, headers=headers)
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
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None
        if int(response.headers.get('X-RateLimit-Remaining', 0)) <= 0:
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            sleep_time = reset_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
    return repo_info


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
