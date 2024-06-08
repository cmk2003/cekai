import time

from django.http import JsonResponse

from cekai import settings
from test_user import models

def login_auth(view_func):
    def inner(request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or token == "null":
            return JsonResponse({},status=401)

        obj = models.UserToken.objects.filter(token=token).first()
        if not obj:
            return JsonResponse({},status=401)

        update_time = int(obj.update_time.timestamp())
        current_time = int(time.time())
        if current_time - update_time >= settings.INVALID_TIME:
            return JsonResponse({}, status=401)
        return view_func(request, *args, **kwargs)
    return inner