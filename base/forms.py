from django.utils.translation import gettext_lazy as _
from django import forms

from crispy_forms.layout import Submit, Button, Layout, Field
from crispy_forms.helper import FormHelper


class BaseModelForm(forms.ModelForm):
    SUBMIT_TEXT = _('Submit')
    CANCEL_TEXT = _('Cancel')
    BUTTON_CSS = 'btn btn-primary'
    CANCEL_CSS = 'btn btn-secondary'

    SYSTEM_FIELDS = ['created_at', 'updated_at', 'user_created', 'date_joined', 'last_login']
    EXCLUDE_FIELDS = ['is_deleted']
    
    class Meta:
        model = None
        exclude = ['is_deleted']
        hidden_in_create_fields = []

    def __init__(self, details=False, edit=False, create=False, visible_fields=None, cancel_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.details = details
        self.edit = edit
        self.create = create
        self.cancel_url = cancel_url

        for field_name in self.EXCLUDE_FIELDS:
            if field_name in self.fields:
                self.fields.pop(field_name)

        for field_name in self.SYSTEM_FIELDS:
            if hasattr(self._meta.model, field_name) and field_name not in self.fields:
                model_field = self._meta.model._meta.get_field(field_name)
                if field_name == 'user_created' and model_field.remote_field:
                    initial_value = getattr(self.instance, field_name, None)
                    display_value = str(initial_value) if initial_value else ''
                    self.fields[field_name] = forms.CharField(
                        disabled=True,
                        required=False,
                        initial=display_value,
                        label=getattr(model_field, 'verbose_name', field_name)
                    )
                else:
                    self.fields[field_name] = forms.CharField(
                        disabled=True,
                        required=False,
                        initial=getattr(self.instance, field_name, None) if self.instance else None,
                        label=getattr(model_field, 'verbose_name', field_name)
                    )

        hidden_in_create_fields = getattr(getattr(self.Meta, 'hidden_in_create_fields', None), 'copy', lambda: [])()
        if create and hidden_in_create_fields:
            for field_name in hidden_in_create_fields:
                if field_name in self.fields:
                    self.fields.pop(field_name)
        
        if details:
            for field in self.fields.values():
                field.disabled = True

        if visible_fields:
            for name in list(self.fields.keys()):
                if name not in visible_fields:
                    self.fields.pop(name)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'row g-3'
        self.helper.label_class = 'col-form-label'
        self.helper.field_class = 'col-md-9'

        layout_fields = [Field(name) for name in self.fields]
        self.helper.layout = Layout(*layout_fields)

        if not details:
            self.helper.add_input(Submit('submit', self.SUBMIT_TEXT, css_class=self.BUTTON_CSS))
            self.helper.add_input(
                Button('cancel', self.CANCEL_TEXT, css_class=self.CANCEL_CSS,
                       onclick=f"window.location='{cancel_url or 'javascript:history.back()'}';")
            )
