from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Synchronization
from .serializers import SynchronizationSerializer


# list all datapoints
@api_view(['GET'])
def getTimestamps(request):
    commentator_ts = Synchronization.objects.all()
    serializer = SynchronizationSerializer(commentator_ts, many=True)
    return Response(serializer.data)


# get single datapoint
@api_view(['GET'])
def getTimestamp(request, pk):
    commentator_ts = Synchronization.objects.get(id=pk)
    serializer = SynchronizationSerializer(commentator_ts, many=False)
    return Response(serializer.data)


# add new datapoint
@api_view(['POST'])
def addTimestamp(request):
    serializer = SynchronizationSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)


# update datapoint
@api_view(['PUT'])
def updateTimestamp(request, pk):
    commentator_ts = Synchronization.objects.get(id=pk)
    serializer = SynchronizationSerializer(instance=commentator_ts, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)


# delete datapoint
@api_view(['DELETE'])
def deleteTimestamp(request, pk):
    commentator_ts = Synchronization.objects.get(id=pk)
    commentator_ts.delete()
    
    return Response('Item successfully deleted!')
