from dataclasses import dataclass, field
from typing import Dict, List
from requests_oauthlib import OAuth1
from helpers import append_qparams_to_url
from query import read_posts, read_drafts, edit_posts, delete_posts, read_q_posts, read_likes, unlike_posts

# API_BASE = 'https://api.tumblr.com'
# API_VERSION = 'v2'

@dataclass
class Instance:
    blog_identifier: str    # Required
    request_url: str
    oauth: OAuth1   # Required (for now)
    target: str = 'posts'   # Set a default
    function: str = 'read'
    params: Dict[str, object] = field(default_factory=dict)

    def set_limit(self, limit: int):
        self.params['limit'] = limit
        return self
    
    def set_before(self, timestamp: int):
        self.params['before'] = timestamp
        return self
    
    def set_after(self, timestamp: int):
        self.params['after'] = timestamp
        return self
    
    def set_type(self, type: str):
        self.params['type'] = type
        return self
    
    def set_tags(self, tags: List[str]):
        self.params['tags'] = tags
        return self
    
    def set_offset(self, offset: int):
        self.params['offset'] = offset
        return self
    
    def get_param(self, param_name: str):
        param = self.params.get(param_name)
        if param:
            return param
        else:
            return None
        
    def run(self, qparams):
        append_qparams_to_url(self, qparams)

        if self.function == 'r' or self.function == 'read':
            if self.target == 'p' or self.target == 'posts':
                print('You have chosen to read posts.\n')
                read_posts(self)
            elif self.target == 'q' or self.target == 'qposts':
                print('Let\'s read some queued posts.')
                read_q_posts(self)
            elif self.target == 'l' or self.target == 'likes':
                print('You have chosen to read likes.\n')
                read_likes(self)
            else:
                # print('You have chosen to read drafts.')
                read_drafts(self)
        elif self.function == 'd' or self.function == 'delete':
            print('You have chosen to delete posts.\n')
            delete_posts(self)
        elif self.function == 'u' or self.function == 'unlike':
            print('You have chosen to unlike posts.\n')
            unlike_posts(self)
        else:
            print('You have chosen to edit posts.\n')
            edit_posts(self)