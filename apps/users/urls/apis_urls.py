from django.urls import path

from ..views import apis_views


urlpatterns = [
    
    path('auth/api/v1/signup/', apis_views.SignupAPI_V1.as_view(), name='signup_request_api'),
    path('auth/api/v1/login/', apis_views.LoginAPI_V1.as_view(), name='login_api'),
    path('auth/api/v1/logout/', apis_views.LogoutAPI_V1.as_view(), name='logout_api'),
    path('auth/api/v1/refresh/token/', apis_views.TokenRefreshAPI_V1.as_view(), name='refresh_token_api'),

]
