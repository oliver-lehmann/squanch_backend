from django.urls import path
from . import views

app_name = 'games'
urlpatterns = [
    path('setGameStart', views.setGameStart, name='setGameStart'),
]