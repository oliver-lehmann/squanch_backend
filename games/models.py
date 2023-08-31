from django.db import models

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=200)
    start_timestamp = models.FloatField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.name
