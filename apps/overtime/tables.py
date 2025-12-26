from django.utils.translation import gettext_lazy as _

from apps.overtime.models import Overtime
from apps.core.tables import BaseTable


class OvertimeTable(BaseTable):
    BUTTONS = {
        'view': {'label': _('View'), 'url_name': 'overtime:overtime_detail'},
        'edit': {'label': _('Edit'), 'url_name': 'overtime:overtime_update'},
        'delete': {'label': _('Delete'), 'url_name': 'overtime:overtime_delete'},
    }

    class Meta(BaseTable.Meta):
        model = Overtime
        fields = ('id', 'user', 'start_datetime', 'end_datetime', 'hours', 'note')
