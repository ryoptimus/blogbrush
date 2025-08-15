import os
import json

import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
from post import Post
from helpers import (
    get_blog_name, get_target, get_function, get_qparams, append_qparams_to_url
)

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
token = os.getenv('TOKEN')
token_secret = os.getenv('TOKEN_SECRET')

def form_request_url(blog_name, target):
    # Construct the API URL
    api_url = f'https://api.tumblr.com/v2/blog/{blog_name}.tumblr.com'
    if target.lower() == 'p' or target.lower() == 'posts':
        print('You have chosen posts.\n')
        request_url = api_url + '/posts'
    elif target.lower() == 'l' or target.lower() == 'likes':
        print('You have chosen likes.\n')
        request_url = api_url + f'/likes?api_key={consumer_key}'
    else:
        print('You have chosen drafts.\n')
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

# GET function for posts and drafts
def get_posts(request_url, oauth):
    # Get posts / drafts
    # print(f'Request URL: {request_url}')
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
        post = Post.get_info(p)
        posts.append(post)

    # print(request_url)
    # Split at '/v2/blog/' to get the blog part first
    blog_part = request_url.split('/v2/blog/')[1]  # username.tumblr.com/posts

    # Split at '.' to get the blog identifier
    blog_id = blog_part.split('/')[0]
    print(blog_id)

    print(f'{len(posts)} post(s) acquired. Printing summaries...\n')

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
        # print(json.dumps(data['response']['liked_posts'], indent=2))
        return data
    except ValueError as error:
        print(f"Error parsing JSON: {error}")
        return

def read_likes(request_url, oauth):
    data = get_likes(request_url, oauth)

    posts = []
    for p in data['response']['liked_posts']:
        post = Post.get_info(p)
        posts.append(post)

    print(f'Request URL: {request_url}')
    # Split at '/v2/blog/' to get the blog part first
    blog_part = request_url.split('/v2/blog/')[1]  # username.tumblr.com/posts

    # Split at '.' to get the blog identifier
    blog_id = blog_part.split('/')[0]
    # print(blog_id)

    print(f'{len(posts)} like(s) acquired. Printing summaries...\n')

    for post in posts:
        print(post)
    
def read_drafts(request_url, oauth):
    data = get_posts(request_url, oauth)

    # Create class instances for posts returned
    posts = []
    for p in data['response']['posts']:
        post = Post.get_info(p)
        posts.append(post)

    # Split at '/v2/blog/' to get the blog part first
    blog_part = request_url.split('/v2/blog/')[1]  # username.tumblr.com/posts

    # Split at '.' to get the blog identifier
    blog_id = blog_part.split('/')[0]
    # print(blog_id)

    print(f'{len(posts)} draft(s) acquired. Printing summaries...\n')

    for post in posts:
        print(post)

def unlike_posts(request_url, oauth):
    data = get_likes(request_url, oauth)
    posts = []
    for p in data['response']['liked_posts']:
        post = Post.get_info(p)
        posts.append(post)
    
    print(f'{len(posts)} like(s) acquired. Unliking...\n')

    if posts:
        for post in posts:
            # print(post)
            unlike_url = f'https://api.tumblr.com/v2/user/unlike'
            rparams = {
                'id': post.id,
                'reblog_key': post.reblog_key
            }

            try:
                unlike_response = requests.post(unlike_url, auth=oauth, data=rparams)
                unlike_response.raise_for_status()
            except requests.exceptions.RequestException as error:
                print(f"Error unliking post {post.id}: {error}")
                continue

            print(f'Post {post.id} unliked successfully.\n(status: {unlike_response.json()['meta']['status']}, msg: {unlike_response.json()['meta']['msg']})\n')
    else:
        print('No likes found matching given parameters. 0 posts unliked.')

def delete_posts(request_url, oauth):
    data = get_posts(request_url, oauth)

    posts = []
    for p in data['response']['posts']:
        post = Post.get_info(p)
        posts.append(post)

    print(f'Request URL: {request_url}')
    # Split at '/v2/blog/' to get the blog part first
    blog_part = request_url.split('/v2/blog/')[1]  # username.tumblr.com/posts

    # Split at '.' to get the blog identifier
    blog_id = blog_part.split('/')[0]
    # print(blog_id)

    if posts:
        print(f'{len(posts)} post(s) acquired. Deleting...\n')
        
        for post in posts:
            print(post)
            delete_url = f'https://api.tumblr.com/v2/blog/{blog_id}/post/delete'
            rparams = {
                'id': post.id
            }

            try:
                del_response = requests.post(delete_url, auth=oauth, data=rparams)
                del_response.raise_for_status()
            except requests.exceptions.RequestException as error:
                print(f"Error deleting post {post.id}: {error}")
                continue

            print(f'Post {post.id} deleted successfully.\n(status: {del_response.json()['meta']['status']}, msg: {del_response.json()['meta']['msg']})\n')
    else:
        print('No posts found matching given parameters. 0 posts deleted.')
    
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
        if target == 'p' or target == 'posts':
            print('You have chosen to read posts.')
            read_posts(request_url, oauth)
        elif target == 'l' or target == 'likes':
            print('You have chosen to read likes.')
            read_likes(request_url, oauth)
        else:
            # print('You have chosen to read drafts.')
            read_drafts(request_url, oauth)
    elif function == 'd' or function == 'delete':
        print('You have chosen to delete posts.')
        delete_posts(request_url, oauth)
    elif function == 'u' or function == 'unlike':
        print('You have chosen to unlike posts.')
        unlike_posts(request_url, oauth)
    else:
        print('You have chosen to edit posts.')

if __name__ == "__main__":
    run_session()