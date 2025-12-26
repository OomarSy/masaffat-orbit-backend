from django.utils.translation import gettext_lazy as _

from .models import AppVersion

from apps.core.mixins import ActiveNormalUserFormMixin
from apps.core.forms import BaseModelForm


class AppVersionForm(ActiveNormalUserFormMixin, BaseModelForm):
    SUBMIT_TEXT = _('Save AppVersion')

    class Meta(BaseModelForm.Meta):
        model = AppVersion
        fields = '__all__'
        hidden_in_create_fields=['update_type']