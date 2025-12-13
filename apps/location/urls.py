from django.urls import path

from apps.location import views


urlpatterns = [
    
    # mobile api paths
    path('api/v1/update/location/', views.UpdateLocationAPI_V1.as_view(), name='update_location_api'),
    
    # cms api paths
    path('cms/user-locations/', views.CMSUserLocationsAPI_V1.as_view(), name='cms-user-locations'),
    
    # cms page views
    path('cms/map/', views.UserLocationsPageView.as_view(), name='cms-user-locations-page'),

]
