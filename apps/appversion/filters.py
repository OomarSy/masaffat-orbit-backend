from apps.appversion.models import AndroidAppRelease
from apps.core.filters import BaseFilterSet
from apps.core.mixins import ActiveNormalUserFilterMixin


class AndroidAppReleaseFilter(ActiveNormalUserFilterMixin, BaseFilterSet):
    
    class Meta:
        model = AndroidAppRelease
        fields = ['version']