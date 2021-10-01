from rest_framework import serializers
from . import models


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Accounts
        fields = "__all__"


class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Places
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = "__all__"

class Review_picSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review_pic
        fields = "__all__"

class Review_tagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review_tag
        fields = "__all__"

class Review_likeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review_like
        fields = "__all__"
