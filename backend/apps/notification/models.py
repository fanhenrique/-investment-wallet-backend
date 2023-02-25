from django.db import models

from guardian.shortcuts import assign_perm, get_perms, remove_perm

from apps.user.models import User

permissions = [
  'notification.view_notification',
  'notification.change_notification',
  'notification.delete_notification'
]

class Notification(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  title = models.CharField(max_length=100, blank=False)
  description = models.CharField(max_length=256, default='', blank=True)
  create_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):

    if self.pk:
      previous = Notification.objects.get(pk=self.pk)
      if 'change_notification' in get_perms(previous.user, self):
        for permission in permissions:
          remove_perm(permission, previous.user, self)

    super(Notification, self).save(*args, **kwargs)

    for permission in permissions:
      assign_perm(permission, self.user, self)