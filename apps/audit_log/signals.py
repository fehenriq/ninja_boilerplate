import uuid
from datetime import datetime

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.audit_log.middleware import get_current_user
from apps.audit_log.models import AuditLog


def build_changes(sender, instance) -> dict:
    changes = {}
    for field in sender._meta.fields:
        value = getattr(instance, field.name)

        if isinstance(value, uuid.UUID):
            value = str(value)

        if isinstance(field, models.ManyToManyField):
            value = [str(obj) for obj in value.all()]

        if isinstance(field, models.OneToOneField):
            value = str(value) if value else None

        if isinstance(field, models.ImageField):
            value = str(value)

        if isinstance(field, models.ForeignKey):
            value = str(value)

        if isinstance(value, datetime):
            value = value.isoformat()
        changes[field.name] = value
    return changes


@receiver(post_save)
def log_create_or_update(sender, instance, created, **kwargs):
    if "migrations" in sender.__module__:
        return
    try:
        user_id = get_current_user() or instance.id
    except:
        user_id = None
    if user_id and sender != AuditLog:
        action = "CREATE" if created else "UPDATE"
        AuditLog.objects.create(
            user_id=user_id,
            action=action,
            model_name=sender.__name__,
            object_id=instance.pk,
            changes=build_changes(sender, instance),
        )


@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if "migrations" in sender.__module__:
        return

    try:
        user_id = get_current_user() or instance.id
    except:
        user_id = None
    if user_id and sender != AuditLog:
        AuditLog.objects.create(
            user_id=user_id,
            action="DELETE",
            model_name=sender.__name__,
            object_id=instance.pk,
            changes=build_changes(sender, instance),
        )
