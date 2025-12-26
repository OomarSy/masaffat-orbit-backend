from django.urls import path

from ..views import pages_views


urlpatterns = [
    
    # App Version Paths
    path('appversion/list', pages_views.ListAppVersion.as_view(), name='appversion_list'),
    path('appversion/details/<int:pk>', pages_views.DetailsAppVersion.as_view(), name='appversion_detail'),
    path('appversion/create/', pages_views.CreateAppVersion.as_view(), name='appversion_create'),
    path('appversion/update/<int:pk>', pages_views.UpdateAppVersion.as_view(), name='appversion_update'),
    path('appversion/delete/<int:pk>', pages_views.DeleteAppVersion.as_view(), name='appversion_delete'),
]
