"""viewset for Trip"""
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from queuedapi.models import Trip, QueueUser

class TripUserSerializer(serializers.ModelSerializer):
    """django user serializer"""
    class Meta:
        model = User
        fields = ("username", "id")

class QueueUserSerializer(serializers.ModelSerializer):
    """queue user serializer"""
    user = TripUserSerializer(many=False)
    class Meta:
        model = QueueUser
        fields = ("profile_image_url", "user")

class TripSerializer(serializers.ModelSerializer):
    """trip serializer"""
    vacationer = QueueUserSerializer(many=False)
    class Meta:
        model = Trip
        fields = ("id", "vacationer_id", "name", "hotel", "date_start", "date_end", "vacationer")

class Trips(ViewSet):
    """trips view"""
    def create(self, request):
        """create new trip"""
        vacationer = QueueUser.objects.get(user=request.auth.user)
        trip = Trip()
        trip.name = request.data["name"]
        trip.hotel = request.data["hotel"]
        trip.date_start = request.data["date_start"]
        trip.date_end = request.data["date_end"]
        trip.vacationer = vacationer
        try:
            trip.save()
            serializer = TripSerializer(trip, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """retrieves single trip if that trip was created by the currently authenticated user"""
        current_user = QueueUser.objects.get(user=request.auth.user)
        try:
            trip = Trip.objects.get(pk=pk, vacationer=current_user)
            serializer = TripSerializer(trip, context={'request': request})
            return Response(serializer.data)
        except Trip.DoesNotExist:
            return Response(
                {'message': 'Trip does not exist for this user'}, 
                status=status.HTTP_400_BAD_REQUEST
                )

    def list(self, request):
        """lists trips that were created by the currently authenticated user"""
        vacationer = QueueUser.objects.get(user=request.auth.user)
        trips = Trip.objects.filter(vacationer=vacationer).order_by('date_start')

        serializer = TripSerializer(trips, many=True, context={"request": request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """deletes single trip if that trip was created by the currently authenticated user"""
        current_user = QueueUser.objects.get(user=request.auth.user)
        try:
            trip = Trip.objects.get(pk=pk, vacationer=current_user)
            trip.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Trip.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """edits trip if that trip was created by the currently authenticated user"""
        current_user = QueueUser.objects.get(user=request.auth.user)
        try:
            trip = Trip.objects.get(pk=pk, vacationer=current_user)
            trip.name = request.data["name"]
            trip.hotel = request.data["hotel"]
            trip.date_start = request.data["date_start"]
            trip.date_end = request.data["date_end"]
            trip.vacationer = current_user
            trip.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Trip.DoesNotExist:
            return Response(
                {'message': 'Trip does not exist for this user'}, 
                status=status.HTTP_400_BAD_REQUEST
                )
                