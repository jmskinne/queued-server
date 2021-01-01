from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from queuedapi.models import QueueUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ("username", "id")

class QueueUserSerializer(serializers.ModelSerializer):
    """queue user serializer"""
    user = UserSerializer(many=False)
    class Meta:
        model = QueueUser
        fields = ("profile_image_url", "user")

class Profiles(ViewSet):
    def list(self, request):

        current_user = QueueUser.objects.filter(user=request.auth.user)
        serializer = QueueUserSerializer(current_user, many=True, context={"request":request})
        return Response(serializer.data)