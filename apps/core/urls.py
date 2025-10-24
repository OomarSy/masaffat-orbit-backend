from django.urls import path

from apps.core.views import (CreateUser, DeleteUser, DetailsUser, ListUser, LoginAPI_V1, LogoutAPI_V1, SignupAPI_V1, UpdateUser, UserLoginView, TokenRefreshAPI_V1)
from django.urls import path
from apps.core.views import logout_view

urlpatterns = [
    
    #auth_api's
    path('auth/api/v1/signup/', SignupAPI_V1.as_view(), name='signup_request_api'),
    path('auth/api/v1/login/', LoginAPI_V1.as_view(), name='login_api'),
    path('auth/api/v1/logout/', LogoutAPI_V1.as_view(), name='logout_api'),
    path('auth/api/v1/refresh/token/', TokenRefreshAPI_V1.as_view(), name='refresh_token_api'),
    
    path('users/', ListUser.as_view(), name='user_list'),
    path('users/create/', CreateUser.as_view(), name='user_create'),
    path('users/<int:pk>/', DetailsUser.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', UpdateUser.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', DeleteUser.as_view(), name='user_delete'),
    
    #pages
    path('accounts/login/', UserLoginView.as_view(), name="login"),
    path('accounts/logout/', logout_view, name="logout"),

]
