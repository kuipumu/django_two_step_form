"""user app forms.py module."""

from django.forms import (
    Form, ModelForm, CharField,
    EmailField, Textarea,
    TextInput, ChoiceField
)
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserChangeForm, AuthenticationForm,
    PasswordResetForm, PasswordChangeForm
)
from django.utils.translation import ugettext_lazy as _
from django_registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from .models import CustomUser

# Fields for user forms.
user_fields = [
    "first_name",
    "last_name",
    "national_id_type",
    "national_id",
    "phone_number",
    "mobile_number",
    "date_birth",
    "photo",
    "security_question",
    "security_answer",
]

# Widgets for user forms.
user_widgets = {
    'national_id': TextInput(attrs={'pattern': '^[0-9]{5,9}'}),
    'date_birth': TextInput(attrs={'type': 'date'})
}

# Fields for company forms.
company_fields = [
    "company_name",
    "company_email",
    "rif_id_type",
    "rif_id",
    "company_phone_number",
    "company_address_line1",
    "company_address_line2",
    "company_state",
    "company_city",
    "company_postal_code",
    "company_logo"
]

# Widgets for company forms.
company_widgets = {
    'rif_id': TextInput(attrs={'pattern': '^[0-9]{8}-[0-9]{1}$'}),
}


class CustomSignUpUserForm(RegistrationForm):
    """First form step for sign up users."""

    email_confirm = EmailField(
        label=_("Confim email address"),
        help_text=_("Enter the same email address as before, for verification.")
    )

    class Meta(RegistrationForm.Meta):
        model = CustomUser
        fields = user_fields + [
            get_user_model().USERNAME_FIELD,
            get_user_model().get_email_field_name(),
            "password1",
            "password2",
        ]
        fields_required = ['email_confirm']
        widgets = user_widgets

    def clean(self):
        """Form clean method"""
        cleaned_data = super().clean()
        if cleaned_data.get(
                'email'
            ) != cleaned_data.get(
                'email_confirm'
            ):
            raise ValidationError({
                'email_confirm': [
                    _("Confirmation email addres does not math with set email.")
                ],
            })
        if cleaned_data.get('phone_number') is not None \
            and cleaned_data.get('mobile_number') is not None:
            if cleaned_data.get(
                    'phone_number'
                ) == cleaned_data.get(
                    'mobile_number'
                ):
                raise ValidationError({
                    'phone_number': [
                        _("Phone number can't be the same mobile number.")
                    ],
                    'mobile_number': [
                        _("Mobile number can't be the same has phone number.")
                    ],
                })

    def __init__(self, *args, **kwargs):
        """Change init method on form"""
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class']='email-field'
        self.fields['email_confirm'].widget.attrs['class']='email-confirm-field'
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['placeholder'] = field.label
            field.label = ''


class CustomSignUpCompanyForm(ModelForm):
    """Second form step for sign up users."""

    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = CustomUser
        fields = company_fields
        widgets = company_widgets

    def __init__(self, *args, **kwargs):
        """Change init method on form"""
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['placeholder'] = field.label
            field.label = ''


class CustomSignInForm(AuthenticationForm):
    """ Custom sign in form."""

    def __init__(self, *args, **kwargs):
        """Change init method on form"""
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['placeholder'] = field.label
            field.label = ''

class CustomPasswordResetForm(PasswordResetForm):
    """ Custom password reset form."""

    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def __init__(self, *args, **kwargs):
        """Change init method on form"""
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['placeholder'] = field.label
            field.label = ''


class ProfileChangeViewForm(UserChangeForm):
    """ Form for profile change."""

    class Meta:
        model = CustomUser
        fields = user_fields
        widgets = user_widgets
        fields_required = ['email_confirm']

    def __init__(self, *args, **kwargs):
        """Change init method on form"""
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['placeholder'] = field.label
            field.label = ''


class CompanyChangeViewForm(UserChangeForm):
    """ Form for company change."""

    class Meta:
        model = CustomUser
        fields = company_fields

    def __init__(self, *args, **kwargs):
        """Change init method on form"""
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['placeholder'] = field.label
            field.label = ''


class CustomPasswordChangeForm(PasswordChangeForm):
    """ Custom password change form."""

    def __init__(self, *args, **kwargs):
        """Change init method on form"""
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['placeholder'] = field.label
            field.label = ''


class EmailChangeViewForm(UserChangeForm):
    """ Form for email change."""

    email_confirm = EmailField(
        label=_("Confim email address"),
        help_text=_("Enter the same email address as before, for verification.")
    )

    class Meta:
        model = CustomUser
        fields = [
            get_user_model().USERNAME_FIELD,
            get_user_model().get_email_field_name(),
        ]
        fields_required = ['email_confirm']

    def clean(self):
        """Form clean method"""
        cleaned_data = super().clean()
        if cleaned_data.get(
                'email'
            ) != cleaned_data.get(
                'email_confirm'
            ):
            raise ValidationError({
                'email_confirm': [
                    _("Confirmation email addres does not math with set email.")
                ],
            })

    def __init__(self, *args, **kwargs):
        """Change init method on form"""
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class']='email-field'
        self.fields['email_confirm'].widget.attrs['class']='email-confirm-field'
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['placeholder'] = field.label
            field.label = ''