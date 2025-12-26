"""
Translation Template Tag
Provides auto-translation in Django templates.
"""

from django import template
from django.utils.safestring import mark_safe
from apps.core.translation_service import translate as translate_text

register = template.Library()


@register.simple_tag(takes_context=True)
def auto_translate(context, text, source_lang='fr'):
    """
    Auto-translate text to the current language.
    
    Usage:
        {% load translation_tags %}
        {% auto_translate "Bonjour le monde" %}
        {% auto_translate project.description "fr" %}
    """
    if not text:
        return ''
    
    # Get current language from context
    request = context.get('request')
    if request:
        target_lang = getattr(request, 'LANGUAGE_CODE', 'fr')
    else:
        target_lang = context.get('LANGUAGE_CODE', 'fr')
    
    # Translate
    translated = translate_text(str(text), target_lang, source_lang)
    return mark_safe(translated)


@register.filter
def translate_to(text, target_lang):
    """
    Filter to translate text to a specific language.
    
    Usage:
        {{ "Bonjour"|translate_to:"en" }}
    """
    if not text:
        return ''
    return translate_text(str(text), target_lang, 'fr')
