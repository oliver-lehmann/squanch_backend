from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    surname = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    password = models.CharField(max_length=128, blank=True)
    birthday = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.surname} {self.lastname}"
