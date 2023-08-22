from rest_framework import serializers
from .models import Synchronization

class SynchronizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Synchronization
        fields = '__all__'