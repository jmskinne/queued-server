"""viewset for Ride Favorites"""
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from queuedapi.models import QueueUser, RideFavorite, Ride

class RideUserSerializer(serializers.ModelSerializer):
    """django user serializer"""
    class Meta:
        model = User
        fields = ("username", "id")

class QueueUserSerializer(serializers.ModelSerializer):
    """queue user serializer"""
    user = RideUserSerializer(many=False)
    class Meta:
        model = QueueUser
        fields = ("profile_image_url", "user")

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ("ride", "name")

class RideFavoriteSerializer(serializers.ModelSerializer):
    """ride favorite serializer"""
    vacationer = QueueUserSerializer(many=False)
    ride = RideSerializer(many=False)
    class Meta:
        model = RideFavorite
        fields = ("id", "ride_id", "favorite", "vacationer_id", "ride", "vacationer")

class RideFavorites(ViewSet):
#     """ride favorite"""
#     def create(self, request):
#         """add a favorite ride"""
#         vacationer = QueueUser.objects.get(user=request.auth.user)
#         ride_favorite = RideFavorite()
#         ride = Ride.objects.get(pk=request.data["ride_id"])
#         ride_favorite.ride = ride
#         ride_favorite.vacationer = vacationer
#         ride_favorite.favorite = request.data["favorite"]
#         try:
#             ride_favorite.save()
#             serializer = RideFavoriteSerializer(ride_favorite, context={'request': request})
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except ValidationError as ex:
#             return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, pk=None):
    #     """get a single object for ride favorites if created by currently authenticated user"""
    #     current_user = QueueUser.objects.get(user=request.auth.user)
    #     try:
    #         ride_favorite = RideFavorite.objects.get(pk=pk, vacationer=current_user)
    #         serializer = RideFavoriteSerializer(ride_favorite, context={'request': request})
    #         return Response(serializer.data)
    #     except RideFavorite.DoesNotExist:
    #         return Response(
    #             {'message': 'Favorite does not exist for this user'}, 
    #             status=status.HTTP_400_BAD_REQUEST
    #             )

    def list(self, request):
        ride_favorites = RideFavorite.objects.all()
        
        current_user = QueueUser.objects.get(user=request.auth.user)
        fav = self.request.query_params.get('favorite', None)
            
        if fav is not None:
            ride_favorites = ride_favorites.filter(vacationer=current_user, favorite=fav)

        serializer = RideFavoriteSerializer(ride_favorites, many=True, context={'request': request})
        return Response(serializer.data)

    # def partial_update(self, request, pk=None):
    #     """patch for favoriting or unfavoriting a ride for currently authenticated user"""
    #     current_user = QueueUser.objects.get(user=request.auth.user)
    #     try:
    #         ride_favorite = RideFavorite.objects.get(pk=pk, vacationer=current_user)
    #         ride_favorite.favorite = request.data["favorite"]
    #         ride_favorite.save()
    #         return Response({},
    #         status=status.HTTP_204_NO_CONTENT
    #         )
    #     except ValidationError as ex:
    #         return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)