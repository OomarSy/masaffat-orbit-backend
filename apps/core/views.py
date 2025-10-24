import json

from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from base.views import BaseListView, BaseCRUDView, BaseDeleteView
from apps.core.models import User
from apps.core.forms import UserForm
from apps.core.filters import UserFilter
from apps.core.tables import UserTable
from django.db import IntegrityError, transaction
from django.contrib.auth.views import LoginView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.core.cache import cache
from django.utils import timezone

from apps.core.forms import LoginForm

from apps.core.serializers import (LoginSerializer, LogoutSerializer, SignupRequestSerializer)

from base.utils import api_response

User = get_user_model()


class SignupAPI_V1(APIView):
    serializer_class = SignupRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return api_response(
                errorno=1,
                message=_("Validation error."),
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        username = data.get("username")

        if User.objects.filter(username=username).exists():
            return api_response(
                errorno=5,
                message=_("An account with this username already exists."),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    password=data.get("password"),
                )
        except IntegrityError as e:
            return api_response(
                errorno=7,
                message=_("An unexpected error occurred while creating the account. Please try again."),
                data=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        refresh = RefreshToken.for_user(user)

        return api_response(
            errorno=0,
            message=_("Account created successfully."),
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class LoginAPI_V1(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return api_response(
                errorno=1,
                message=_("Validation error."),
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request=request, username=username, password=password)
        if user is None:
            return api_response(
                errorno=2,
                message=_("Invalid username or password."),
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        cache_key = f"delete_request:{user.id}"
        if cache.get(cache_key):
            cache.delete(cache_key)
            message = _("You have successfully logged in. Your pending account deletion request has been canceled.")
        else:
            message = _("You have successfully logged in.")

        refresh = RefreshToken.for_user(user)

        return api_response(
            errorno=0,
            message=message,
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class LogoutAPI_V1(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return api_response(
                errorno=1,
                message=_("Validation error."),
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        refresh = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return api_response(
                errorno=0,
                message=_("Logout successful.")
            )
        except TokenError:
            return api_response(
                errorno=2,
                message=_("The token is invalid or has expired. Please log in again."),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class TokenRefreshAPI_V1(TokenRefreshView):

    def handle_exception(self, exc):
        if isinstance(exc, (InvalidToken, TokenError)):
            return api_response(
                errorno=2,
                message="Token is invalid",
                data={"code": "token_not_valid"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        return super().handle_exception(exc)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return api_response(
                errorno=0,
                message="Token refreshed successfully",
                data=response.data
            )
        return response


class ListUser(BaseListView):
    model = User
    table_class = UserTable
    filterset_class = UserFilter
    view_name = "Users"
    add_url_name = 'core:user_create'


class DetailsUser(BaseCRUDView, DetailView):
    model = User
    form_class = UserForm
    template_name = 'generic/form.html'
    view_name = "User Details"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['details'] = True
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = True
        context['form'] = self.form_class(instance=self.object, details=True)
        return context


class CreateUser(BaseCRUDView, CreateView):
    model = User
    form_class = UserForm
    template_name = 'generic/form.html'
    success_url = reverse_lazy('core:user_list')
    view_name = "Create User"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.set_password(form.cleaned_data.get('password') or "defaultpass")
        instance.save()
        return super().form_valid(form)


class UpdateUser(BaseCRUDView, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'generic/form.html'
    success_url = reverse_lazy('core:user_list')
    view_name = "Update User"


class DeleteUser(BaseDeleteView):
    model = User
    view_name = "Delete User"


#views
#cms login view
class UserLoginView(LoginView):
  form_class = LoginForm
  template_name = 'pages/accounts/sign-in.html'

#cms logout view
def logout_view(request):
  logout(request)
  return redirect('/core/accounts/login/')
  
# Index view
def index(request):
    return render(request, 'pages/index.html')