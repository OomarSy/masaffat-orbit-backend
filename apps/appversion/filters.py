from apps.appversion.models import AppVersion
from base.filters import BaseFilterSet
from base.mixins import ActiveNormalUserFilterMixin


class AppVersionFilter(ActiveNormalUserFilterMixin, BaseFilterSet):
    
    class Meta:
        model = AppVersion
        fields = ['version']