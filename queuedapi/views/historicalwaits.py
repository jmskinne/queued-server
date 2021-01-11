from django.core.exceptions import ValidationError
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from queuedapi.models import Ride, HistoricalWait


class WaitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HistoricalWait
        fields = ("ride", "created_on", "wait")


class HistoricalWaits(ViewSet):
    def create(self, request):
        historical_wait = HistoricalWait()
        historical_wait.ride = request.data["ride"]
        
        historical_wait.wait = request.data["wait"]
        try:
            historical_wait.save()
            serializer = WaitSerializer(historical_wait, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)  


    def list(self, request):
        historical_waits = HistoricalWait.objects.all()

        ride = self.request.query_params.get('ride', None)
        by_date = self.request.query_params.get('date', None)

        if ride is not None:
            historical_waits = historical_waits.filter(ride=ride)
        
        if by_date is not None:
            historical_waits = historical_waits.filter(created_on__contains=by_date)

        serializer = WaitSerializer(historical_waits, many=True,
        context={'request': request})
        return Response(serializer.data)
