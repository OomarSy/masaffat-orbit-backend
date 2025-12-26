from django import forms
from django.utils.translation import gettext_lazy as _

from apps.attendance.models import Attendance

from apps.core.mixins import ActiveNormalUserFormMixin
from apps.core.forms import BaseModelForm


  
class AttendanceForm(ActiveNormalUserFormMixin,BaseModelForm):
    SUBMIT_TEXT = _('Save Attendance')

    class Meta(BaseModelForm.Meta):
        model = Attendance
        fields = '__all__'
        widgets = {
            'checkin_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'checkout_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }