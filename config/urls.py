from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import include, path, re_path
from apps.users.views.pages_views import index

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('dashboard/pages/', include(('apps.dashboard.urls.pages_urls', 'dashboard-pages'), namespace="dashboard-pages")),
    
    path("admin/", admin.site.urls),
    
    path('', index, name="index"),
    
    path("", include('admin_volt.urls')),
    
    
    #Apps URLs
    path('users/pages/', include(('apps.users.urls.pages_urls', 'users-pages'), namespace="users-pages")),
    path('users/api/', include(('apps.users.urls.apis_urls', 'users-apis'), namespace="users-apis")),
    
    path('location/pages/', include(('apps.location.urls.pages_urls', 'location-pages'), namespace="location-pages")),
    path('location/api/', include(('apps.location.urls.apis_urls', 'location-apis'), namespace="location-apis")),
    
    path('attendance/pages/', include(('apps.attendance.urls.pages_urls', 'attendance-pages'), namespace="attendance-pages")),
    path('attendance/api/', include(('apps.attendance.urls.apis_urls', 'attendance-apis'), namespace="attendance-apis")),
    
    path('appversion/pages/', include(('apps.appversion.urls.pages_urls', 'appversion-pages'), namespace="appversion-pages")),
    path('appversion/api/', include(('apps.appversion.urls.apis_urls', 'appversion-apis'), namespace="appversion-apis")),
    
    #media
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
]
