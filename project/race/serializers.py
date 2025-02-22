from rest_framework import serializers
from .models import LeaderboardEntry, Route

# Serializer for the Route model
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'  # This includes all fields from the Route model

# Serializer for the LeaderboardEntry model
class LeaderboardEntrySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display username instead of user ID
    route = RouteSerializer()  # Nested serializer to include route data

    class Meta:
        model = LeaderboardEntry
        fields = '__all__'  # This includes all fields from the LeaderboardEntry model