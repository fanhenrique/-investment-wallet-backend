from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.wallet.api.serializers import WalletSerializer
from apps.wallet.models import Wallet

class WalletViewSet(ModelViewSet):
  queryset = Wallet.objects.all()
  serializer_class = WalletSerializer

  permission_classes = (IsAuthenticated, )