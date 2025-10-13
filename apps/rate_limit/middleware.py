from django.core.cache import cache
from django.http import JsonResponse


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = 5
        self.timeout = 60

    def __call__(self, request):
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            identity = auth.split(" ")[1]
        elif auth:
            identity = auth
        else:
            identity = request.META.get("REMOTE_ADDR") or "unknown"

        path = request.get_full_path()
        key = f"rl:{identity}:{path}"
        count_key = f"{key}:count"
        timer_key = f"{key}:timer"

        if not cache.add(count_key, 1, timeout=self.timeout):
            count = cache.incr(count_key)
        else:
            count = 1
            cache.set(timer_key, True, timeout=self.timeout)

        if count > self.limit:
            retry_after = (
                getattr(cache, "ttl", lambda key: None)(timer_key) or self.timeout
            )
            return JsonResponse(
                {"detail": "Muitas requisições, tente novamente em breve."},
                status=429,
                headers={"Retry-After": str(retry_after)},
            )

        return self.get_response(request)
