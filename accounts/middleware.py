from django.shortcuts import redirect
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth import logout

class TimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and user.is_timed_out():
            logout(request)
            timeout_time = user.timeout_until.strftime("%Y-%m-%d %H:%M:%S")
            messages.error(
                request,
                f"You've been timeout until {timeout_time} by admin. "
                "If you're wrongfully timeout, contact the admin at kmh61030@gmail.com"
            )
            return redirect("login")
        return self.get_response(request)
