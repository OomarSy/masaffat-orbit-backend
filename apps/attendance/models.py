from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendances")
    checkin_time = models.DateTimeField(default=timezone.now)
    checkout_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-checkin_time']

    def __str__(self):
        return f"{self.user.username} - {self.checkin_time} / {self.checkout_time}"