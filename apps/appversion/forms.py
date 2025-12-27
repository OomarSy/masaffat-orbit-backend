from django.utils.translation import gettext_lazy as _

from .models import AndroidAppRelease

from apps.core.mixins import ActiveNormalUserFormMixin
from apps.core.forms import BaseModelForm


class AndroidAppReleaseForm(ActiveNormalUserFormMixin, BaseModelForm):
    SUBMIT_TEXT = _('Save Android App Release')

    class Meta(BaseModelForm.Meta):
        model = AndroidAppRelease
        fields = '__all__'
        hidden_in_create_fields=['update_type']