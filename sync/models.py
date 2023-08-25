from django.db import models

class Commentator(models.Model):
    commentator_name = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    stream_start = models.DateTimeField(blank=True, null=True)
    stream_key = models.CharField(max_length=200, blank=True)
    playback_id = models.CharField(max_length=200, blank=True)
    game_offset = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.commentator_name
    

# class Viewer(models.Model):
#     viewer_name = models.CharField(max_length=50)
#     event_name = models.CharField(max_length=200)
#     event_start = models.IntegerField(blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.viewer_name
    