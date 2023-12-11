from django.contrib import admin

from .models import Post, PostLike

admin.site.register((Post, PostLike))
