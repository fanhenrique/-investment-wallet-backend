from django.db import models
from guardian.shortcuts import assign_perm

from apps.user.models import User

class Notification(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  title = models.CharField(max_length=100, blank=False)
  description = models.CharField(max_length=256, default='', blank=True)
  create_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    super(Notification, self).save(*args, **kwargs)
    for permission in [
      'notification.add_notification',
      'notification.change_notification',
      'notification.view_notification',
      'notification.delete_notification'
    ]:
      assign_perm(permission, self.user, self)