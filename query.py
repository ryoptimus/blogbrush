import requests

# GET function for posts and drafts
def posts_get(session):
    # Get posts / drafts
    print(f'[query_posts_get] Request URL: {session.request_url}')
    try:
        response = requests.get(session.request_url, auth=session.oauth)
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

# GET function for likes   
def likes_get(session):
    # Get likes
    try:
        response = requests.get(session.request_url, auth=session.oauth)
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