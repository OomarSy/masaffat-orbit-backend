import django_filters
from apps.attendance.models import Attendance, Overtime
from base.filters import BaseFilterSet
from base.mixins import ActiveNormalUserFilterMixin


class AttendanceFilter(ActiveNormalUserFilterMixin, BaseFilterSet):
    checkin_time = django_filters.DateTimeFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'datetime-local'}
        )
    )
    
    class Meta:
        model = Attendance
        fields = ['user', 'checkin_time']


class OvertimeFilter(ActiveNormalUserFilterMixin, BaseFilterSet):
    start_datetime = django_filters.DateTimeFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'datetime-local'}
        )
    )
    
    class Meta:
        model = Overtime
        fields = ['user', 'start_datetime']