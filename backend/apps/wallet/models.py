from django.db import models

from guardian.shortcuts import assign_perm

from apps.user.models import User

class Wallet(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=100, blank=False)
  description = models.CharField(max_length=256, default='', blank=True)
  create_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    super(Wallet, self).save(*args, **kwargs)
    for permission in [
      'wallet.add_wallet',
      'wallet.change_wallet',
      'wallet.view_wallet',
      'wallet.delete_wallet',
    ]:
      assign_perm(permission, self.user, self)  
