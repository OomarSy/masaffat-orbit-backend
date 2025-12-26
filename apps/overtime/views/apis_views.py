from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status

from ..services.overtime_service import ListOvertimeService, OvertimeService
from ..serializers import OvertimeEntrySerializer
from ..serializers import OvertimeSerializer

from apps.core.pagination import SmallResultsPagination
from apps.core.utils import api_response

class OvertimeAPI_V1(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        entries = request.data.get("entries", [])

        if not isinstance(entries, list) or not entries:
            return api_response(
                errorno=1,
                message="يرجى تمرير قائمة صحيحة من الإدخالات.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = OvertimeEntrySerializer(data=entries, many=True)
        if not serializer.is_valid():
            return api_response(
                errorno=2,
                message="خطأ في التحقق من البيانات.",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        errors = OvertimeService.validate_entries(
            request.user,
            serializer.validated_data
        )

        if errors:
            return api_response(
                errorno=3,
                message="فشل تسجيل الدوام الإضافي بسبب أخطاء في الإدخال.",
                data={"errors": errors},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        created = OvertimeService.create_overtime(
            request.user,
            serializer.validated_data
        )

        return api_response(
            errorno=0,
            message="تم تسجيل الدوام الإضافي بنجاح.",
            data={"created": created},
            status_code=status.HTTP_201_CREATED
        )


class UserOvertimeListAPI_v1(ListAPIView):
    serializer_class = OvertimeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallResultsPagination

    def get_queryset(self):
        return ListOvertimeService.get_user_overtimes(
            user=self.request.user,
            from_date=self.request.GET.get("from_date"),
            to_date=self.request.GET.get("to_date"),
        )

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return api_response(
                errorno=0,
                message="تم جلب البيانات",
                data=response.data
            )
        except ValueError as e:
            return api_response(
                errorno=1,
                message=f"خطأ في البيانات المدخلة: {str(e)}",
                data={}
            )
        except PermissionError as e:
            return api_response(
                errorno=2,
                message="ليس لديك صلاحية الوصول لهذه البيانات.",
                data={}
            )
        except Exception as e:
            return api_response(
                errorno=99,
                message=f"حدث خطأ غير متوقع",
                data={}
            )
