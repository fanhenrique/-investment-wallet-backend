from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.notification.api.serializers import NotificationSerializer
from apps.notification.models import Notification

class NotificationViewSet(ModelViewSet):
  queryset = Notification.objects.all()
  serializer_class = NotificationSerializer

  permission_classes = (IsAuthenticated,)
