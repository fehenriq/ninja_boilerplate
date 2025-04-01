import json
import threading

from utils.jwt import check_jwt_token

_thread_locals = threading.local()


def get_current_user():
    if not (data := getattr(_thread_locals, "user", None)):
        return None

    return data.get("user_id")


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.user = self.get_user_from_token(request)
        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def _get_request_data(self, request):
        request_data = {
            "method": request.method,
            "path": request.get_full_path(),
            "params": request.GET.dict(),
            "body": self._get_body(request),
            "client_ip": self.get_client_ip(request),
        }
        return request_data

    def _get_body(self, request):
        try:
            if request.body:
                return json.loads(request.body.decode("utf-8"))
        except Exception:
            return None

    def get_user_from_token(self, request):
        try:
            if not (auth_header := request.headers.get("Authorization")):
                return None

            return check_jwt_token(auth_header)
        except Exception:
            return None

    def save_request_log(self, request_data):
        from audit_log.models import AuditLog

        user_id = get_current_user()
        if user_id:
            AuditLog.objects.create(
                user_id=user_id,
                action="REQUEST",
                model_name="RequestLog",
                object_id=None,
                changes=None,
                request_data=request_data,
            )
