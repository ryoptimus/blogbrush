from dataclasses import dataclass, field
from typing import Dict, List
from requests_oauthlib import OAuth1

# API_BASE = 'https://api.tumblr.com'
# API_VERSION = 'v2'

@dataclass
class Session:
    blog_identifier: str    # Required
    request_url: str
    oauth: OAuth1   # Required (for now)
    target: str = 'posts'   # Set a default
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
    
    def get_limit(self):
        limit = self.params.get('limit')
        if limit:
            return int(limit)
        else:
            return None
        
    def get_before(self):
        before = self.params.get('before')
        if before:
            return before
        else:
            return None
    
    def get_after(self):
        after = self.params.get('after')
        if after:
            return after
        else:
            return None
    
    def get_type(self):
        type = self.params.get('type')
        if type:
            return type
        else:
            return None
    
    def get_tags(self):
        tags = self.params.get('tags')
        if tags:
            return tags
        else:
            return None
        
    def get_offset(self):
        offset = self.params.get('offset')
        if offset:
            return offset
        else:
            return None