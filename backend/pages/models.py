import uuid

from django.db import models
from tags.models import Tag


class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user_id = models.UUIDField()
    user_group_id = models.UUIDField(null=True)
    image_url = models.URLField(blank=True)
    tags = models.ManyToManyField(Tag, related_name="pages")
    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PageFollower(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="page_followers"
    )
    user_id = models.UUIDField()
