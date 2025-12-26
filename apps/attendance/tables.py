from django.utils.translation import gettext_lazy as _

from apps.attendance.models import Attendance
from apps.core.tables import BaseTable


class AttendanceTable(BaseTable):
    BUTTONS = {
        'view': {'label': _('View'), 'url_name': 'attendance:attendance_detail'},
        'edit': {'label': _('Edit'), 'url_name': 'attendance:attendance_update'},
        'delete': {'label': _('Delete'), 'url_name': 'attendance:attendance_delete'},
    }

    class Meta(BaseTable.Meta):
        model = Attendance
        fields = ('id', 'user', 'checkin_time', 'checkout_time')
