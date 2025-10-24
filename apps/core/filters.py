from base.filters import BaseFilterSet
from apps.core.models import User


class UserFilter(BaseFilterSet):
    class Meta:
        model = User
        fields = ['username', 'is_active', 'is_staff']
