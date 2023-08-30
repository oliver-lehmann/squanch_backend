from django.db import models

class Commentator(models.Model):
    commentator_name = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    live_stream_id = models.CharField(max_length=200, blank=True)
    stream_start = models.DateTimeField(blank=True, null=True)
    stream_key = models.CharField(max_length=200, blank=True)
    playback_id = models.CharField(max_length=200, blank=True)
    game_offset = models.IntegerField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.commentator_name
    