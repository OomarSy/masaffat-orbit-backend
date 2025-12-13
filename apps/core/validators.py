import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()

def validate_syria_phone(phone):
    pattern = re.compile(r"^(?:\+963|0)9\d{8}$")
    if not pattern.match(phone):
        raise ValidationError(_("Phone number must be a valid Syrian number starting with +9639 or 09."))

def validate_password_strength(password):
    if len(password) < 8:
        raise serializers.ValidationError(_("Password must be at least 8 characters long."))