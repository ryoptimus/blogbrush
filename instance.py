import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional
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
    started: bool = False
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    stats: Dict[str, object] = field(default_factory=dict)

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
        
    def start_timer(self):
        self.started = True
        self.start_time = time.time()
    
    def init_stats(self):
        self.stats['calls'] = 0
        self.stats['errors'] = 0
        self.stats['time'] = 0.0
        self.stats['fetched'] = 0
        self.stats['read'] = 0
        self.stats['unliked'] = 0
        self.stats['deleted'] = 0
        self.stats['edited'] = 0
    
    def print_stats(self):
        api_calls = self.stats['calls']
        error_count = self.stats['errors']
        time_elapsed = self.stats['time']
        posts_fetched = self.stats['fetched']

        instance_summary = f'INSTANCE SUMMARY\n' \
        '------------------------\n' \
        f'API calls: {api_calls}\n' \
        f'Errors: {error_count}\n' \
        f'Time elapsed (s): {time_elapsed:.2f}\n' \
        '------------------------\n' \
        f'Posts fetched: {posts_fetched}\n'

        if self.stats['read'] != 0:
            instance_summary += f'Posts read: {self.stats['read']}\n'
        if self.stats['unliked'] != 0:
            instance_summary += f'Posts unliked: {self.stats['unliked']}\n'
        if self.stats['deleted'] != 0:
            instance_summary += f'Posts deleted: {self.stats['deleted']}\n'
        if self.stats['edited'] != 0:
            instance_summary += f'Posts edited: {self.stats['edited']}\n'

        print(instance_summary)
        
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
        
        self.end_time = time.time()
        self.stats['time'] = self.end_time - self.start_time