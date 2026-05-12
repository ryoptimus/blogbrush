
from dataclasses import dataclass
from typing import List, Dict, Any

def detect_format(p: dict):
    if isinstance(p.get('content'), list):
        return 'npf'
    if ('body' in p) or ('caption' in p):
        return 'legacy'
    return 'unknown'

@dataclass
class Post:
    id: int
    url: str
    type: str
    date: str
    timestamp: int
    summary: str
    reblog_key: str
    tags: List[str]
    format: str = 'unknown'

    @classmethod
    def get_info(cls, post: Dict[str, Any]):
        return cls(
            id = int(post['id']),    # Essential field; the rest are optional, so use get()
            url = post.get('post_url', ''),
            type = post.get('type', ''),
            date = post.get('date', ''),
            timestamp = int(post.get('timestamp', 0)),
            summary = post.get('summary', ''),
            reblog_key = post.get('reblog_key', ''),
            tags = post.get('tags', []),
            format = detect_format(post)
        )