from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django import forms

from base.forms import BaseModelForm
from .models import User



class LoginForm(AuthenticationForm):
  username = UsernameField(label=_("Your Username"), widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  password = forms.CharField(
      label=_("Your Password"),
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
  )


class UserForm(BaseModelForm):
    SUBMIT_TEXT = _('Save User')

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('Enter new password')})
    )
    
    class Meta(BaseModelForm.Meta):
        model = User
        fields = ['username', 'is_active', 'is_staff', 'is_superuser']