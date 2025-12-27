from django.db import models
from django.core.validators import FileExtensionValidator

from apps.core.models import BaseModel


class AndroidAppRelease(BaseModel):
    
    version = models.CharField(max_length=20, unique=True)
    minimum_supported_version = models.CharField(max_length=20)
    apk_file = models.FileField(
        upload_to='apk_files/',
        validators=[FileExtensionValidator(allowed_extensions=['apk'])],
        help_text='Upload the APK file for Android platform.'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.version