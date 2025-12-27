from django.urls import path

from ..views import pages_views


urlpatterns = [
    
    path('cms/map/', pages_views.EmployeeLocationsPageView.as_view(), name='Employee_Locations_Page'),

]
