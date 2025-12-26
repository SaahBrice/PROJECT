"""
FDTM Platform URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
    # Language switcher URL
    path('i18n/', include('django.conf.urls.i18n')),
    path('set-language/', set_language, name='set_language'),
]

# i18n URLs (with language prefix)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('projets/', include('apps.projects.urls', namespace='projects')),
    path('actualites/', include('apps.articles.urls', namespace='articles')),
    path('dons/', include('apps.donations.urls', namespace='donations')),
    path('compte/', include('apps.accounts.urls', namespace='accounts')),
    prefix_default_language=False,  # Don't prefix the default language (French)
)

# Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    
    # Django Debug Toolbar
    try:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns
    except ImportError:
        pass
