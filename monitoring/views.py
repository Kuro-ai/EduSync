from django.http import JsonResponse
from django.views.decorators.cache import never_cache 
from django.core.cache import cache
import time
@never_cache
def request_count_api(request):
    now = int(time.time())
    #Return the last 60 seconds of request counts
    counts = [cache.get(f'req_count_{now - i}', 0) for i in range(60)] 
    return JsonResponse({
    "requests_per_second": counts[::-1] # oldest first
    })