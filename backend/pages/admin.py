from django.contrib import admin
from pages.models import Page, PageFollower

admin.site.register((Page, PageFollower))
