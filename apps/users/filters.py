from apps.core.filters import BaseFilterSet
from apps.users.models import User


class UserFilter(BaseFilterSet):
    class Meta:
        model = User
        fields = ['username', 'is_active', 'is_staff']
