"""user app models.py module."""

from uuid import uuid4
from pathlib import Path
from sys import getsizeof
from io import BytesIO
from PIL import Image, ImageOps
from django.conf import settings
from django.urls import reverse_lazy
from django.core.validators import RegexValidator
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import (
    Model, CASCADE, UUIDField,
    CharField, BigIntegerField,
    BooleanField, EmailField,
    ImageField, DateField
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from countryinfo import CountryInfo
from .managers import CustomUserManager

# Get country information using default region for phone number.
COUNTRY = CountryInfo(getattr(settings, "PHONENUMBER_DEFAULT_REGION", "US"))

def photo_directory_path(instance, filename):
    """Get path to store photo with user id"""
    file_extension = Path(filename).suffix
    if instance.id:
        return 'user/photo/' + str(instance.email) + '_{0}{1}'.format(instance.id, file_extension)
    else:
        return 'user/photo/' + str(instance.email) + file_extension

def logo_directory_path(instance, filename):
    """Get path to store logo with user id"""
    file_extension = Path(filename).suffix
    if instance.id:
        return 'user/logo/' + str(instance.email) + '_{0}{1}'.format(instance.id, file_extension)
    else:
        return 'user/logo/' + str(instance.email) + file_extension


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""


    id = UUIDField(
        verbose_name=_('id'),
        auto_created=True,
        primary_key=True,
        serialize=False,
        default=uuid4,
        editable=False
    )
    email = EmailField(
        _('email address'),
        unique=True
    )
    first_name = CharField(
        _('first name'),
        max_length=254
    )
    last_name = CharField(
        _('last name'),
        max_length=254
    )
    national_id_type = CharField(
        _('national ID type'),
        choices = [
            ('V', 'V'),
            ('E', 'E'),
            ('J', 'J'),
            ('P', 'P'),
        ],
        max_length=2,
        blank=False,
        null=False
    )
    national_id = CharField(
        _('national ID'),
        max_length=254,
        validators=[
            RegexValidator(
                regex='^[0-9]{5,9}$',
                message=_("National ID must be in XXXXXXXXX format."),
                code='invalid_national_id'
            ),
        ],
        help_text=_('National ID must be in XXXXXXXXX format.'),
        unique=True
    )
    phone_number = PhoneNumberField(
        _('phone number'),
        max_length=254
    )
    mobile_number = PhoneNumberField(
        _('mobile number'),
        blank=True,
        null=True
    )
    date_birth = DateField(
        _('date birth'),
        help_text=_('Enter your birth date.')
    )
    security_question = CharField(
        _('security question'),
        help_text=_('Set you security question.'),
        max_length=254
    )
    security_answer = CharField(
        _('security answer'),
        help_text=_('Set the answer for your security question.'),
        max_length=254
    )
    photo = ImageField(
        _('photo'),
        upload_to=photo_directory_path,
        help_text=_('Upload a user photo, the image must be in a resolution proportional to 150x150.'),
        blank=True,
        null=True
    )
    company_name = CharField(
        _('name'),
        max_length=254,
        unique=True
    )
    company_email = EmailField(
        _('email address'),
        unique=True
    )
    rif_id_type = CharField(
        _('RIF ID type'),
        choices = [
            ('V', 'V'),
            ('E', 'E'),
            ('J', 'J'),
            ('P', 'P'),
            ('G', 'G'),
        ],
        max_length=2,
        blank=False,
        null=False
    )
    rif_id = CharField(
        _('RIF ID'),
        max_length=254,
        validators=[
            RegexValidator(
                regex='^[0-9]{8}-[0-9]{1}$',
                message=_("RIF ID must be in XXXXXXXX-X format."),
                code='invalid_rif_id'
            ),
        ],
        help_text=_("RIF ID must be in XXXXXXXX-X format."),
        unique=True
    )
    company_phone_number = PhoneNumberField(
        _('phone number'),
        max_length=254
    )
    company_address_line1 = CharField(
        _('address line 1'),
        max_length=254
    )
    company_address_line2 = CharField(
        _('address line 2'),
        max_length=254,
        blank=True,
        null=True
    )
    company_city = CharField(
        _('city'),
        max_length=254
    )
    company_state = CharField(
        _('state'),
        max_length=254,
        choices=tuple(zip(*[iter(COUNTRY.info()["provinces"])]*2)),
    )
    company_postal_code = CharField(
        _('postal code'),
        max_length=4
    )
    company_logo = ImageField(
        _('logo'),
        upload_to=logo_directory_path,
        help_text=_('Upload a company logo, the image must be in a resolution proportional to 250x150.'),
        blank=True,
        null=True
    )
    is_staff = BooleanField(
        _('Staff'),
        default=False
    )
    is_active = BooleanField(
        _('Active'),
        default=True
    )

    # Define username field for manager.
    USERNAME_FIELD = 'email'
    # Define required fields for manager.
    REQUIRED_FIELDS = ['first_name, last_name']

    objects = CustomUserManager()

    class Meta:
        ordering = ['-email']
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = [
            ('national_id_type', 'national_id',),
            ('rif_id_type', 'rif_id',)
        ]

    def get_absolute_url(self):
        """Returns absolute url to model"""
        return reverse_lazy('user_update', args=[str(self.id)])

    def save(self, *args, **kwargs):
        """Model save method"""
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        """Model clean method"""
        # Modify if adding.
        if self._state.adding is True:
            # Set created date.
            self.created_at = timezone.now()
        # Set update date.
        self.updated_at = timezone.now()

        if self.photo:
            image = Image.open(self.photo)
            rgb_im = image.convert('RGB')
            output_io_stream = BytesIO()
            image_temporary = ImageOps.fit(rgb_im, (150, 150), Image.ANTIALIAS)
            image_temporary.save(output_io_stream, format='JPEG', quality=70)
            output_io_stream.seek(0)
            self.photo = InMemoryUploadedFile(
                output_io_stream,
                'ImageField',
                "%s.jpg" %self.photo.name.split('.')[0],
                'image/jpeg',
                getsizeof(output_io_stream),
                None
            )

        if self.company_logo:
            image = Image.open(self.company_logo)
            rgb_im = image.convert('RGB')
            output_io_stream = BytesIO()
            image_temporary = ImageOps.fit(rgb_im, (250, 150), Image.ANTIALIAS)
            image_temporary.save(output_io_stream, format='JPEG', quality=70)
            output_io_stream.seek(0)
            self.company_logo = InMemoryUploadedFile(
                output_io_stream,
                'ImageField',
                "%s.jpg" %self.company_logo.name.split('.')[0],
                'image/jpeg',
                getsizeof(output_io_stream),
                None
            )

    def get_full_name(self):
        """Get the full name of a Person."""
        if self.last_name is not None:
            full_name = "{0} {1}".format(self.first_name, self.last_name)
            full_name.strip()
        else:
            full_name = self.first_name
        return full_name

    def __str__(self):
        return self.email