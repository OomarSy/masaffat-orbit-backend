from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User model that uses only username for authentication."""
    pass