from rest_framework.serializers import ModelSerializer
from apps.wallet.models import Wallet

class WalletSerializer(ModelSerializer):
  class Meta:
    model = Wallet
    fields = '__all__'