from django.utils.translation import gettext_lazy as _

from .models import AndroidAppRelease
from apps.core.tables import BaseTable


class AndroidAppReleaseTable(BaseTable):
    BUTTONS = {
        'view': {'label': _('View'), 'url_name': 'appversion:androidapprelease_detail'},
        'edit': {'label': _('Edit'), 'url_name': 'appversion:androidapprelease_update'},
        'delete': {'label': _('Delete'), 'url_name': 'appversion:androidapprelease_delete'},
    }

    class Meta(BaseTable.Meta):
        model = AndroidAppRelease
        fields = ('id', 'version')
