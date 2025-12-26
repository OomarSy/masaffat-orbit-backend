from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse

import django_tables2 as tables


BUTTON_COLORS = {
    'view': '#3B82F6',
    'edit': '#10B981',
    'delete': '#EF4444',
}

BUTTON_HOVER = {
    'view': '#2563EB',
    'edit': '#059669',
    'delete': '#DC2626',
}

COMMON_BUTTON_STYLE = (
    "display: inline-flex; "
    "align-items: center; "
    "justify-content: center; "
    "padding: 0.35rem 0.65rem; "
    "font-size: 0.75rem; "
    "font-weight: 600; "
    "border-radius: 0.375rem; "
    "border: 1px solid transparent; "
    "color: white; "
    "white-space: nowrap; "
    "margin: 0 2px; "
    "cursor: pointer; "
    "transition: background-color 0.2s, transform 0.15s;"
)


class BaseTable(tables.Table):
    action = tables.Column(empty_values=(), orderable=False, exclude_from_export=True)

    def _render_button(self, record, button_type):
        btn = self.BUTTONS.get(button_type)
        if not btn or not btn.get('url_name'):
            return format_html('<span style="color: #ccc;">{}</span>', btn['label'] if btn else '')
        url = reverse(btn['url_name'], args=[record.id])
        style = f"{COMMON_BUTTON_STYLE} background-color: {BUTTON_COLORS[button_type]};"
        hover_color = BUTTON_HOVER[button_type]
        return format_html(
            '<a href="{}" class="btn" style="{}" '
            'onmouseover="this.style.backgroundColor=\'{}\'" '
            'onmouseout="this.style.backgroundColor=\'{}\'">{}</a>',
            url, style, hover_color, BUTTON_COLORS[button_type], btn['label']
        )

    def render_action(self, record):
        return format_html(
            "{} {} {}",
            self._render_button(record, 'view'),
            self._render_button(record, 'edit'),
            self._render_button(record, 'delete'),
        )

    class Meta:
        template_name = "django_tables2/bootstrap5-responsive.html"
        per_page = 10
        attrs = {
            "thead": {"class": "thead-light", "style": "text-align: center;"},
            "td": {"style": "text-align: center; vertical-align: middle;"},
            "th": {"style": "text-align: center; vertical-align: middle;"},
        }