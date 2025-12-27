from django.utils.translation import gettext_lazy as _

from apps.attendance.models import EmployeeAttendance
from apps.core.tables import BaseTable


class EmployeeAttendanceTable(BaseTable):
    BUTTONS = {
        'view': {'label': _('View'), 'url_name': 'attendance:employeeattendance_detail'},
        'edit': {'label': _('Edit'), 'url_name': 'attendance:employeeattendance_update'},
        'delete': {'label': _('Delete'), 'url_name': 'attendance:employeeattendance_delete'},
    }

    class Meta(BaseTable.Meta):
        model = EmployeeAttendance
        fields = ('id', 'user', 'checkin_time', 'checkout_time')
