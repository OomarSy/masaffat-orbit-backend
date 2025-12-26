import math

from django.utils import timezone
from django.conf import settings

from apps.attendance.models import Attendance


class AttendanceService:

    @staticmethod
    def calculate_distance_m(lat1, lon1, lat2, lon2):
        R = 6371000  # meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    @staticmethod
    def get_today_attendance(user):
        today = timezone.now().date()
        return Attendance.objects.filter(
            user=user,
            checkin_time__date=today
        ).first()

    @staticmethod
    def is_weekend():
        today = timezone.now().weekday()   # Monday=0 ... Sunday=6
        return today in settings.WEEKEND_DAYS
    
    @staticmethod
    def checkin(user, latitude, longitude):
        
        if AttendanceService.is_weekend():
            return {
                "status": "weekend",
                "message": "عذراً، لا يمكن تسجيل الدوام في أيام العطلة (الجمعة والسبت)."
            }
        
        company_lat = settings.COMPANY_LATITUDE
        company_lon = settings.COMPANY_LONGITUDE
        radius = settings.COMPANY_RADIUS_METERS

        # distance check
        distance = AttendanceService.calculate_distance_m(
            latitude, longitude, company_lat, company_lon
        )

        if distance > radius:
            return {
                "status": "out_of_range",
                "message": "عذراً، لا يمكن تسجيل الدوام خارج موقع الشركة."
            }

        today_attendance = AttendanceService.get_today_attendance(user)
        if today_attendance:
            return {
                "status": "already_checked_in",
                "message": "لقد تم تسجيل الدوام مسبقاً اليوم."
            }

        Attendance.objects.create(user=user)
        return {
            "status": "success",
            "message": "تم تسجيل الدوام بنجاح."
        }

    @staticmethod
    def checkout(user, latitude, longitude):
        
        if AttendanceService.is_weekend():
            return {
                "status": "weekend",
                "message": "لا يمكن تسجيل الخروج خلال أيام العطلة."
            }
        
        company_lat = settings.COMPANY_LATITUDE
        company_lon = settings.COMPANY_LONGITUDE
        radius = settings.COMPANY_RADIUS_METERS

        # check distance
        distance = AttendanceService.calculate_distance_m(
            latitude, longitude, company_lat, company_lon
        )

        if distance > radius:
            return {
                "status": "out_of_range",
                "message": "عذراً، لا يمكن تسجيل الخروج خارج موقع الشركة."
            }

        today_attendance = AttendanceService.get_today_attendance(user)

        if not today_attendance:
            return {
                "status": "no_checkin",
                "message": "لا يمكن تسجيل الخروج قبل تسجيل الدخول."
            }

        if today_attendance.checkout_time:
            return {
                "status": "already_checked_out",
                "message": "تم تسجيل الخروج مسبقاً اليوم."
            }

        today_attendance.checkout_time = timezone.now()
        today_attendance.save()

        return {
            "status": "success",
            "message": "تم تسجيل الخروج بنجاح."
        }