from django.urls import path

from ..views import pages_views


urlpatterns = [
    
    path('cms/map/', pages_views.UserLocationsPageView.as_view(), name='cms-user-locations-page'),

]
