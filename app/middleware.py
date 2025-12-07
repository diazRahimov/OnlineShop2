import time
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

class AutoLogoutMiddleware:
    """
    Session orqali ishlaydigan oddiy auto-logout middleware.
    last_activity sessiyada int(timestamp) shaklida saqlanadi.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout = getattr(settings, "AUTO_LOGOUT_TIMEOUT", 600)

    def __call__(self, request):
        if request.user.is_authenticated:
            now = int(time.time())
            last = request.session.get('last_activity')

            if last:
                elapsed = now - int(last)
                if elapsed > self.timeout:
                    logout(request)
                    try:
                        del request.session['last_activity']
                    except KeyError:
                        pass
                    return redirect('user:login_page')

            request.session['last_activity'] = now

        response = self.get_response(request)
        return response
