import django_filters

from .models import Attendance
from apps.core.filters import BaseFilterSet
from apps.core.mixins import ActiveNormalUserFilterMixin


class AttendanceFilter(ActiveNormalUserFilterMixin, BaseFilterSet):
    checkin_time = django_filters.DateTimeFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'datetime-local'}
        )
    )
    
    class Meta:
        model = Attendance
        fields = ['user', 'checkin_time']