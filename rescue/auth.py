from functools import wraps

from django.conf import settings
from django.http import JsonResponse


def require_api_key(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        expected = settings.RESCUE_API_KEY

        if not expected or api_key != expected  :
            return JsonResponse(
                {"error": "unauthorized"},
                status=401
            )

        return view_func(request, *args, **kwargs)

    return wrapper