from django.utils.translation import gettext_lazy as _

from apps.overtime.models import EmployeeOvertime
from apps.core.tables import BaseTable


class EmployeeOvertimeTable(BaseTable):
    BUTTONS = {
        'view': {'label': _('View'), 'url_name': 'overtime:employeeovertime_detail'},
        'edit': {'label': _('Edit'), 'url_name': 'overtime:employeeovertime_update'},
        'delete': {'label': _('Delete'), 'url_name': 'overtime:employeeovertime_delete'},
    }

    class Meta(BaseTable.Meta):
        model = EmployeeOvertime
        fields = ('id', 'user', 'start_datetime', 'end_datetime', 'hours', 'note')
