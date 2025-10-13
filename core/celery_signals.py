import requests
from celery.signals import task_failure
from django.conf import settings


@task_failure.connect
def notify_task_failure(
    sender, task_id, exception, args, kwargs, _traceback, einfo, **_
):
    if not (webhook_url := getattr(settings, "GOOGLE_CHAT_WEBHOOK_URL")):
        print("⚠️ Webhook do Google Chat não configurado no settings.")
        return

    message = {
        "cards": [
            {
                "header": {
                    "title": f"❌ Falha definitiva na task Celery: {sender.name}",
                    "subtitle": str(exception),
                },
                "sections": [
                    {
                        "widgets": [
                            {
                                "textParagraph": {
                                    "text": f"Task ID: {task_id}<br>"
                                    f"Args: {args}<br>"
                                    f"Kwargs: {kwargs}<br>"
                                    f"Traceback:<br><pre>{einfo}</pre>"
                                }
                            }
                        ]
                    }
                ],
            }
        ]
    }
    try:
        requests.post(
            webhook_url,
            json=message,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
    except Exception:
        pass
