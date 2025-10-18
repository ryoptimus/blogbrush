import json
import requests
from post import Post
from helpers import append_param_to_url

# GET function for posts and drafts
def posts_get(session):
    # Get posts / drafts
    print(f'[query_posts_get] Request URL: {session.request_url}')
    try:
        response = requests.get(session.request_url, auth=session.oauth)
        if response.status_code == 429:
            print('Rate limit exceeded.')
            return
        response.raise_for_status()
        
    except requests.exceptions.RequestException as error:
        print(f'Error: {error}')

    # Parse JSON
    try:
        data = response.json()
        # print(json.dumps(data['response']['posts'], indent=2))
        return data
    except ValueError as error:
        print(f'Error parsing JSON: {error}')
        return
    
def gather_posts(session):
    data = posts_get(session)

    if not data:
        return []

    posts = []
    seen_ids = set()
    for p in data['response']['posts']:
        post = Post.get_info(p)
        if post.id not in seen_ids:
            posts.append(post)
            seen_ids.add(post.id)

    limit = session.get_param('limit')
    if limit and limit > 20:
        print('[gather_posts] Greedy. Want more posts, do you?\n')
        remaining_count = limit - 20
        print(f'[gather_posts] Looks like... {remaining_count} more, hm?')
        while remaining_count > 0:
            last_post = posts[-1]
            append_param_to_url(session, 'before', last_post.timestamp)
            if remaining_count > 20:
                append_param_to_url(session, 'limit', 20)
                data = posts_get(session)
                print(f'[gather_posts] Posts returned from call: {len(data['response']['posts'])}')
                for p in data['response']['posts']:
                    post = Post.get_info(p)
                    if post.id not in seen_ids:
                        posts.append(post)
                        seen_ids.add(post.id)
                if len(data['response']['posts']) < 20:
                    print('[gather_posts] No more posts found. Setting remaining count to zero.')
                    remaining_count = 0
                else:
                    remaining_count -= 20
            else:
                append_param_to_url(session, 'limit', remaining_count)
                data = posts_get(session)
                print(f'[gather_posts] Posts returned from call: {len(data['response']['posts'])}')
                for p in data['response']['posts']:
                    post = Post.get_info(p)
                    if post.id not in seen_ids:
                        posts.append(post)
                        seen_ids.add(post.id)

                remaining_count = 0
    print(f'[gather_posts] seen_ids set has {len(seen_ids)} elements.')
    if session.target.lower() == 'p' or session.target.lower() == 'posts':
        target = 'post'
    else:
        target = 'draft'
    if len(posts) != limit:
        print(f'Despite the provided limit of {limit}, only {len(posts)} {target}(s) were found.\n')
    else:
        print(f'{limit} {target}(s) successfully found!\n')
    return posts

def q_posts_get(session):
    try:
        response = requests.get(session.request_url, auth=session.oauth)
        if response.status_code == 429:
            print('Rate limit exceeded.')
            return
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(f'Error: {error}')

    # Parse JSON
    try:
        data = response.json()
        # print(json.dumps(data['response'], indent=2))
        return data
    except ValueError as error:
        print(f'Error parsing JSON: {error}')
        return

def gather_q_posts(session):
    data = q_posts_get(session)

    if not data:
        return []
    
    posts = []
    seen_ids = set()
    for p in data['response']['posts']:
        post = Post.get_info(p)
        if post.id not in seen_ids:
            posts.append(post)
            seen_ids.add(post.id)

    offset = session.get_param('offset')
    if not offset:
        offset = 0
    limit = session.get_param('limit')
    if limit and limit > 20:
        print('[gather_q_posts] Greedy. Want more posts, do you?\n')
        remaining_count = limit - 20
        print(f'[gather_q_posts] Looks like... {remaining_count} more, hm?')
        while remaining_count > 0:
            offset = len(posts)
            append_param_to_url(session, 'offset', offset)
            print(f'Offset is now {offset}.')
            if remaining_count > 20:
                append_param_to_url(session, 'limit', 20)
                data = q_posts_get(session)
                print(f'[gather_q_posts] Posts returned from call: {len(data['response']['posts'])}')
                for p in data['response']['posts']:
                    post = Post.get_info(p)
                    if post.id not in seen_ids:
                        posts.append(post)
                        seen_ids.add(post.id)
                if len(data['response']['posts']) < 20:
                    print('[gather_q_posts] No more posts found. Setting remaining count to zero.')
                    remaining_count = 0
                else:
                    remaining_count -= 20
            else:
                append_param_to_url(session, 'limit', remaining_count)
                data = q_posts_get(session)
                print(f'[gather_q_posts] Posts returned from call: {len(data['response']['posts'])}')
                for p in data['response']['posts']:
                    post = Post.get_info(p)
                    if post.id not in seen_ids:
                        posts.append(post)
                        seen_ids.add(post.id)

                remaining_count = 0
    
    if len(posts) != limit:
        print(f'Despite provided limit of {limit}, only {len(posts)} queued post(s) were found.\n')
    else:
        print(f'{limit} queued post(s) successfully found!\n')

    # print(f'[gather_q_posts] posts list has {len(posts)} elements.')
    # print(f'[gather_q_posts] seen_ids set has {len(seen_ids)} elements.')
    return posts

# GET function for likes   
def likes_get(session):
    # Get likes
    try:
        response = requests.get(session.request_url, auth=session.oauth)
        if response.status_code == 429:
            print('Rate limit exceeded.')
            return
        response.raise_for_status()
        
    except requests.exceptions.RequestException as error:
        print(f'Error: {error}')

    # Parse JSON
    try:
        data = response.json()
        # print(json.dumps(data['response']['liked_posts'], indent=2))
        return data
    except ValueError as error:
        print(f'Error parsing JSON: {error}')
        return
    
def gather_likes(session):
    data = likes_get(session)

    if not data:
        return []

    posts = []
    seen_ids = set()
    for p in data['response']['liked_posts']:
        post = Post.get_info(p)
        posts.append(post)
        seen_ids.add(post.id)

    limit = session.get_param('limit')
    if limit and limit > 20:
        print('[gather_likes] Greedy. Want more posts, do you?\n')
        remaining_count = limit - 20
        print(f'[gather_likes] Looks like... {remaining_count} more, hm?')
        while remaining_count > 0:
            last_post = posts[-1]
            append_param_to_url(session, 'before', last_post.timestamp)
            if remaining_count > 20:
                append_param_to_url(session, 'limit', 20)
                data = posts_get(session)
                print(f'[gather_likes] Posts returned from call: {len(data['response']['posts'])}')
                for p in data['response']['liked_posts']:
                    post = Post.get_info(p)
                    if post.id not in seen_ids:
                        posts.append(post)
                        seen_ids.add(post.id)
                if len(data['response']['liked_posts']) < 20:
                    print('[gather_likes] No more posts found. Setting remaining count to zero.')
                    remaining_count = 0
                else:
                    remaining_count -= 20
            else:
                append_param_to_url(session, 'limit', remaining_count)
                data = posts_get(session)
                print(f'[gather_likes] Posts returned from call: {len(data['response']['liked_posts'])}')
                for p in data['response']['liked_posts']:
                    post = Post.get_info(p)
                    if post.id not in seen_ids:
                        posts.append(post)
                        seen_ids.add(post.id)

                remaining_count = 0
    print(f'[gather_likes] seen_ids set has {len(seen_ids)} elements.')
    if len(posts) != limit:
        print(f'Despite provided limit of {limit}, only {len(posts)} liked posts were found.\n')
    else:
        print(f'{limit} liked post(s) successfully found!\n')
    return posts

def edit_post_legacy(session, post, new_tags):
    edit_url = f'https://api.tumblr.com/v2/blog/{session.blog_identifier}/post/edit'

    payload = {
        'id': post.id, 
        'tags': ','.join(new_tags)
    }
    try:
        edit_response = requests.post(edit_url, auth=session.oauth, data=payload)
        if edit_response.status_code == 429:
            print('Rate limit exceeded.')
            return
        edit_response.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(f'Error editing post {post.id}: {error}')
    print(f'Post {post.id} edited successfully.\n(status: {edit_response.json()['meta']['status']}, msg: {edit_response.json()['meta']['msg']})\n')
 
def edit_post_npf(session, post, new_tags):
    edit_url = f'https://api.tumblr.com/v2/blog/{session.blog_identifier}/posts/{post.id}'
    payload = {
        'tags': new_tags,
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        edit_response = requests.put(edit_url, auth=session.oauth, json=payload, headers=headers)
        if edit_response.status_code == 429:
            print('Rate limit exceeded.')
            return
        edit_response.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(f'Error editing post {post.id}: {error}')
    
    print(f'Post {post.id} edited successfully.\n(status: {edit_response.json()['meta']['status']}, msg: {edit_response.json()['meta']['msg']})\n')