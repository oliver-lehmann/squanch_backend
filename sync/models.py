from django.db import models

class Synchronization(models.Model):
    event_name = models.CharField(max_length=200)
    commentator_position = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    