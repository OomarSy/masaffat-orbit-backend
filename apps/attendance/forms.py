from django import forms
from django.utils.translation import gettext_lazy as _

from apps.attendance.models import EmployeeAttendance

from apps.core.mixins import ActiveNormalUserFormMixin
from apps.core.forms import BaseModelForm


  
class EmployeeAttendanceForm(ActiveNormalUserFormMixin,BaseModelForm):
    SUBMIT_TEXT = _('Save Employee Attendance')

    class Meta(BaseModelForm.Meta):
        model = EmployeeAttendance
        fields = '__all__'
        widgets = {
            'checkin_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'checkout_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }