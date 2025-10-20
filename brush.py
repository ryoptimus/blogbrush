import os
import json

import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
from session import Session
from query import gather_posts, edit_posts, delete_posts, gather_q_posts, gather_likes, unlike_posts
from helpers import (
    get_blog_name, craft_blog_id, get_target, get_function, get_qparams, append_qparams_to_url
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
    elif target.lower() == 'q' or target.lower() == 'qposts':
        request_url = api_url + '/posts/queue'
    elif target.lower() == 'l' or target.lower() == 'likes':
        request_url = api_url + f'/likes?api_key={consumer_key}'
    else:
        request_url = api_url + '/posts/draft'

    return request_url

def parse_user_input(qparams, session):
    append_qparams_to_url(session, qparams)

def read_posts(session):
    posts = gather_posts(session)

    print(f'{len(posts)} post(s) acquired. Printing summaries...\n')

    i = 1
    for post in posts:
        print(f'Post {i}: {post}\n')
        # print(post)
        i += 1

def read_q_posts(session):
    posts = gather_q_posts(session)
    i = 1
    for post in posts:
        print(f'Post {i}: {post}\n')
        # print(post)
        i += 1

def read_likes(session):
    posts = gather_likes(session)

    print(f'Request URL: {session.request_url}')

    print(f'{len(posts)} like(s) acquired. Printing summaries...\n')

    i = 1
    for post in posts:
        print(f'Post {i}: {post}\n')
        # print(post)
        i += 1

def read_drafts(session):
    posts = gather_posts(session)

    print(f'{len(posts)} draft(s) acquired. Printing summaries...\n')

    i = 1
    for post in posts:
        print(f'Post {i}: {post}\n')
        # print(post)
        i += 1

def session_instance_run(blog_name, oauth):
    if blog_name is None:
        blog_name = get_blog_name()
    else:
        valid_user_input = False
        while not valid_user_input:
            user_input = input(f'Target blog name is currently \'{blog_name}\'. Please confirm (y/n): ')
            if user_input.lower() == 'y':
                valid_user_input = True
            elif user_input.lower() == 'n':
                valid_user_input = True
                blog_name = get_blog_name()
            else:
                print('Invalid input. Try again.')

    target = get_target()
    function = get_function(target)
    qparams = get_qparams(target)
    blog_identifier = craft_blog_id(blog_name)
    request_url = form_request_url(blog_identifier, target)

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
        elif target == 'q' or target == 'qposts':
            print('Let\'s read some queued posts.')
            read_q_posts(session)
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
        edit_posts(session)

    valid_user_input = False
    while not valid_user_input:
        user_input = input('Request complete.\n\nConclude session? Your input (y/n): ')
        if user_input.lower() == 'y':
            valid_user_input = True
            session_conclude = True
        if user_input.lower() == 'n':
            print('\nGot it. Refreshing session...\n')
            valid_user_input = True
            session_conclude = False

    return blog_name, session_conclude

def session_run():
    # Create OAuth1 session
    oauth = OAuth1(
        consumer_key,
        consumer_secret,
        token,
        token_secret
    )

    blog_name = None
    session_conclude = False

    while not session_conclude:
        blog_name, session_conclude = session_instance_run(blog_name, oauth)

    print('\nSession concluded. See you next time!')

if __name__ == '__main__':
    session_run()