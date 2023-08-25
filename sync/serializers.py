from rest_framework import serializers
from .models import Commentator

class CommentatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentator
        fields = '__all__'