#!/usr/bin/python3
"""Retrieve GitHub info"""
import os
from flask import render_template, request
from web_flask import app_views
import requests
import time

token = os.getenv('GITHUB_TOKEN')


@app_views.route("/search/", methods=['GET'])
def search():
    return render_template('user.html', user_info='', repo_info='')


@app_views.route("/search/", methods=['POST'])
def fetch_user():
    username = request.form.get('username')
    user_info = get_github_user_info(username)
    if user_info is None:
        return render_template('404.html'), 404
    repo_info = get_user_repos(username)
    if repo_info is None:
        return render_template('404.html'), 404
    return render_template('user.html', user_info=user_info, repo_info=repo_info)


def get_github_user_info(username):
    headers = {'Authorization': f'token {token}'}
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
        'avatar_url': data.get('avatar_url')
    }
    handle_rate_limit(response)
    return user_info


def get_user_repos(username):
    headers = {'Authorization': f'token {token}'}
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
                'stargazers_count': repo['stargazers_count']
            })
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None
        handle_rate_limit(response)
    return repo_info


def handle_rate_limit(response):
    if int(response.headers.get('X-RateLimit-Remaining', 0)) <= 0:
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        sleep_time = reset_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
