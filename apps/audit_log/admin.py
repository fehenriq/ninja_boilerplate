from django.contrib import admin

from apps.audit_log.models import AuditLog


class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["user", "full_name", "action", "model_name", "created_at"]
    search_fields = ["user__email", "model_name", "object_id"]
    list_filter = ["action", "model_name", "created_at"]
    readonly_fields = [
        "user",
        "action",
        "model_name",
        "object_id",
        "changes",
        "request_data",
        "created_at",
    ]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    def full_name(self, obj):
        return obj.user.name if obj.user else "-"

    full_name.short_description = "Name"


admin.site.register(AuditLog, AuditLogAdmin)
