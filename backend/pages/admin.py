from django.contrib import admin
from .models import Page, PageFollower

admin.site.register((Page, PageFollower))
