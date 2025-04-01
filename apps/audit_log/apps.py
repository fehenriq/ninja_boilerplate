from django.apps import AppConfig


class AuditLogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.audit_log"

    def ready(self):
        import apps.audit_log.signals
