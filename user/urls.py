"""user app urls.py module."""

from django.urls import path
from django.contrib.auth.views import LogoutView
from django.utils.translation import ugettext_lazy as _
from .forms import (
    CustomSignInForm, CustomPasswordResetForm, CustomPasswordChangeForm
)
from .views import (
    CustomRegistrationView, CustomLoginView,
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,  CustomPasswordResetCompleteView,
    UserUpdateView, CompanyUpdateView, EmailUpdateView, PasswordUpdateView
)

# https://docs.djangoproject.com/en/3.0/topics/http/urls/#syntax-of-the-urlpatterns-variable
urlpatterns = [
    path(
        _('signup/'),
        CustomRegistrationView.as_view(
        ),
        name="signup"
    ),
    path(
        _('login/'),
        CustomLoginView.as_view(
            form_class=CustomSignInForm,
        ),
        name='login'
    ),
    path(
        _('logout/'),
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        _('reset/'),
        CustomPasswordResetView.as_view(
            form_class=CustomPasswordResetForm
        ),
        name='password_reset'
    ),
    path(
        _('reset/done/'),
        CustomPasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        _('reset/<uidb64>/<token>/'),
        CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        _('reset/complete/'),
        CustomPasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path(
        _('user/<uuid:pk>/'),
        UserUpdateView.as_view(),
        name='user_update'
    ),
    path(
        _('company/<uuid:pk>/'),
        CompanyUpdateView.as_view(),
        name='company_update'
    ),
    path(
        _('email/<uuid:pk>/'),
        EmailUpdateView.as_view(),
        name='email_update'
    ),
    path(
        _('password/'),
        PasswordUpdateView.as_view(
            form_class=CustomPasswordChangeForm
        ),
        name='password_update'
    ),
]