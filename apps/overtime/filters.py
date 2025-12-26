import django_filters
from apps.overtime.models import Overtime
from apps.core.filters import BaseFilterSet
from apps.core.mixins import ActiveNormalUserFilterMixin


class OvertimeFilter(ActiveNormalUserFilterMixin, BaseFilterSet):
    start_datetime = django_filters.DateTimeFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'datetime-local'}
        )
    )
    
    class Meta:
        model = Overtime
        fields = ['user', 'start_datetime']