"""
Context Processors
Makes site settings and common data available in all templates.
"""

from apps.core.models import SiteSettings


def site_settings(request):
    """Add site settings to template context"""
    return {
        'site_settings': SiteSettings.get_settings(),
    }


def language_context(request):
    """Add language-related context"""
    from django.conf import settings
    return {
        'available_languages': settings.LANGUAGES,
        'current_language': getattr(request, 'LANGUAGE_CODE', 'fr'),
    }
