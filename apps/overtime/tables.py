from django.utils.translation import gettext_lazy as _
import django_tables2 as tables

from apps.overtime.models import EmployeeOvertime
from apps.core.tables import BaseTable



class EmployeeOvertimeTable(BaseTable):
    day = tables.Column(
        verbose_name=_("اليوم"),
        accessor="day_name_ar",
        orderable=False
    )
    
    BUTTONS = {
        'view': {'label': _('View'), 'url_name': 'overtime:employeeovertime_detail'},
        'edit': {'label': _('Edit'), 'url_name': 'overtime:employeeovertime_update'},
        'delete': {'label': _('Delete'), 'url_name': 'overtime:employeeovertime_delete'},
    }

    class Meta(BaseTable.Meta):
        model = EmployeeOvertime
        fields = ('id', 'user', 'day', 'start_datetime', 'end_datetime', 'hours', 'note')
