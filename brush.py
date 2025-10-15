import os
import json

import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
from session import Session
from post import Post
from query import gather_posts, gather_likes
from helpers import (
    get_blog_name, craft_blog_id, get_target, get_function, get_qparams, append_param_to_url, append_qparams_to_url
)

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
token = os.getenv('TOKEN')
token_secret = os.getenv('TOKEN_SECRET')

def form_request_url(blog_identifier, target):
    # Construct the API URL
    api_url = f'https://api.tumblr.com/v2/blog/{blog_identifier}'
    if target.lower() == 'p' or target.lower() == 'posts':
        request_url = api_url + '/posts'
    elif target.lower() == 'l' or target.lower() == 'likes':
        request_url = api_url + f'/likes?api_key={consumer_key}'
    else:
        request_url = api_url + '/posts/draft'

    return request_url

def get_user_input():
    blog_name = get_blog_name()
    target = get_target()
    function = get_function(target)
    qparams = get_qparams(target)

    return blog_name, target, function, qparams

def parse_user_input(qparams, session):
    append_qparams_to_url(session, qparams)

def read_posts(session):
    posts = gather_posts(session)

    # Split at '/v2/blog/' to get the blog part first
    blog_part = session.request_url.split('/v2/blog/')[1]  # username.tumblr.com/posts

    # Split at '.' to get the blog identifier
    blog_id = blog_part.split('/')[0]
    # print(blog_id)

    print(f'{len(posts)} post(s) acquired. Printing summaries...\n')

    i = 1
    for post in posts:
        print(f'Post {i} [ID: {post.id}]: {post}\n')
        # print(post)
        i += 1

def read_likes(session):
    posts = gather_likes(session)

    print(f'Request URL: {session.request_url}')
    # Split at '/v2/blog/' to get the blog part first
    blog_part = session.request_url.split('/v2/blog/')[1]  # username.tumblr.com/posts

    # Split at '.' to get the blog identifier
    blog_id = blog_part.split('/')[0]
    # print(blog_id)

    print(f'{len(posts)} like(s) acquired. Printing summaries...\n')

    for post in posts:
        print(post)

# TODO: Implement higher draft limit, but it'll be different. No limit param, or before
#       However, a before_id param exists...  
def read_drafts(session):
    posts = gather_posts(session)

    # Split at '/v2/blog/' to get the blog part first
    blog_part = session.request_url.split('/v2/blog/')[1]  # username.tumblr.com/posts

    # Split at '.' to get the blog identifier
    blog_id = blog_part.split('/')[0]
    # print(blog_id)

    print(f'{len(posts)} draft(s) acquired. Printing summaries...\n')

    for post in posts:
        print(post)

def unlike_posts(session):
    posts = gather_likes(session)
    
    print(f'{len(posts)} like(s) acquired. Unliking...\n')

    if posts:
        for post in posts:
            print(post)
            unlike_url = f'https://api.tumblr.com/v2/user/unlike'
            rparams = {
                'id': post.id,
                'reblog_key': post.reblog_key
            }

            try:
                unlike_response = requests.post(unlike_url, auth=session.oauth, data=rparams)
                unlike_response.raise_for_status()
            except requests.exceptions.RequestException as error:
                print(f"Error unliking post {post.id}: {error}")
                continue

            print(f'Post {post.id} unliked successfully.\n(status: {unlike_response.json()['meta']['status']}, msg: {unlike_response.json()['meta']['msg']})\n')
    else:
        print('No likes found matching given parameters. 0 posts unliked.')

def delete_posts(session):
    posts = gather_posts(session)

    print(f'Request URL: {session.request_url}')
    # Split at '/v2/blog/' to get the blog part first
    blog_part = session.request_url.split('/v2/blog/')[1]  # username.tumblr.com/posts

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
                del_response = requests.post(delete_url, auth=session.oauth, data=rparams)
                del_response.raise_for_status()
            except requests.exceptions.RequestException as error:
                print(f"Error deleting post {post.id}: {error}")
                continue

            print(f'Post {post.id} deleted successfully.\n(status: {del_response.json()['meta']['status']}, msg: {del_response.json()['meta']['msg']})\n')
    else:
        print('No posts found matching given parameters. 0 posts deleted.')

def run_session():
    blog_name, target, function, qparams = get_user_input()
    blog_identifier = craft_blog_id(blog_name)
    request_url = form_request_url(blog_identifier, target)
    
    # Create OAuth1 session
    oauth = OAuth1(
        consumer_key,
        consumer_secret,
        token,
        token_secret
    )

    session = Session(
        blog_identifier = blog_identifier,
        request_url = request_url,
        oauth = oauth,
        target = target
    )

    parse_user_input(qparams, session)

    if function == 'r' or function == 'read':
        if target == 'p' or target == 'posts':
            print('You have chosen to read posts.\n')
            read_posts(session)
        elif target == 'l' or target == 'likes':
            print('You have chosen to read likes.\n')
            read_likes(session)
        else:
            # print('You have chosen to read drafts.')
            read_drafts(session)
    elif function == 'd' or function == 'delete':
        print('You have chosen to delete posts.\n')
        delete_posts(session)
    elif function == 'u' or function == 'unlike':
        print('You have chosen to unlike posts.\n')
        unlike_posts(session)
    else:
        print('You have chosen to edit posts.\n')
        # TODO: Write / test edit logic

if __name__ == "__main__":
    run_session()