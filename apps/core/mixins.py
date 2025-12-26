from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()

class SoftDeleteUniqueMixin:
    """
    Mixin to allow unique fields to ignore soft-deleted records.
    Usage:
        class MyModel(SoftDeleteUniqueMixin, BaseModel):
            unique_fields = ['name']
    """
    unique_fields: list = []

    def clean(self):
        super().clean()
        if not self.unique_fields:
            return

        for field_name in self.unique_fields:
            value = getattr(self, field_name)
            qs = self.__class__.all_objects.filter(**{field_name: value, 'is_deleted': False})
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({field_name: f"This {field_name} already exists."})


class ActiveNormalUserFilterMixin:
    """
    Mixin to limit the 'user' filter to active normal users (not staff or superuser).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'user' in getattr(self, 'filters', {}):
            self.filters['user'].queryset = User.objects.filter(
                is_active=True, is_staff=False, is_superuser=False
            )


class ActiveNormalUserFormMixin:
    """
    Mixin to limit a user field to active normal users (not staff or superuser).
    """
    user_field_name = 'user'  # Default field name, يمكن تغييره عند الحاجة

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_field_name in self.fields:
            self.fields[self.user_field_name].queryset = User.objects.filter(
                is_active=True, is_staff=False, is_superuser=False
            )