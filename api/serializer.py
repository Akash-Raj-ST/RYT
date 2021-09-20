from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"


class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Places
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = "__all__"
