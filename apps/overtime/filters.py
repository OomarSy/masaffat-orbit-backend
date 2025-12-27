import django_filters
from apps.overtime.models import EmployeeOvertime
from apps.core.filters import BaseFilterSet
from apps.core.mixins import ActiveNormalUserFilterMixin


class EmployeeOvertimeFilter(ActiveNormalUserFilterMixin, BaseFilterSet):
    start_datetime = django_filters.DateTimeFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'datetime-local'}
        )
    )
    
    class Meta:
        model = EmployeeOvertime
        fields = ['user', 'start_datetime']