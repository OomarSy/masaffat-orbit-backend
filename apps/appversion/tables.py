from django.utils.translation import gettext_lazy as _

from .models import AppVersion
from apps.core.tables import BaseTable


class AppVersionTable(BaseTable):
    BUTTONS = {
        'view': {'label': _('View'), 'url_name': 'appversion:appversion_detail'},
        'edit': {'label': _('Edit'), 'url_name': 'appversion:appversion_update'},
        'delete': {'label': _('Delete'), 'url_name': 'appversion:appversion_delete'},
    }

    class Meta(BaseTable.Meta):
        model = AppVersion
        fields = ('id', 'version')
