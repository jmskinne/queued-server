"""viewset for Ride Reviews"""
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from queuedapi.models import QueueUser, RideReview, Ride

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

class RideReviewSerializer(serializers.ModelSerializer):
    """ride review serializer"""
    reviewer = QueueUserSerializer(many=False)
    ride = RideSerializer(many=False)
    class Meta:
        model = RideReview
        fields = ("id", "ride_id", "rating", "review","ride", "reviewer")

class RideReviews(ViewSet):
    """ride review view set"""
    def create(self, request):
        """create a ride review"""
        reviewer = QueueUser.objects.get(user=request.auth.user)
        ride_review = RideReview()
        ride = Ride.objects.get(pk=request.data["ride_id"])
        ride_review.ride = ride
        ride_review.rating = request.data["rating"]
        ride_review.review = request.data["review"]
        ride_review.reviewer = reviewer
        try:
            ride_review.save()
            serializer = RideReviewSerializer(ride_review, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
 
    def retrieve(self, request, pk=None):
        """get a single ride review object"""
        try:
            ride_review = RideReview.objects.get(pk=pk)
            serializer = RideReviewSerializer(ride_review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseNotFound(ex)

    def list(self, request):
        """view all ride reviews, also can view rides by
            ride_id, >= rating, and a specific rating
        """
        ride_reviews = RideReview.objects.all()

        ride = self.request.query_params.get('ride_id', None)
        min_rating = self.request.query_params.get('min_rating', None)
        rating = self.request.query_params.get('rating', None)
        
        if ride is not None:
            ride_reviews = ride_reviews.filter(ride_id=ride)
        
        if rating is not None:
            ride_reviews = ride_reviews.filter(rating=rating)
        
        if min_rating is not None:
            ride_reviews = ride_reviews.filter(rating__gte=min_rating)

        serializer = RideReviewSerializer(ride_reviews, many=True,context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """delete a ride review if request is from currently authenticated user"""
        current_user = QueueUser.objects.get(user=request.auth.user)
        try:
            ride_review = RideReview.objects.get(pk=pk, reviewer=current_user)
            ride_review.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except RideReview.DoesNotExist:
            return Response(
                {'message': "You cannot delete another user's review"},
                status=status.HTTP_404_NOT_FOUND
                )

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """edit a ride review if request is from currently authenticated user"""
        current_user = QueueUser.objects.get(user=request.auth.user)
        ride_review = RideReview.objects.get(pk=pk, reviewer=current_user)
        try:
            ride = Ride.objects.get(pk=request.data["ride_id"])
            ride_review.ride = ride
            ride_review.rating = request.data["rating"]
            ride_review.review = request.data["review"]
            ride_review.reviewer = current_user
            ride_review.save()
            return Response({},
            status=status.HTTP_204_NO_CONTENT
            )
        except RideReview.DoesNotExist:
            return Response(
                {'message': "You cannot edit another user's review"},
                status=status.HTTP_400_BAD_REQUEST
            )
