"""viewset for Ride Itineraries"""
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from queuedapi.models import RideItinerary, Itinerary, Ride

class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ("id", "park_date", "trip", "trip_id")

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ("name", "lat", "longitude")

class RideItinerarySerializer(serializers.ModelSerializer):
    itinerary = ItinerarySerializer(many=False)
    ride = RideSerializer(many=False)
    class Meta:
        model = RideItinerary
        fields = ("id", "ride_id", "order", "ride", "itinerary", "itinerary_id")



class RideItineraries(ViewSet):
    def create(self, request):
        itinerary = Itinerary.objects.get(pk=request.data["itinerary_id"])
        ride_itinerary = RideItinerary()
        ride_itinerary.itinerary = itinerary
        ride = Ride.objects.get(pk=request.data["ride_id"])
        ride_itinerary.ride = ride
        ride_itinerary.order = request.data["order"]
        try:
            ride_itinerary.save()
            serializer = RideItinerarySerializer(ride_itinerary, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            ride_itinerary = RideItinerary.objects.get(pk=pk)
            serializer = RideItinerarySerializer(ride_itinerary, context={'request': request})
            return Response(serializer.data)
        except RideItinerary.DoesNotExist:
            return Response({'message': 'Ride itinerary does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        ride_itineraries = RideItinerary.objects.all()
        itinerary = self.request.query_params.get('itinerary_id', None)
        if itinerary is not None:
            ride_itineraries = ride_itineraries.filter(itinerary_id=itinerary).order_by('order')
        serializer = RideItinerarySerializer(ride_itineraries, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            ride_itinerary = RideItinerary.objects.get(pk=pk)
            ride_itinerary.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except RideItinerary.DoesNotExist:
            return Response({'message': 'Ride itinerary does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        try:
            ride_itinerary = RideItinerary.objects.get(pk=pk)
            ride_itinerary.order = request.data["order"]
            ride_itinerary.save()
            return Response({},
            status=status.HTTP_204_NO_CONTENT
            )
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

           


