import os
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
from typing import Optional
from blogbrush.instance import Instance
from blogbrush.helpers import (
    get_blog_name, craft_blog_id, get_target, get_function, get_qparams
)

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
token = os.getenv('TOKEN')
token_secret = os.getenv('TOKEN_SECRET')

API_BASE = 'https://api.tumblr.com'
API_VERSION = 'v2'

def form_request_url(blog_id, target):
    # Construct the API URL
    api_url = f'{API_BASE}/{API_VERSION}/blog/{blog_id}'
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

def session_instance_create(blogname, oauth):
    if blogname is None:
        blogname = get_blog_name()
    else:
        valid_user_input = False
        while not valid_user_input:
            user_input = input(f'Target blog name is currently \'{blogname}\'! Please confirm (y/n): ')
            if user_input.lower() == 'y':
                valid_user_input = True
            elif user_input.lower() == 'n':
                valid_user_input = True
                blogname = get_blog_name()
            else:
                print('Invalid input. Try again.')

    target, function, qparams = get_instance_details()
    blog_id = craft_blog_id(blogname)
    request_url = form_request_url(blog_id, target)

    instance: Instance = Instance(
        blog_identifier = blog_id,
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

    return blogname, session_conclude

def session_run():
    # Create OAuth1 session
    oauth = OAuth1(
        consumer_key,
        consumer_secret,
        token,
        token_secret
    )

    blogname: Optional[str] = None
    session_conclude: bool = False

    while not session_conclude:
        blogname, session_conclude = session_instance_create(blogname, oauth)

    print('\nSession concluded. See you next time!')

if __name__ == '__main__':
    session_run()