from rest_framework import serializers

class UserLocationSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=30, decimal_places=15)
    longitude = serializers.DecimalField(max_digits=30, decimal_places=15)
    
class UserLocationCMSSerializer(serializers.Serializer):
    is_online = serializers.ReadOnlyField()
    user_id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    updated_at = serializers.DateTimeField()