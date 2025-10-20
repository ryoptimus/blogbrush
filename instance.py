from dataclasses import dataclass, field
from typing import Dict, List
from requests_oauthlib import OAuth1

# API_BASE = 'https://api.tumblr.com'
# API_VERSION = 'v2'

@dataclass
class Instance:
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
    
    def get_param(self, param_name: str):
        param = self.params.get(param_name)
        if param:
            return param
        else:
            return None