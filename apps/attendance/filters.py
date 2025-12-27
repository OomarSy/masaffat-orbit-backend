import django_filters

from .models import EmployeeAttendance
from apps.core.filters import BaseFilterSet
from apps.core.mixins import ActiveNormalUserFilterMixin


class EmployeeAttendanceFilter(ActiveNormalUserFilterMixin, BaseFilterSet):
    checkin_time = django_filters.DateTimeFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'datetime-local'}
        )
    )
    
    class Meta:
        model = EmployeeAttendance
        fields = ['user', 'checkin_time']