from django.db import models

from apps.users.models import CustomUser
from utils.base_model import BaseModel


class AuditLog(BaseModel):
    ACTION_CHOICES = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("REQUEST", "Request"),
    ]

    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        db_table = "audit_log"

    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100, null=True, blank=True)
    object_id = models.UUIDField(null=True, blank=True)
    changes = models.JSONField(null=True, blank=True)
    request_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")
