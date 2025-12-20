from rest_framework import serializers
from datetime import datetime
from django.utils import timezone

class AttendanceSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=30, decimal_places=15)
    longitude = serializers.DecimalField(max_digits=30, decimal_places=15)


class OvertimeEntrySerializer(serializers.Serializer):
    start_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_date = serializers.DateField()
    end_time = serializers.TimeField()
    note = serializers.CharField(required=False, allow_blank=True)
    