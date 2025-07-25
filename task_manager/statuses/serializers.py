from rest_framework import serializers
from .models import Statuses

class StatusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statuses
        fields = "__all__"