import datetime
import os
import requests

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Commentator  #, Viewer
from .serializers import CommentatorSerializer
from .utils import mm_ss_to_seconds
from .webhooks import handleStreamStart, handleAssetReady


MUX_LS_API_URL = "https://api.mux.com/video/v1/live-streams"

# load .env file
load_dotenv()


def index(request):
    return render(request, 'sync/index.html')


def createNewStream(request):
    name = request.POST["name"]
    game = request.POST["game"]
    new_commentator = Commentator.objects.create(commentator_name=name, event_name=game)
    
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
        "reconnect_window": 10,
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
    
    return render(request, 'sync/commentator_ts.html', { "commentator": new_commentator})


def commentatorHome(request, commentator_id):
    commentator = get_object_or_404(Commentator, pk=commentator_id)
    return render(request, 'sync/commentator_ts.html', {"commentator": commentator})


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
    
    offset = (submit_time - stream_started).total_seconds() + commentator_position
    print("Offset (s):", offset)
    
    # update commentator object
    commentator.game_offset = offset
    commentator.save()
    
    return HttpResponseRedirect(reverse('sync:commentator', args=(commentator_id,)))


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
    
    live_stream_ids = [active_stream["id"] for active_stream in response.json()["data"]]
    try:
        commentators = Commentator.objects.filter(live_stream_id__in=live_stream_ids, event_name=event)
        serializer = CommentatorSerializer(commentators, many=True)
        return Response(serializer.data)
    
    except Commentator.DoesNotExist:
        return Response("No active commentators found.")
