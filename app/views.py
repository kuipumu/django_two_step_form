"""app views.py module."""

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import ugettext_lazy as _
from app.settings import COMPANY_NAME


class GlobalMixin(View):
    '''Add context data to all views.'''
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        # Set view singular object name.
        context['company_name'] = COMPANY_NAME
        return context


class IndexView(GlobalMixin,TemplateView):
    """Homepage view."""
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        """Add extra context data."""
        context = super().get_context_data(**kwargs)
        context['title'] = COMPANY_NAME
        return context