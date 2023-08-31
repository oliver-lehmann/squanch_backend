from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Game
from .serializers import GameSerializer

# Create your views here.

# add new datapoint
@api_view(['PUT'])
def setGameStart(request):
    game_name = request.data["name"]
    game = get_object_or_404(Game, name=game_name)
    serializer = GameSerializer(instance=game, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)
