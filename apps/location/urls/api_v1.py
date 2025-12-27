from django.urls import path

from ..views import apis_views


urlpatterns = [
    
    # mobile api paths
    path('update/location/', apis_views.UpdateLocationAPI_V1.as_view(), name='update_location_api'),
    
    # cms api paths
    path('cms/user-locations/', apis_views.CMSUserLocationsAPI_V1.as_view(), name='cms_user_locations_api_v1'),
    

]
