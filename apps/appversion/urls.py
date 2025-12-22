from django.urls import path

from apps.appversion import views


urlpatterns = [
    
    # App Version Paths
    path('appversion/list', views.ListAppVersion.as_view(), name='appversion_list'),
    path('appversion/details/<int:pk>', views.DetailsAppVersion.as_view(), name='appversion_detail'),
    path('appversion/create/', views.CreateAppVersion.as_view(), name='appversion_create'),
    path('appversion/update/<int:pk>', views.UpdateAppVersion.as_view(), name='appversion_update'),
    path('appversion/delete/<int:pk>', views.DeleteAppVersion.as_view(), name='appversion_delete'),
    
    # mobile api paths
    path('api/v1/app/version/check/', views.AppUpdateCheckAPI_V1.as_view(), name='app_update_check_api_v1'),

]
