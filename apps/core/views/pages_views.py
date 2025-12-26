from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.utils import timezone

from datetime import datetime
from tablib import Dataset


class BaseCRUDView(LoginRequiredMixin):
    model = None
    form_class = None
    template_name = 'generic/form.html'
    success_url = None
    view_name = None
    segment = None

    details = False
    edit = False
    create = False
    visible_fields = None

    def form_valid(self, form):
        """
        Set user_created automatically for new records.
        """
        if not form.instance.pk:
            form.instance._current_user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.success_url or reverse_lazy(
            f'{self.model._meta.app_label}:{self.model._meta.model_name}_list'
        )

    def get_form_kwargs(self):
        """Return kwargs to instantiate form"""
        kwargs = super().get_form_kwargs() if hasattr(super(), "get_form_kwargs") else {}

        kwargs['details'] = getattr(self, 'details', False)
        kwargs['edit'] = getattr(self, 'edit', False)
        kwargs['create'] = getattr(self, 'create', False)
        kwargs['visible_fields'] = getattr(self, 'visible_fields', None)
        kwargs['cancel_url'] = self.success_url

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'form' not in context and self.form_class:
            context['form'] = self.get_form() if hasattr(self, 'get_form') else self.form_class(
                instance=getattr(self, 'object', None),
                **self.get_form_kwargs()
            )

        context['details'] = getattr(self, 'details', False)
        context['edit'] = getattr(self, 'edit', False)
        context['create'] = getattr(self, 'create', False)

        context['segment'] = self.segment or self.model._meta.model_name
        context['view_name'] = self.view_name
        context['breadcrumbs'] = self.get_breadcrumbs()

        return context

    def get_breadcrumbs(self):
        breadcrumbs = [{'name': 'Home', 'url': reverse_lazy('index')}]
        list_url = reverse_lazy(f'{self.model._meta.app_label}:{self.model._meta.model_name}_list')
        list_name = self.model._meta.verbose_name_plural.title()
        breadcrumbs.append({'name': list_name, 'url': list_url})
        if self.view_name:
            breadcrumbs.append({'name': self.view_name, 'url': ''})
        return breadcrumbs

    def form_invalid(self, form):
        """Return form with errors"""
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
    

class BaseListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    """
    Base List View with table, filter, breadcrumbs, and export (CSV/XLS) using django-import-export.
    """
    model = None
    table_class = None
    filterset_class = None
    template_name = 'generic/list.html'
    view_name = None
    add_url_name = None
    export_fields = None  # List of fields to export, default None = all fields
    segment = None
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('id')  # Default ordering by 'id'
        if self.filterset_class:
            self.filterset = self.filterset_class(self.request.GET, queryset=qs)
            return self.filterset.qs
        return qs


    def get_table_data(self):
        # Ensure table gets filtered queryset
        return self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = self.segment or self.request.resolver_match.app_name

        # Add export URL
        query_params = self.request.GET.copy()
        query_params['_export'] = 'csv'
        context['export_url'] = reverse_lazy(
            f'{self.model._meta.app_label}:{self.model._meta.model_name}_list'
        ) + '?' + query_params.urlencode()

        if self.add_url_name:
            context['add_url'] = reverse_lazy(self.add_url_name)

        context['view_name'] = self.view_name
        context['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse_lazy('dashboard:index')},
            {'name': self.view_name, 'url': ''},
        ]

        # Add filterset instance for template
        if self.filterset_class:
            context['filter'] = self.filterset

        return context

    
    def export_data(self):
        dataset = Dataset()
        qs = self.get_queryset()

        if self.export_fields:
            fields = self.export_fields

        elif self.table_class and hasattr(self.table_class.Meta, "fields"):
            fields = self.table_class.Meta.fields

        else:
            fields = [f.name for f in self.model._meta.fields]

        dataset.headers = fields

        for obj in qs:
            row = []
            for field_name in fields:
                value = getattr(obj, field_name)

                if isinstance(value, datetime):
                    value = timezone.localtime(value)
                    value = value.replace(microsecond=0, tzinfo=None)

                row.append(value)

            dataset.append(row)

        response = HttpResponse(
            dataset.export('csv').encode('utf-8-sig'),
            content_type='text/csv'
        )
        response['Content-Disposition'] = (
            f'attachment; filename="{self.model._meta.model_name}_export.csv"'
        )
        return response


    def get(self, request, *args, **kwargs):
        if '_export' in request.GET:
            return self.export_data()
        return super().get(request, *args, **kwargs)
    

class BaseDeleteView(LoginRequiredMixin, DeleteView):
    """
    Base Delete View with breadcrumbs, fields, and back_url.
    """
    template_name = 'generic/confirm_delete.html'
    view_name = None
    hide_fields = ['id']  # Default: hide the 'id' field

    def delete(self, request, *args, **kwargs):
        """
        Override to perform soft delete instead of actual delete.
        """
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy(f'{self.model._meta.app_label}:{self.model._meta.model_name}_list')

    def get_back_url(self):
        """
        URL to go back to when clicking Cancel.
        """
        return reverse_lazy(f'{self.model._meta.app_label}:{self.model._meta.model_name}_list')

    def get_fields(self):
        """
        Prepare fields to display in the template, excluding hidden fields.
        """
        return [
            {'name': field.verbose_name, 'value': getattr(self.object, field.name)}
            for field in self.model._meta.fields
            if field.name not in getattr(self, 'hide_fields', [])
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = self.view_name
        context['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse_lazy('dashboard:index')},
            {'name': self.model._meta.verbose_name_plural.title(), 'url': self.get_success_url()},
            {'name': self.view_name or "Delete", 'url': ''},
        ]
        context['fields'] = self.get_fields()
        context['back_url'] = self.get_back_url()
        
        context['segment'] = getattr(self, 'segment', self.model._meta.app_label)
        
        return context