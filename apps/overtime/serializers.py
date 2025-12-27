from rest_framework import serializers

from .models import EmployeeOvertime


class EmployeeOvertimeEntrySerializer(serializers.Serializer):
    start_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_date = serializers.DateField()
    end_time = serializers.TimeField()
    note = serializers.CharField(required=False, allow_blank=True)


class EmployeeOvertimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeOvertime
        fields = (
            "id",
            "start_datetime",
            "end_datetime",
            "hours",
            "note",
            "created_at",
        )
