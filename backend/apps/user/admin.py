from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.user.models import User


class MyUserAdmin(UserAdmin):
  
  fieldsets = (
    (_("Data"), {"fields": ("username", "password", "email", "cpf")}),
    (_("Personal info"), {"fields": ("first_name", "last_name")}),
    (_("Permissions"),
      {
        "fields": (
          "is_active",
          "is_staff",
          "is_superuser",
          "groups",
          "user_permissions",
        ),
      },
    ),
    (_("Important dates"), {"fields": ("last_login", "date_joined")}),
  )
    
  add_fieldsets = (
    (None,
      {
        "classes": ("wide",),
        "fields": ("username", "email", "cpf", "password1", "password2"),
      },
    ),
  )
  
  list_display = ("email", "username", "first_name", "last_name", "is_staff")

admin.site.register(User, MyUserAdmin)