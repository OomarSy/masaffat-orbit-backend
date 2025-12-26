from apps.appversion.models import AppVersion
from apps.core.filters import BaseFilterSet
from apps.core.mixins import ActiveNormalUserFilterMixin


class AppVersionFilter(ActiveNormalUserFilterMixin, BaseFilterSet):
    
    class Meta:
        model = AppVersion
        fields = ['version']