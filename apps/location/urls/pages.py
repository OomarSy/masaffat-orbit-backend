from django.urls import path

from ..views import pages_views


urlpatterns = [
    
    path('cms/employee-locations/', pages_views.EmployeeLocationsPageView.as_view(), name='employee_locations_page'),
    path('cms/employee-locations-history/', pages_views.EmployeeLocationsHistoryPageView.as_view(), name='employee_locations_history'),

]
