import os
import json

import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
token = os.getenv('TOKEN')
token_secret = os.getenv('TOKEN_SECRET')

# Get blog name from user
blog_name = input('Enter blog name: ')

if blog_name.endswith('.tumblr.com'):
    blog_name = blog_name.split('.')[0]

# Construct the API URL
api_url = f'https://api.tumblr.com/v2/blog/{blog_name}.tumblr.com'

target = 'x'
targets = ['p', 'posts', 'l', 'likes', 'd', 'drafts']

while target.lower() not in targets:
    target = input('What do you want to see?\n\tFor posts, type p or posts.\n\tFor likes, type l or likes.\n\tFor drafts, type d or drafts.')

if target.lower() == 'p' or target.lower() == 'posts':
    print('You have chosen posts.')
    request_url = api_url + '/posts'
elif target.lower() == 'l' or target.lower() == 'likes':
    print('You have chosen likes.')
else:
    print('You have chosen drafts.')

# Create OAuth1 session
oauth = OAuth1(
    consumer_key,
    consumer_secret,
    token,
    token_secret
)

try:
    response = requests.get(request_url, auth=oauth)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data['response'], indent=2))
except requests.exceptions.RequestException as error:
    print(f"Error: {error}")