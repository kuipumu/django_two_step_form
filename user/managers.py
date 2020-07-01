"""user app managers.py module."""

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom user model manager."""

    def create_user(self, email, first_name, password, **extra_fields):
        """User creation function."""
        if not email:
            raise ValueError(_('The email of the user must be set.'))
        if not first_name:
            raise ValueError(_('At least the first name of the user must be set.'))
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, **extra_fields):
        """Super user creation function"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, first_name, password, **extra_fields)



