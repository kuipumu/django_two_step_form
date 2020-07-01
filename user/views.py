"""user app views.py module."""

from os import path
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, PasswordChangeView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.messages import success
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.utils.translation import ugettext_lazy as _
from django_registration.signals import user_registered
from formtools.wizard.views import SessionWizardView
from app.settings import COMPANY_NAME, MEDIA_ROOT
from app.views import GlobalMixin
from .forms import (
    CustomSignUpUserForm, CustomSignUpCompanyForm,
    EmailChangeViewForm, ProfileChangeViewForm,
    CompanyChangeViewForm
)
from .models import CustomUser


class NotLoggedInMixin(UserPassesTestMixin):
    """Test if user is currently logged in,
    if logged, deny access."""
    def test_func(self):
        """Check if user logged in."""
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        """Return 404 response."""
        return Http404()


class CustomRegistrationView(
    NotLoggedInMixin,
    GlobalMixin,
    SessionWizardView):
    """Custom registration view using a WizardView."""
    TEMPLATES = {
        "user": "registration/signup_user.html",
        "company": "registration/signup_company.html"
    }

    template_name = "registration/signup.html"
    file_storage = FileSystemStorage(
        location=path.join(MEDIA_ROOT, 'signup')
    )
    form_list = [
        ("user", CustomSignUpUserForm),
        ("company", CustomSignUpCompanyForm)
    ]

    def get_template_names(self):
        """Get templates for each step."""
        return [self.TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        """Process data returned from all steps."""
        form_data = [form.cleaned_data for form in form_list]
        user_data = {}
        for dict in form_data:
            user_data.update(dict)
        user_data['password'] = user_data.pop('password1')
        del user_data['password2']
        del user_data['email_confirm']
        del user_data['captcha']
        new_user = get_user_model().objects.create_user(
            **user_data
        )
        new_user.save()
        user_registered.send(
            sender=self.__class__, user=new_user, request=self.request
        )
        success(self.request, _('User successfully created!. log in now.'))
        return HttpResponseRedirect(reverse_lazy('login'))

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        context['title'] = COMPANY_NAME + ' - ' + str(_('Sign Up'))
        return context


class CustomLoginView(
    NotLoggedInMixin,
    GlobalMixin,
    LoginView):

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        context['title'] = COMPANY_NAME + ' - ' + str(_('Login'))
        return context


class CustomPasswordResetView(
    NotLoggedInMixin,
    GlobalMixin,
    PasswordResetView,):

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        context['title'] = COMPANY_NAME + ' - ' + str(_('Reset Password'))
        return context


class CustomPasswordResetDoneView(
    NotLoggedInMixin,
    GlobalMixin,
    PasswordResetDoneView,):

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        context['title'] = COMPANY_NAME + ' - ' + str(_('Reset Password Done'))
        return context


class CustomPasswordResetConfirmView(
    NotLoggedInMixin,
    GlobalMixin,
    PasswordResetConfirmView,):

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        context['title'] = COMPANY_NAME + ' - ' + str(_('Reset Password Confirm'))
        return context


class CustomPasswordResetCompleteView(
    NotLoggedInMixin,
    GlobalMixin,
    PasswordResetCompleteView,):

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        context['title'] = COMPANY_NAME + ' - ' + str(_('Reset Password Complete'))
        return context


class UserUpdateView(
    SuccessMessageMixin,
    UserPassesTestMixin,
    LoginRequiredMixin,
    GlobalMixin,
    UpdateView):
    """User update view."""

    model = CustomUser
    form_class = ProfileChangeViewForm
    template_name = 'user/user_update.html'
    success_message = _('Successfully updated!.')
    login_url = 'login'

    def test_func(self, *args, **kwargs):
        """Check if user to edit is the has the logged user."""
        object = super().get_object(*args, **kwargs)
        return object.id == self.request.user.id

    def handle_no_permission(self):
        """Return 404 response."""
        return Http404()

    def get_success_url(self):
        """Success url function."""
        return reverse_lazy('user_update', args=[str(self.object.id)])

    def form_valid(self, form):
        """Valid form function."""
        self.object.save()
        success(self.request, self.success_message % self.object.__dict__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        context['title'] = COMPANY_NAME + ' - ' + str(_('User Profile'))
        context['object'] = self.object
        return context


class CompanyUpdateView(
    SuccessMessageMixin,
    UserPassesTestMixin,
    LoginRequiredMixin,
    GlobalMixin,
    UpdateView):
    """Company update view."""

    model = CustomUser
    form_class = CompanyChangeViewForm
    template_name = 'user/company_update.html'
    success_message = _('Successfully updated!.')
    login_url = 'login'

    def test_func(self, *args, **kwargs):
        """Test previous to user access."""
        object = super().get_object(*args, **kwargs)
        return object.id == self.request.user.id

    def handle_no_permission(self):
        """Return 404 response."""
        return Http404()

    def get_success_url(self):
        """Success url function."""
        return reverse_lazy('company_update', args=[str(self.object.id)])

    def form_valid(self, form):
        """Valid form function."""
        self.object.save()
        success(self.request, self.success_message % self.object.__dict__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        context['title'] = COMPANY_NAME + ' - ' + str(_('Company Profile'))
        context['object'] = self.object
        return context


class EmailUpdateView(
    SuccessMessageMixin,
    UserPassesTestMixin,
    LoginRequiredMixin,
    GlobalMixin,
    UpdateView):
    """Email update view."""

    model = CustomUser
    form_class = EmailChangeViewForm
    template_name = 'user/email_update.html'
    success_message = _('Successfully updated!.')
    login_url = 'login'

    def test_func(self, *args, **kwargs):
        """Test previous to user access."""
        object = super().get_object(*args, **kwargs)
        return object.id == self.request.user.id

    def handle_no_permission(self):
        """Return 404 response."""
        return Http404()

    def get_success_url(self):
        """Success url function."""
        return reverse_lazy('email_update', args=[str(self.object.id)])

    def form_valid(self, form):
        """Valid form function."""
        self.object.save()
        success(self.request, self.success_message % self.object.__dict__)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        context['title'] = COMPANY_NAME + ' - ' + str(_('Change Email'))
        context['object'] = self.object
        return context


class PasswordUpdateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    GlobalMixin,
    PasswordChangeView):
    """Password update view."""

    login_url = 'login'
    success_url = reverse_lazy('password_update')
    success_message = _('Password successfully updated!.')

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        context['title'] = COMPANY_NAME + ' - ' + str(_('Change Password'))
        return context