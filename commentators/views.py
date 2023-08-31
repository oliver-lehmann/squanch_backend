import datetime
import os
import requests

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .forms import NewComentatorForm
from .models import Commentator
from .serializers import CommentatorSerializer
from .utils import mm_ss_to_seconds
from .webhooks import handleStreamStart, handleAssetReady
from games.models import Game
from users.models import User


MUX_LS_API_URL = "https://api.mux.com/video/v1/live-streams"

# load .env file
load_dotenv()


def index(request):
    form = NewComentatorForm()
    context = {"form": form}
    return render(request, 'commentators/index.html', context)


def commentatorHome(request, commentator_id):
    commentator = get_object_or_404(Commentator, pk=commentator_id)
    context = {"commentator": commentator}
    # TODO: let the commentator choose another game
    return render(request, 'commentators/commentator_ts.html', context)


def createNewStream(request):
    user = User.objects.get(pk=request.POST["name"])
    game = Game.objects.get(pk=request.POST["game"])
    print("Name:", user.surname, "Game:", game.name)
    
    # Create new commentator object
    new_commentator = Commentator.objects.create(user=user, game=game)
    
    # Create new live stream on Mux
    data = {
        "playback_policy": [
            "public"
        ],
        "new_asset_settings": {
            "playback_policy": [
                "public"
            ]
        },
        "audio_only": True,
        "latency_mode": "low",
        "reconnect_window": 30,
        "test": True
    }
    headers = { "Content-Type": "application/json" }
    
    response = requests.post(MUX_LS_API_URL, 
                             headers=headers, 
                             json=data,
                             auth=(os.getenv('MUX_TOKEN_ID'), os.getenv('MUX_TOKEN_SECRET')))
    
    print("Response.json(): ", response.json())
    # Save stream key and playback id to database
    if response.json()["data"]:
        new_commentator.stream_key = response.json()["data"]["stream_key"]
        new_commentator.live_stream_id = response.json()["data"]["id"]
        new_commentator.save()
    
    context = { "commentator": new_commentator }
    return render(request, 'commentators/commentator_ts.html', context)


def addCommentatorOffset(request, commentator_id):
    commentator_position = mm_ss_to_seconds(request.POST["time"])
    print("Request['Time']:", request.POST["time"])
    print("Commentator position:", commentator_position)
    
    # convert submit tim to datetime object
    submit_time = datetime.datetime.fromisoformat(request.POST["submit_time"].replace('Z', '+00:00'))
    print("Submit time:", submit_time, type(submit_time))
    
    # get commentator object
    commentator = get_object_or_404(Commentator, pk=commentator_id)
    stream_started = commentator.stream_start
    print("Stream started:", stream_started, type(stream_started))
    
    offset = (submit_time - stream_started).total_seconds() - commentator_position
    print("Offset (s):", offset)
    
    # update commentator object
    commentator.game_offset = offset
    commentator.save()
    
    return HttpResponseRedirect(reverse('commentators:commentator', args=(commentator.id,)))


# list all datapoints
@api_view(['GET'])
def getTimestamps(request):
    commentator_ts = Commentator.objects.all()
    serializer = CommentatorSerializer(commentator_ts, many=True)
    return Response(serializer.data)


# get single datapoint
@api_view(['GET'])
def getTimestamp(request, pk):
    commentator_ts = Commentator.objects.get(id=pk)
    serializer = CommentatorSerializer(commentator_ts, many=False)
    return Response(serializer.data)


# add new datapoint
@api_view(['POST'])
def addTimestamp(request):
    serializer = CommentatorSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)


# update datapoint
@api_view(['PUT'])
def updateTimestamp(request, pk):
    commentator_ts = Commentator.objects.get(id=pk)
    serializer = CommentatorSerializer(instance=commentator_ts, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)


# delete datapoint
@api_view(['DELETE'])
def deleteTimestamp(request, pk):
    commentator_ts = Commentator.objects.get(id=pk)
    commentator_ts.delete()
    
    return Response('Item successfully deleted!')


@api_view(['POST'])
def parseMuxWebhooks(request):
    webhook_type = request.data["type"]
    if webhook_type == "video.live_stream.connected":
        handleStreamStart(request.data)
    elif webhook_type == "video.asset.ready":
        handleAssetReady(request.data)
        
    return Response("Webhook received.")


@api_view(['GET'])
def getActiveCommentators(request, event):
    """
    This is the function that gets called by the chrome extension. 
    It returns a list of all active commentators for a given event.
    """
    # Get all active live streams from Mux
    response = requests.get(f"{MUX_LS_API_URL}?status=active", 
                            headers={"Content-Type": "application/json"},
                            auth=(os.getenv('MUX_TOKEN_ID'), os.getenv('MUX_TOKEN_SECRET')))
    if len(response.json()["data"]) > 0:
        live_stream_ids = [active_stream["id"] for active_stream in response.json()["data"]]
        try:
            commentators = Commentator.objects.filter(live_stream_id__in=live_stream_ids, game__name=event)
            serializer = CommentatorSerializer(commentators, many=True)
            
            # Add game start timestamp to serializer
            gamestart_ts = commentators[0].game.start_timestamp
            for commentator in serializer.data:
                commentator["game_start_ts"] = gamestart_ts
                    
            return Response(serializer.data)
        
        except Commentator.DoesNotExist:
            return Response("No active commentators found.", status=404)
    else:
        return Response([])
