from django.db import models

from guardian.shortcuts import assign_perm, remove_perm, get_perms

from apps.user.models import User

permissions = [
  'wallet.view_wallet',
  'wallet.change_wallet',
  'wallet.delete_wallet',
]

class Wallet(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=100, blank=False)
  description = models.CharField(max_length=256, default='', blank=True)
  create_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    
    if self.pk:
      previous = Wallet.objects.get(pk=self.pk)
      if 'change_wallet' in get_perms(previous.user, self):
        for permission in permissions: 
          remove_perm(permission, previous.user, self)
    
    super(Wallet, self).save(*args, **kwargs)
    
    for permission in permissions: 
      assign_perm(permission, self.user, self)  
