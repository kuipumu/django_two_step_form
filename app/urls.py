"""app urls.py module."""

from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
from app.settings import ( DEBUG, MEDIA_URL,
MEDIA_ROOT, STATIC_URL, STATIC_ROOT )
from .views import IndexView

# https://docs.djangoproject.com/en/3.0/topics/http/urls/#syntax-of-the-urlpatterns-variable
urlpatterns = i18n_patterns(
    path('', IndexView.as_view(), name='home'),
    path(_('accounts/'), include('user.urls')),
    prefix_default_language=False
)

# Add static and media settings if using DEBUG.
if DEBUG:
    urlpatterns = urlpatterns + \
        static(MEDIA_URL, document_root=MEDIA_ROOT)
    urlpatterns = urlpatterns + \
        static(STATIC_URL, document_root=STATIC_ROOT)