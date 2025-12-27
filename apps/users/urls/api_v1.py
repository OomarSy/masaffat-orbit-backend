from django.urls import path

from ..views import apis_views

app_name = "users-api-v1"

urlpatterns = [
    
    path('signup/', apis_views.SignupAPI_V1.as_view(), name='signup_api_v1'),
    path('login/', apis_views.LoginAPI_V1.as_view(), name='login_api_v1'),
    path('logout/', apis_views.LogoutAPI_V1.as_view(), name='logout_api_v1'),
    path('token/refresh/', apis_views.TokenRefreshAPI_V1.as_view(), name='token_refresh_api_v1'),

]
