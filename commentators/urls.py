from django.urls import path
from . import views

app_name = 'commentators'
urlpatterns = [
    path('', views.index, name='index'),
    path('newStream', views.createNewStream, name='newStream'),
    path('commentator/<int:commentator_id>', views.commentatorHome, name='commentator'),
    path('commentator/<int:commentator_id>/addTs', views.addCommentatorOffset, name='addOffset'),
    path('listAll', views.getTimestamps, name='listAllTimestamps'),
    path('create', views.addTimestamp, name='addTimestamp'),
    path('read/<int:pk>', views.getTimestamp, name='getTimestamp'),
    path('update/<int:pk>', views.updateTimestamp, name='updateTimestamp'),
    path('delete/<int:pk>', views.deleteTimestamp, name='deleteTimestamp'),
    path('listActive/<str:event>', views.getActiveCommentators, name='listActiveCommentators'),
    path('mux/webhooks', views.parseMuxWebhooks, name='parseMuxWebhooks'),
]

