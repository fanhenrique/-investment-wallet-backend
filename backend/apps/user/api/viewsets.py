from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

import guardian.shortcuts as guardian

from apps.user.models import User
from apps.user.api.serializers import UserSerializer
from apps.wallet.api.serializers import WalletSerializer
from apps.notification.api.serializers import NotificationSerializer
from apps.active.api.serializers import ActiveSerializer

class UserViewSet(ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  
  permission_classes = (IsAuthenticated,)

  def pagination(self, queryset):
    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)

  def set_queryset(self, token, permission, serializer):
    
    user = Token.objects.get(key=token).user

    queryset = self.filter_queryset(guardian.get_objects_for_user(user, permission))
  
    self.serializer_class = serializer

    return queryset

  @action(detail=False, methods=['get'])
  def wallets(self, request, *args, **kwargs):
    return self.pagination(self.set_queryset(request.auth, 'wallet.view_wallet', WalletSerializer))

  @action(detail=False, methods=['get'])
  def notifications(self, request, *args, **kwargs):
    return self.pagination(self.set_queryset(request.auth, 'nofitication.view_notification', NotificationSerializer))
  
  @action(detail=False, methods=['get'])
  def actives(self, request, *args, **kwargs):

    if self.request.data:
      try: 
        user = Token.objects.get(key=request.auth).user
        wallet = guardian.get_objects_for_user(user, 'wallet.view_wallet').filter(id=self.request.data['id_wallet']).last()
        actives = wallet.active_set.all()
        self.serializer_class = ActiveSerializer
      except:
        return Response(data={"detail": 'Use "id_wallet" to inform the wallet'}, status=status.HTTP_400_BAD_REQUEST)
      return self.pagination(actives)

    else:
      return self.pagination(self.set_queryset(request.auth, 'active.view_active', ActiveSerializer))
