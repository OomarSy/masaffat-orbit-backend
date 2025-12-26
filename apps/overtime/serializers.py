from rest_framework import serializers

from .models import Overtime


class OvertimeEntrySerializer(serializers.Serializer):
    start_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_date = serializers.DateField()
    end_time = serializers.TimeField()
    note = serializers.CharField(required=False, allow_blank=True)


class OvertimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overtime
        fields = (
            "id",
            "start_datetime",
            "end_datetime",
            "hours",
            "note",
            "created_at",
        )
