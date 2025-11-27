from collections import defaultdict
from datetime import datetime

from ua_parser.user_agent_parser import Parse
from fastapi import Request


class UserIdentifer:
    def __init__(self):
        self.user_info = defaultdict(list)

    async def get_client_ip(self, request: Request):
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    async def get_user_device(self, request: Request):
        user_agent = request.headers.get("User-Agent", "unknown")
        ua = Parse(user_agent)
        browser = ua["user_agent"]["family"]
        os = ua["os"]["family"]
        device = ua["device"]["family"]
        return f"{browser} on {os} ({device})"

    async def user_activity(self, username: str, ip: str, device: str):
        current_time = datetime.now()
        activity = {
            "username": username,
            "ip": ip,
            "device": device,
            "ip_changed": False,
            "device_changed": False,
            "last_seen": current_time.isoformat(),
            "timestamp": current_time.isoformat(),
        }
        if username not in self.user_info:
            self.user_info[username] = [activity]
            return

        # Check if IP or device has changed
        user_data = self.user_info[username]
        ip_changed = user_data[-1]["ip"] != ip
        device_changed = user_data[-1]["device"] != device
        if ip_changed:
            activity["ip_changed"] = True
        if device_changed:
            activity["device_changed"] = True

        self.user_info[username].append(activity)
        return activity
