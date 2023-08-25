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
        "use_slate_for_standard_latency": True,
        "audio_only": True,
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
        new_commentator.playback_id = response.json()["data"]["playback_ids"][0]["id"]
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


def handleStreamStart(data):
    print("Handling stream start...")
    # get commentator object with matching stream_key
    commentator = get_object_or_404(Commentator, stream_key=data["data"]["stream_key"])
    stream_start = datetime.datetime.fromisoformat(data["created_at"].replace('Z', '+00:00'))
    commentator.stream_start = stream_start
    commentator.save()
    print("Stream start time saved to database.")


@api_view(['POST'])
def parseMuxWebhooks(request):
    print("request.data: ", request.data)
    if request.data["type"] == "video.live_stream.active":
        handleStreamStart(request.data)
    return Response("Webhook received.")
