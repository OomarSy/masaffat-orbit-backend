from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Field
from crispy_forms.layout import Submit, Layout, Field
from django.utils.translation import gettext_lazy as _


class BaseModelForm(forms.ModelForm):
    SUBMIT_TEXT = _('Submit')
    CANCEL_TEXT = _('Cancel')

    BUTTON_CSS = 'btn btn-primary'
    CANCEL_CSS = 'btn btn-secondary'

    def __init__(self, details=False, cancel_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.details = details
        self.cancel_url = cancel_url

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'row g-3'
        self.helper.label_class = 'col-form-label col-md-3'
        self.helper.field_class = 'col-md-9'

        layout_fields = []
        for name, field in self.fields.items():
            if details:
                field.disabled = True
            layout_fields.append(Field(name))

        self.helper.layout = Layout(
            *layout_fields,
            Layout(
                Field('submit_buttons', template='generic/form_buttons.html')
            )
        )

        if not details:
            self.helper.add_input(
                Submit('submit', self.SUBMIT_TEXT, css_class=self.BUTTON_CSS)
            )
            self.helper.add_input(
                Button('cancel', self.CANCEL_TEXT, css_class=self.CANCEL_CSS, onclick=f"window.location='{cancel_url or 'javascript:history.back()'}';")
            )