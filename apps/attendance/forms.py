from django import forms
from django.utils.translation import gettext_lazy as _

from apps.attendance.models import Attendance, Overtime

from base.mixins import ActiveNormalUserFormMixin
from base.forms import BaseModelForm


  
class AttendanceForm(ActiveNormalUserFormMixin,BaseModelForm):
    SUBMIT_TEXT = _('Save Attendance')

    class Meta(BaseModelForm.Meta):
        model = Attendance
        fields = '__all__'
        widgets = {
            'checkin_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'checkout_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class OvertimeForm(ActiveNormalUserFormMixin, BaseModelForm):
    SUBMIT_TEXT = _('Save Overtime')

    class Meta(BaseModelForm.Meta):
        model = Overtime
        fields = '__all__'
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        hidden_in_create_fields=['hours']