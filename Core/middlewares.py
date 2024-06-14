import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        current_time = datetime.datetime.now()
        last_activity_str = request.session.get('last_activity')
        last_activity = datetime.datetime.fromisoformat(last_activity_str) if last_activity_str else current_time

        if (current_time - last_activity).seconds > settings.SESSION_COOKIE_AGE:
            logout(request)
        else:
            request.session['last_activity'] = current_time.isoformat()
