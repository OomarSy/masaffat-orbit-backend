from django.db import models
from django.utils import timezone
from django.conf import settings

from apps.core.managers import AllObjectsManager, SoftDeleteManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
        editable=False
    )
    
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()
    
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])
    
    def save(self, *args, **kwargs):
        if not self.pk and hasattr(self, '_current_user'):
            self.user_created = self._current_user
        super().save(*args, **kwargs)
    
    
    class Meta:
        abstract = True