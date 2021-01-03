"""Viewset for park rides"""
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from queuedapi.models import Ride
from django.db.models import Q

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ("ride","name", "lat", "longitude")

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
        rides = Ride.objects.all()

        search_text = self.request.query_params.get('q', None)
        if search_text is not None:
            rides = Ride.objects.filter(Q(name__contains=search_text))

        serializer = RideSerializer(rides, many=True, context={'request': request})
        return Response(serializer.data)
