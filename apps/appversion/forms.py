from django import forms
from django.utils.translation import gettext_lazy as _

from apps.appversion.models import AppVersion

from base.mixins import ActiveNormalUserFormMixin
from base.forms import BaseModelForm


class AppVersionForm(ActiveNormalUserFormMixin, BaseModelForm):
    SUBMIT_TEXT = _('Save AppVersion')

    class Meta(BaseModelForm.Meta):
        model = AppVersion
        fields = '__all__'
        hidden_in_create_fields=['update_type']