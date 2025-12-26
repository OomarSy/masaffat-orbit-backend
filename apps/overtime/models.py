from django.db import models
from django.contrib.auth import get_user_model

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

    def __str__(self):
        return f"{self.user.username}: {self.start_datetime} - {self.end_datetime} ({self.hours}h)"