from django.utils import timezone
from datetime import timedelta
from django.db import models

from django.contrib.auth import get_user_model

from apps.core.mixins import SoftDeleteUniqueMixin
from apps.core.models import BaseModel

User = get_user_model()


class UserLocation(SoftDeleteUniqueMixin, BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="location")
    latitude = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    is_online = models.BooleanField(default=False)
    
    OFFLINE_THRESHOLD_MINUTES = 5
    
    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.updated_at:
            self.is_online = (now - self.updated_at) <= timedelta(minutes=self.OFFLINE_THRESHOLD_MINUTES)
        else:
            self.is_online = False
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.latitude}, {self.longitude}"