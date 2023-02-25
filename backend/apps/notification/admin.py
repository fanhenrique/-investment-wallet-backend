from django.contrib import admin

from .models import Notification
from modelAdmin.modelAdmin import ModelAdmin

admin.site.register(Notification, ModelAdmin)
