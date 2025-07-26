import time
from django.core.cache import cache
class RequestCounterMiddleware: 
    def __init__(self, get_response): 
        self.get_response = get_response

    def __call__(self, request):
        now = int(time.time())  # current UNIX timestamp (seconds)
        key = f'req_count: {now}'
        current = cache.get(key, 0)
        cache.set(key, current + 1, timeout=120)  # store count for 2 mins
        return self.get_response(request)