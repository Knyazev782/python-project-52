from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Statuses
from .serializers import StatusesSerializer
from .permission import IsOwner


class StatusesAPIList(generics.ListAPIView):
    queryset = Statuses.objects.all()
    serializer_class = StatusesSerializer
    permission_classes = [IsAuthenticated]

class StatusesAPIUpdate(generics.UpdateAPIView):
    queryset = Statuses.objects.all()
    serializer_class = StatusesSerializer
    permission_classes = [IsAdminUser]

class StatusesAPIDestroy(generics.DestroyAPIView):
    queryset = Statuses.objects.all()
    serializer_class = StatusesSerializer
    permission_classes = [IsOwner]
