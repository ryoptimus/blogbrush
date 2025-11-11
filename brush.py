import os
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
from instance import Instance
from helpers import (
    get_blog_name, craft_blog_id, get_target, get_function, get_qparams
)

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
token = os.getenv('TOKEN')
token_secret = os.getenv('TOKEN_SECRET')

API_BASE = 'https://api.tumblr.com'
API_VERSION = 'v2'

def form_request_url(blog_identifier, target):
    # Construct the API URL
    api_url = f'{API_BASE}/{API_VERSION}/blog/{blog_identifier}'
    if target.lower() == 'p' or target.lower() == 'posts':
        request_url = api_url + '/posts'
    elif target.lower() == 'q' or target.lower() == 'qposts':
        request_url = api_url + '/posts/queue'
    elif target.lower() == 'l' or target.lower() == 'likes':
        request_url = api_url + f'/likes?api_key={consumer_key}'
    else:
        request_url = api_url + '/posts/draft'

    return request_url

def get_instance_details():
    target = get_target()
    function = get_function(target)
    qparams = get_qparams(target)

    return target, function, qparams

def session_instance_create(blog_name, oauth):
    if blog_name is None:
        blog_name = get_blog_name()
    else:
        valid_user_input = False
        while not valid_user_input:
            user_input = input(f'Target blog name is currently \'{blog_name}\'! Please confirm (y/n): ')
            if user_input.lower() == 'y':
                valid_user_input = True
            elif user_input.lower() == 'n':
                valid_user_input = True
                blog_name = get_blog_name()
            else:
                print('Invalid input. Try again.')

    target, function, qparams = get_instance_details()
    blog_identifier = craft_blog_id(blog_name)
    request_url = form_request_url(blog_identifier, target)

    instance = Instance(
        blog_identifier = blog_identifier,
        request_url = request_url,
        oauth = oauth,
        target = target,
        function = function
    )

    instance.run(qparams)

    valid_user_input = False
    while not valid_user_input:
        user_input = input('Conclude session? Your input (y/n): ')
        if user_input.lower() == 'y':
            valid_user_input = True
            session_conclude = True
        elif user_input.lower() == 'n':
            print('\nGot it. Refreshing session...\n')
            valid_user_input = True
            session_conclude = False
        else:
            print('\tError: Invalid input.\n')

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
        blog_name, session_conclude = session_instance_create(blog_name, oauth)

    print('\nSession concluded. See you next time!')

if __name__ == '__main__':
    session_run()