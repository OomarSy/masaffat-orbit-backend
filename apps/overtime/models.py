from django.db import models
from django.contrib.auth import get_user_model

from decimal import Decimal

from apps.core.mixins import SoftDeleteUniqueMixin
from apps.core.models import BaseModel

User = get_user_model()


class Overtime(SoftDeleteUniqueMixin, BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="overtimes")
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
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
    
    def __str__(self):
        return f"{self.user.username}: {self.start_datetime} - {self.end_datetime} ({self.hours}h)"