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

    def validate(self, data):
        start_dt = datetime.combine(data['start_date'], data['start_time'])
        end_dt = datetime.combine(data['end_date'], data['end_time'])

        if start_dt >= end_dt:
            raise serializers.ValidationError("تاريخ ووقت البدء يجب أن يكون قبل تاريخ ووقت الانتهاء.")

        if end_dt > timezone.now():
            raise serializers.ValidationError(
                "لا يمكن إدخال دوام إضافي في المستقبل."
            )
        
        return data