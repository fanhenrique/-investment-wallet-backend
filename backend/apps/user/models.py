from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.contrib.auth.validators import UnicodeUsernameValidator

class User(AbstractUser):
  username = models.CharField(max_length=150, validators=[UnicodeUsernameValidator()], unique=False, blank=True)
  cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
  email = models.EmailField(validators=[EmailValidator], unique=True)
  is_trusty = models.BooleanField(default=False, help_text="Designates whether this user has confirmed his account")

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'cpf']
