from django.db import models
from games.models import Game
from users.models import User

class Commentator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    live_stream_id = models.CharField(max_length=200, blank=True)
    stream_start = models.DateTimeField(blank=True, null=True)
    stream_key = models.CharField(max_length=200, blank=True)
    playback_id = models.CharField(max_length=200, blank=True)
    game_offset = models.IntegerField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username + ": " + self.game.name
    
    def get_commentator_name(self):
        return self.user.username
    
    def get_game_name(self):
        return self.game.name
    