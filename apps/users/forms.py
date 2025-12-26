from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import User

from apps.core.forms import BaseModelForm


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
        fields = ['username', 'is_active', 'is_staff', 'is_superuser', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 8:
            raise forms.ValidationError(_("يجب أن تكون كلمة المرور 8 أحرف على الأقل."))
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user