#!/usr/bin/python3
"""Retrieve GitHub info"""
from flask import render_template, request, redirect, url_for, jsonify
import requests
import time
from web_flask import app, app_views
from web_flask.config import Config

app.config.from_object(Config)
app.url_map.strict_slashes = False
"""token = os.getenv('GITHUB_TOKEN')"""
token = app.config['GITHUB_TOKEN']
headers = {'Authorization': f'token {token}'}


@app_views.route("/repos/search/github", methods=['GET'])
def search_repo():
    """Search GitHub repo (default: github)"""
    print('search_repo')
    repo_name = 'github'
    sort = 'stars'
    language = 'python'
    repo_list = get_repos(repo_name, sort=sort, language=language)
    return jsonify(repo_list), 200
    # return render_template('repo.html', repo_list=repo_list)


@app_views.route("/repos/search", methods=['POST'])
def fetch_repo():
    """Fetch GitHub repo"""
    if request.method == 'POST':
        repo_name = request.form.get('repo_name')
        sort = request.form.get('sort')
        language = request.form.get('language')
        repo_list = get_repos(repo_name, sort=sort, language=language)
        if repo_list:
            return jsonify(repo_list), 200
            # return redirect(url_for('app_views.return_repo', repo_name=repo_name, sort=sort, language=language))
        else:
            return redirect(url_for('404.html'))


@app_views.route("/repos/search/<repo_name>/<sort>/<language>", methods=['GET'])
def return_repo(repo_name, sort, language):
    """Return GitHub repos"""
    # sort = request.form.get('sort')
    # language = request.form.get('language')
    repo_list = get_repos(repo_name, sort=sort, language=language)
    if repo_list:
        return jsonify(repo_list), 200
        # return render_template('repo.html', repo_list=repo_list)
    else:
        return redirect(url_for('404.html'))


def get_repos(repo_name, sort, language):
    """Retrieve GitHub user repos"""
    url = f'https://api.github.com/search/repositories?q={repo_name}+language:{language}&sort={sort}&page=1&per_page=10'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    repo_list = []
    data = response.json()
    print(data)
    if 'items' in data:
        for repo in data['items']:
            repo_info = {
                'name': repo.get('name'),
                'description': repo.get('description'),
                'forks_count': repo.get('forks_count'),
                'stargazers_count': repo.get('stargazers_count'),
                'html_url': repo.get('html_url')
            }
            repo_list.append(repo_info)
    handle_rate_limit(response)
    return repo_list


def handle_rate_limit(response):
    """Handle GitHub API rate limit"""
    if int(response.headers.get('X-RateLimit-Remaining', 0)) <= 0:
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        sleep_time = reset_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
