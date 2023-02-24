from django.contrib import admin
from .models import Wallet

from modelAdmin.modelAdmin import ModelAdmin

admin.site.register(Wallet, ModelAdmin)
