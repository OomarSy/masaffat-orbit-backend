from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from tablib import Dataset
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.http import HttpResponse


class BaseCRUDView(LoginRequiredMixin):
    """
    Base class for CRUD CBVs
    """
    model = None
    form_class = None
    template_name = 'generic/form.html'
    success_url = None
    view_name = None  # For template context

    def get_success_url(self):
        return self.success_url or reverse_lazy(
            f'{self.model._meta.app_label}:{self.model._meta.model_name}_list'
        )

    def get_breadcrumbs(self):
        """
        Default breadcrumb: Home > Model List > Current Page
        """
        breadcrumbs = [{'name': 'Home', 'url': reverse_lazy('index')}]

        # List page
        list_url = reverse_lazy(f'{self.model._meta.app_label}:{self.model._meta.model_name}_list')
        list_name = self.model._meta.verbose_name_plural.title()
        breadcrumbs.append({'name': list_name, 'url': list_url})

        # Current view name (Create/Update/Detail/Delete)
        if self.view_name:
            breadcrumbs.append({'name': self.view_name, 'url': ''})

        return breadcrumbs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = self.view_name
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context


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
        """
        Export only fields defined in the table_class (Meta.fields).
        """
        dataset = Dataset()
        qs = self.get_queryset()

        if self.table_class and hasattr(self.table_class.Meta, "fields"):
            fields = list(self.table_class.Meta.fields)
        else:
            fields = self.export_fields or [f.name for f in self.model._meta.fields]

        dataset.headers = fields

        for obj in qs:
            row = [getattr(obj, f) for f in fields]
            dataset.append(row)

        response = HttpResponse(dataset.export("csv"), content_type="text/csv")
        response["Content-Disposition"] = (
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
        return context