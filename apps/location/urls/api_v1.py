from django.urls import path

from ..views import apis_views


urlpatterns = [
    
    # mobile api paths
    path('update/location/', apis_views.UpdateLocationAPI_V1.as_view(), name='update_location_api'),
    
    # cms api paths
    path('cms/employee-locations/', apis_views.EmployLocationsAPI_V1.as_view(), name='employee_locations_api_v1'),
    path('cms/employee-locations-history/', apis_views.EmployeeLocationHistoryAPI_V1.as_view(), name='employee_locations_history_api_v1')

]
