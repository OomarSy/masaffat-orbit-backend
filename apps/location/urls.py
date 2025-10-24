from django.urls import path

from apps.location.views import CMSUserLocationsAPI, UpdateLocationAPI_V1, UserLocationsPageView


urlpatterns = [
    
    path('api/v1/update/location/', UpdateLocationAPI_V1.as_view(), name='update_location_api'),
    path('cms/user-locations/', CMSUserLocationsAPI.as_view(), name='cms-user-locations'),
    
    path('cms/map/', UserLocationsPageView.as_view(), name='cms-user-locations-page'),

]
