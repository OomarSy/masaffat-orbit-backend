from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils import timezone

from ..serializers import (LoginSerializer, LogoutSerializer, SignupRequestSerializer)

from ..models import User

from apps.core.utils import api_response

User = get_user_model()


# API Views
class SignupAPI_V1(APIView):
    serializer_class = SignupRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return api_response(
                errorno=1,
                message=_("خطأ في التحقق من البيانات."),
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        username = data.get("username")

        if User.objects.filter(username=username).exists():
            return api_response(
                errorno=5,
                message=_("يوجد حساب بالفعل بهذا الاسم."),
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
                message=_("حدث خطأ أثناء إنشاء الحساب."),
                data=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        refresh = RefreshToken.for_user(user)

        return api_response(
            errorno=0,
            message=_("تم إنشاء الحساب بنجاح."),
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
                message=_("خطأ في التحقق من البيانات."),
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
                message=_("خطأ في اسم المستخدم أو كلمة المرور."),
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        cache_key = f"delete_request:{user.id}"
        if cache.get(cache_key):
            cache.delete(cache_key)
            message = _("تم تسجيل الدخول بنجاح. لاحظ أن لديك طلب حذف حساب معلق تم إلغاؤه.")
        else:
            message = _("تم تسجيل الدخول بنجاح.")

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
                message=_("خطأ في التحقق من البيانات."),
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        refresh = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return api_response(
                errorno=0,
                message=_("تم تسجيل الخروج بنجاح."),
            )
        except TokenError:
            return api_response(
                errorno=2,
                message=_("التوكن غير صالح أو منتهي."),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class TokenRefreshAPI_V1(TokenRefreshView):

    def handle_exception(self, exc):
        if isinstance(exc, (InvalidToken, TokenError)):
            return api_response(
                errorno=2,
                message="التوكن غير صالح أو منتهي.",
                data={"code": "token_not_valid"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        if isinstance(exc, ValidationError):
            field_errors = {}

            for field, msgs in exc.detail.items():
                field_errors[field] = [str(msg) for msg in msgs]

            return api_response(
                errorno=3,
                message="بيانات الطلب غير صالحة.",
                data=field_errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )


        return api_response(
            errorno=99,
            message="خطأ غير متوقع، يرجى المحاولة لاحقًا.",
            data=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)

            return api_response(
                errorno=0,
                message="تم تحديث التوكن بنجاح.",
                data=response.data,
                status_code=status.HTTP_200_OK
            )

        except Exception as exc:
            return self.handle_exception(exc)