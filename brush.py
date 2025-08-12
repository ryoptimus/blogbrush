import os
import json

import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
from helpers import (
    get_blog_name, get_target, get_function, get_qparams, append_qparams_to_url
)

load_dotenv()

class Post:
    def __init__(self, id, url, type, date, timestamp, summary, tags):
        self.id = id
        self.url = url
        self.type = type
        self.date = date
        self.timestamp = timestamp
        self.summary = summary
        self.tags = tags

    def __repr__(self):
        return (
            f"Post(id={self.id},\n\t"
            f"url='{self.url}',\n\t"
            f"type='{self.type}',\n\t"
            f"date='{self.date}',\n\t"
            f"timestamp={self.timestamp},\n\t"
            f"summary='{self.summary}',\n\t"
            f"tags={self.tags})"
        )

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
token = os.getenv('TOKEN')
token_secret = os.getenv('TOKEN_SECRET')

def form_request_url(blog_name, target):
    # Construct the API URL
    api_url = f'https://api.tumblr.com/v2/blog/{blog_name}.tumblr.com'
    if target.lower() == 'p' or target.lower() == 'posts':
        print('You have chosen posts.')
        request_url = api_url + '/posts'
    elif target.lower() == 'l' or target.lower() == 'likes':
        print('You have chosen likes.')
        request_url = api_url + f'/likes?api_key={consumer_key}'
    else:
        print('You have chosen drafts.')
        request_url = api_url + '/posts/draft'

    return request_url

def get_user_input():
    blog_name = get_blog_name()
    target = get_target()
    request_url = form_request_url(blog_name, target)
    function = get_function(target)
    qparams = get_qparams(target)
    request_url = append_qparams_to_url(request_url, qparams)

    return blog_name, target, request_url, function, qparams

def get_posts(request_url, oauth):
    # Get posts
    try:
        response = requests.get(request_url, auth=oauth)
        response.raise_for_status()
        
    except requests.exceptions.RequestException as error:
        print(f"Error: {error}")

    # Parse JSON
    try:
        data = response.json()
        # print(json.dumps(data['response']['posts'], indent=2))
        return data
    except ValueError as error:
        print(f"Error parsing JSON: {error}")
        return

def read_posts(request_url, oauth):
    data = get_posts(request_url, oauth)

    posts = []
    for p in data['response']['posts']:
        post = Post(
            p['id'],
            p['post_url'],
            p['type'],
            p['date'],
            p['timestamp'],
            p['summary'],
            p['tags']
        )
        posts.append(post)

    print(request_url)
    # Split at '/v2/blog/' to get the blog part first
    blog_part = request_url.split('/v2/blog/')[1]  # username.tumblr.com/posts

    # Split at '.' to get the blog identifier
    blog_id = blog_part.split('/')[0]
    print(blog_id)

    for post in posts:
        print(post)

def get_likes(request_url, oauth):
    # Get likes
    try:
        response = requests.get(request_url, auth=oauth)
        response.raise_for_status()
        
    except requests.exceptions.RequestException as error:
        print(f"Error: {error}")

    # Parse JSON
    try:
        data = response.json()
        print(json.dumps(data['response']['liked_posts'], indent=2))
        return data
    except ValueError as error:
        print(f"Error parsing JSON: {error}")
        return

def read_likes(request_url, oauth):
    data = get_likes(request_url, oauth)

    posts = []
    for p in data['response']['liked_posts']:
        post = Post(
            p['id'],
            p['post_url'],
            p['type'],
            p['date'],
            p['timestamp'],
            p['summary'],
            p['tags']
        )
        posts.append(post)

    print(f'Request URL: {request_url}')
    # Split at '/v2/blog/' to get the blog part first
    blog_part = request_url.split('/v2/blog/')[1]  # username.tumblr.com/posts

    # Split at '.' to get the blog identifier
    blog_id = blog_part.split('/')[0]
    # print(blog_id)

    for post in posts:
        print(post)

def delete_posts(request_url, qparams, oauth):
    data = get_posts(request_url, oauth)

    posts = []
    for p in data['response']['posts']:
        post = Post(
            p['id'],
            p['post_url'],
            p['type'],
            p['date'],
            p['timestamp'],
            p['summary'],
            p['tags']
        )
        posts.append(post)

    print(f'Request URL: {request_url}')
    # Split at '/v2/blog/' to get the blog part first
    blog_part = request_url.split('/v2/blog/')[1]  # username.tumblr.com/posts

    # Split at '.' to get the blog identifier
    blog_id = blog_part.split('/')[0]
    # print(blog_id)

    for post in posts:
        print(post)
        delete_url = f'https://api.tumblr.com/v2/blog/{blog_id}/post/delete'
        data = {
            'id': post.id
        }

        try:
            del_response = requests.post(delete_url, auth=oauth, data=data)
            del_response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(f"Error deleting post {post.id}: {error}")
            continue

        print(f'Post {post.id} deleted successfully.\n(status: {del_response.json()['meta']['status']}, msg: {del_response.json()['meta']['msg']})')
    
    # if not ('l' in qparams or 'limit' in qparams):

def run_session():
    blog_name, target, request_url, function, qparams = get_user_input()

    # Create OAuth1 session
    oauth = OAuth1(
        consumer_key,
        consumer_secret,
        token,
        token_secret
    )

    if function == 'r' or function == 'read':
        print('You have chosen to read posts.')
        if target == 'p' or target == 'posts':
            read_posts(request_url, oauth)
        elif target == 'l' or target == 'likes':
            read_likes(request_url, oauth)
    elif function == 'd' or function == 'delete':
        print('You have chosen to delete posts.')
        delete_posts(request_url, qparams, oauth)
    elif function == 'u' or function == 'unlike':
        print('You have chosen to unlike posts.')
    else:
        print('You have chosen to edit posts.')

if __name__ == "__main__":
    run_session()