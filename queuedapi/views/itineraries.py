"""viewset for Daily Itineraries"""
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from queuedapi.models import Itinerary, Trip

class TripSerializer(serializers.ModelSerializer):
    """trip serializer"""
    class Meta:
        model = Trip
        fields = ("id", "vacationer_id", "name", "hotel", "date_start", "date_end")

class ItinerarySerializer(serializers.ModelSerializer):
    trip = TripSerializer(many=False)
    class Meta:
        model = Itinerary
        fields = ("id", "park_date", "trip", "trip_id")

class Itineraries(ViewSet):
    """itinerary view"""
    def create(self, request):
        """create new itinerary"""
        trip = Trip.objects.get(pk=request.data["trip_id"])
        itinerary = Itinerary()
        itinerary.trip = trip
        itinerary.park_date = request.data["park_date"]
        try:
            itinerary.save()
            serializer = ItinerarySerializer(itinerary, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            serializer = ItinerarySerializer(itinerary, context={'request': request})
            return Response(serializer.data)
        except Itinerary.DoesNotExist:
            return Response({'message': 'Itinerary does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        itineraries = Itinerary.objects.all()

        trip = self.request.query_params.get('trip_id', None)

        if trip is not None:
            itineraries = itineraries.filter(trip_id=trip)
        
        serializer = serializer = ItinerarySerializer(itineraries, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            itinerary.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Itinerary.DoesNotExist:
            return Response({'message': 'Itinerary does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk=None):
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            itinerary.park_date = request.data["park_date"]
            trip = Trip.objects.get(pk=request.data["trip_id"])
            itinerary.trip = trip
            itinerary.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Itinerary.DoesNotExist:
            return Response({'message': 'Itinerary does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
