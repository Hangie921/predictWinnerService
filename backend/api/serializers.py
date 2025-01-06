from rest_framework import serializers
from .models import User, Weight, PredictionQuery
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = ["diff_win_point_weight", "last_10_win_weight", "home_or_away_winning_weight", "pithcer_handed_winning_weight", "overall_winning_weight", "owner"]
        extra_kwargs = {"owner": {"read_only": True}}

class PredictionQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionQuery
        fields = ["user", "start_date", "end_date"]
        # extra_kwargs = {"result": {"read_only": True}}