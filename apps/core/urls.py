from django.urls import path

from apps.core import views


urlpatterns = [
    
    # User Management Paths
    path('users/', views.ListUser.as_view(), name='user_list'),
    path('users/create/', views.CreateUser.as_view(), name='user_create'),
    path('users/<int:pk>/', views.DetailsUser.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', views.UpdateUser.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.DeleteUser.as_view(), name='user_delete'),
    
    #auth_api's
    path('auth/api/v1/signup/', views.SignupAPI_V1.as_view(), name='signup_request_api'),
    path('auth/api/v1/login/', views.LoginAPI_V1.as_view(), name='login_api'),
    path('auth/api/v1/logout/', views.LogoutAPI_V1.as_view(), name='logout_api'),
    path('auth/api/v1/refresh/token/', views.TokenRefreshAPI_V1.as_view(), name='refresh_token_api'),
    
    #pages
    path('accounts/login/', views.UserLoginView.as_view(), name="login"),
    path('accounts/logout/', views.logout_view, name="logout"),

]
