from django.db import models
from django.core.validators import MinValueValidator

from guardian.shortcuts import assign_perm

# from apps.wallet.models import Wallet

class Active(models.Model):
  wallet = models.ForeignKey("wallet.Wallet", on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=100, blank=False)
  data_purchase = models.DateField()
  institution = models.CharField(max_length=100, default='', blank=True)
  amount = models.IntegerField(default=0, validators=[MinValueValidator(0)], blank=False)
  price_paid = models.DecimalField(default=0.0, validators=[MinValueValidator(0.0)], max_digits=20, decimal_places=2, blank=False)
  invested_price = models.DecimalField(default=0.0, validators=[MinValueValidator(0.0)], max_digits=20, decimal_places=2, blank=False)
  # TODO rever taxa de corretagem
  brokerage_rate = models.DecimalField(default=0.0, validators=[MinValueValidator(0.0)], max_digits=20, decimal_places=2, blank=True)
  create_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    super(Active, self).save(*args, **kwargs)
    for permission in [
      'active.add_active',
      'active.change_active',
      'active.view_active',
      'active.delete_active',
    ]:
      assign_perm(permission, self.wallet.user, self)