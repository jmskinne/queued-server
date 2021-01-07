"""Viewset for park rides"""
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from queuedapi.models import Ride, RideFavorite, QueueUser
from django.db.models import Q
from rest_framework.decorators import action

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ("ride","name", "lat", "longitude", "average_rating")

class Rides(ViewSet):
    def create(self, request):
        ride = Ride()
        ride.ride = request.data["id"]
        ride.name = request.data["name"]
        ride.lat = request.data["lat"]
        ride.longitude = request.data["longitude"]
        try:
            ride.save()
            serializer = RideSerializer(ride, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            ride = Ride.objects.get(pk=pk)
            serializer = RideSerializer(ride, context={'request': request})
            return Response(serializer.data)
        except Ride.DoesNotExist:
            return Response(False)

    def list(self, request):
        rides = Ride.objects.all().order_by('name')

        search_text = self.request.query_params.get('q', None)
        if search_text is not None:
            rides = Ride.objects.filter(Q(name__contains=search_text) | Q(ride__contains=search_text))

        serializer = RideSerializer(rides, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post', 'get'], detail=True)
    def favorite(self, request, pk):
        if request.method == "POST":
            try:
                vacationer = QueueUser.objects.get(user=request.auth.user)
                ride = Ride.objects.get(pk=pk)
                favorite = request.data["favorite"]
                ridefavorites = RideFavorite.objects.get(vacationer=vacationer, ride=ride, favorite=favorite)
                ridefavorites.delete()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except RideFavorite.DoesNotExist:
                vacationer = QueueUser.objects.get(user=request.auth.user)
                ride_favorite = RideFavorite()
                ride = Ride.objects.get(pk=pk)
                ride_favorite.ride = ride
                ride_favorite.vacationer = vacationer
                ride_favorite.favorite = request.data["favorite"]
                ride_favorite.save()
                return Response({}, status=status.HTTP_201_CREATED)
