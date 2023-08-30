import datetime

from django.shortcuts import get_object_or_404

from .models import Commentator


def handleStreamStart(data):
    print("Handling stream start...")
    # get commentator object with matching stream_key
    commentator = get_object_or_404(Commentator, stream_key=data["data"]["stream_key"])
    stream_start = datetime.datetime.fromisoformat(data["created_at"].replace('Z', '+00:00'))
    commentator.stream_start = stream_start
    commentator.save()
    print("Stream start time saved to database.")
    

def handleAssetReady(data):
    if data["data"]["is_live"]:
        print("Handling asset ready...")
        # get commentator object with matching live_stream_id
        commentator = get_object_or_404(Commentator, live_stream_id=data["data"]["live_stream_id"])
        commentator.playback_id = data["data"]["playback_ids"][0]["id"]
        commentator.save()
        print("Playback ID saved to database.")