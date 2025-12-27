from django.utils.translation import gettext_lazy as _

from apps.core.tables import BaseTable
from apps.users.models import User


class UserTable(BaseTable):
    BUTTONS = {
        'view': {'label': _('View'), 'url_name': 'users:user_detail'},
        'edit': {'label': _('Edit'), 'url_name': 'users:user_update'},
        'delete': {'label': _('Delete'), 'url_name': 'users:user_delete'},
    }

    class Meta(BaseTable.Meta):
        model = User
        fields = ('id', 'username', 'is_active', 'last_login')