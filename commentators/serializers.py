from rest_framework import serializers
from .models import Commentator

class CommentatorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    game = serializers.StringRelatedField()
    
    class Meta:
        model = Commentator
        fields = '__all__'