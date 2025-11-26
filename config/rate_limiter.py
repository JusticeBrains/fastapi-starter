from collections import defaultdict
from datetime import datetime, timedelta
from config.env import REQUESTS_PER_MINUTE


class RateLimiter:
    def __init__(self, request_per_minute: int = REQUESTS_PER_MINUTE):
        self.request_per_minute = request_per_minute
        self.requests = defaultdict(list)

    def is_rate_limited(self, token: str) -> bool:
        now = datetime.now()
        minutes_ago = now - timedelta(minutes=1)

        self.requests[token] = [
            request for request in self.requests[token] if request > minutes_ago
        ]

        if len(self.requests[token]) >= self.request_per_minute:
            return True

        self.requests[token].append(now)

        return False
