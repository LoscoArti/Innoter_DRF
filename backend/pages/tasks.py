from celery import shared_task
from django.utils import timezone
from pages.models import Page


@shared_task
def unblock_pages():
    Page.objects.filter(is_blocked=True, unblock_date__lte=timezone.now()).update(
        is_blocked=False
    )
