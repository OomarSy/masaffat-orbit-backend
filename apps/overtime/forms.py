from django import forms
from django.utils.translation import gettext_lazy as _

from apps.overtime.models import EmployeeOvertime

from apps.core.mixins import ActiveNormalUserFormMixin
from apps.core.forms import BaseModelForm


class EmployeeOvertimeForm(ActiveNormalUserFormMixin, BaseModelForm):
    SUBMIT_TEXT = _('Save Employee Overtime')

    class Meta(BaseModelForm.Meta):
        model = EmployeeOvertime
        fields = '__all__'
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        hidden_in_create_fields=['hours']