from django.contrib import admin
from django.conf import settings
from django.views.static import serve
import os
from django.views.static import serve
from django.urls import include, path, re_path
from apps.core.views import index
from config import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('dashboard/', include(('apps.dashboard.urls', 'dashboard'), namespace="dashboard")),
    
    path("admin/", admin.site.urls),
    path('', index, name="index"),
    path("", include('admin_volt.urls')),
    
    
    #Apps URLs
    path('core/', include(('apps.core.urls', 'core'), namespace="core")),
    path('location/', include(('apps.location.urls', 'location'), namespace="location")),
    path('attendance/', include(('apps.attendance.urls', 'attendance'), namespace="attendance")),
    path('appversion/', include(('apps.appversion.urls', 'appversion'), namespace="appversion")),
    
    #media
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
]
