from django.urls import path
from . import views

app_name = 'sync'
urlpatterns = [
    path('', views.getTimestamps, name='listAllTimestamps'),
    path('create', views.addTimestamp, name='addTimestamp'),
    path('read/<str:pk>', views.getTimestamp, name='getTimestamp'),
    path('update/<str:pk>', views.updateTimestamp, name='updateTimestamp'),
    path('delete/<str:pk>', views.deleteTimestamp, name='deleteTimestamp'),
]

