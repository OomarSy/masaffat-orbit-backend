from django.urls import path

from ..views import pages_views

app_name = "appversion"

urlpatterns = [
    
    # App Version Paths
    path('list', pages_views.ListAppVersion.as_view(), name='appversion_list'),
    path('details/<int:pk>', pages_views.DetailsAppVersion.as_view(), name='appversion_detail'),
    path('create/', pages_views.CreateAppVersion.as_view(), name='appversion_create'),
    path('update/<int:pk>', pages_views.UpdateAppVersion.as_view(), name='appversion_update'),
    path('delete/<int:pk>', pages_views.DeleteAppVersion.as_view(), name='appversion_delete'),
]
