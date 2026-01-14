from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime

from decimal import Decimal

from apps.core.mixins import SoftDeleteUniqueMixin
from apps.core.models import BaseModel

User = get_user_model()


class EmployeeOvertime(SoftDeleteUniqueMixin, BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_overtimes")
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    date = models.DateField(null=True, blank=True)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_datetime']

    def save(self, *args, **kwargs):
        if self.start_datetime and self.end_datetime:
            delta = self.end_datetime - self.start_datetime
            self.hours = Decimal(delta.total_seconds() / 3600).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)
    
    @property
    def day_name(self):
        """
        اسم اليوم بالإنجليزية
        """
        dt = self.start_datetime or self.date
        if dt:
            # إذا dt هو date فقط بدون وقت
            if isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime):
                from datetime import datetime
                dt = datetime.combine(dt, datetime.min.time())
            return dt.strftime("%A")
        return None

    @property
    def day_name_ar(self):
        days = {
            "Saturday": "السبت",
            "Sunday": "الأحد",
            "Monday": "الاثنين",
            "Tuesday": "الثلاثاء",
            "Wednesday": "الأربعاء",
            "Thursday": "الخميس",
            "Friday": "الجمعة",
        }
        day = self.day_name
        return days.get(day) if day else None

    # وللتاريخ نفسه
    @property
    def local_date(self):
        if self.start_datetime:
            return localtime(self.start_datetime).date()
        return None

    def __str__(self):
        return (
            f"{self.user.username}: "
            f"{self.start_datetime} - {self.end_datetime} "
            f"({self.hours}h)"
        )