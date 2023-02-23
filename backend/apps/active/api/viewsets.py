from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.active.api.serializers import ActiveSerializer
from apps.active.models import Active

class ActiveViewSet(ModelViewSet):
  queryset = Active.objects.all()
  serializer_class = ActiveSerializer

  permission_classes = (IsAuthenticated, )