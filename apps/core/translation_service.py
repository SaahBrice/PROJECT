"""
Translation Service
Auto-translation using DeepL API for French-first content.
"""

try:
    import deepl
    DEEPL_AVAILABLE = True
except ImportError:
    DEEPL_AVAILABLE = False
    deepl = None

from django.conf import settings
from django.core.cache import cache
import hashlib


class TranslationService:
    """
    Service for automatic translation of content.
    Uses DeepL API for high-quality translations.
    Caches translations to minimize API calls.
    """
    
    # Language codes mapping (Django to DeepL)
    LANGUAGE_MAP = {
        'fr': 'FR',
        'en': 'EN-US',
        'it': 'IT',
        'de': 'DE',
    }
    
    # Cache timeout (1 week)
    CACHE_TIMEOUT = 60 * 60 * 24 * 7
    
    def __init__(self):
        self.api_key = getattr(settings, 'DEEPL_API_KEY', '')
        self.translator = None
        
        if self.api_key and DEEPL_AVAILABLE:
            try:
                self.translator = deepl.Translator(self.api_key)
            except Exception:
                pass
    
    def _get_cache_key(self, text: str, source_lang: str, target_lang: str) -> str:
        """Generate a unique cache key for a translation"""
        text_hash = hashlib.md5(text.encode()).hexdigest()[:16]
        return f"translation:{source_lang}:{target_lang}:{text_hash}"
    
    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: str = 'fr',
        use_cache: bool = True
    ) -> str:
        """
        Translate text from source language to target language.
        
        Args:
            text: Text to translate
            target_lang: Target language code (fr, en, it, de)
            source_lang: Source language code (default: fr)
            use_cache: Whether to use cached translations
            
        Returns:
            Translated text or original if translation fails
        """
        # Don't translate if same language
        if source_lang == target_lang:
            return text
        
        # Check if translator is available
        if not self.translator:
            return text
        
        # Convert to DeepL language codes
        deepl_source = self.LANGUAGE_MAP.get(source_lang, 'FR')
        deepl_target = self.LANGUAGE_MAP.get(target_lang, 'EN-US')
        
        # Check cache first
        if use_cache:
            cache_key = self._get_cache_key(text, source_lang, target_lang)
            cached = cache.get(cache_key)
            if cached:
                return cached
        
        try:
            result = self.translator.translate_text(
                text,
                source_lang=deepl_source,
                target_lang=deepl_target,
                preserve_formatting=True,
            )
            
            translated = result.text
            
            # Cache the result
            if use_cache:
                cache.set(cache_key, translated, self.CACHE_TIMEOUT)
            
            return translated
            
        except Exception as e:
            # Log error but return original text
            print(f"Translation error: {e}")
            return text
    
    def translate_batch(
        self,
        texts: list,
        target_lang: str,
        source_lang: str = 'fr'
    ) -> list:
        """
        Translate multiple texts at once.
        
        Args:
            texts: List of texts to translate
            target_lang: Target language code
            source_lang: Source language code
            
        Returns:
            List of translated texts
        """
        if not texts:
            return []
        
        if source_lang == target_lang:
            return texts
        
        if not self.translator:
            return texts
        
        # Convert to DeepL language codes
        deepl_source = self.LANGUAGE_MAP.get(source_lang, 'FR')
        deepl_target = self.LANGUAGE_MAP.get(target_lang, 'EN-US')
        
        try:
            results = self.translator.translate_text(
                texts,
                source_lang=deepl_source,
                target_lang=deepl_target,
                preserve_formatting=True,
            )
            
            return [r.text for r in results]
            
        except Exception as e:
            print(f"Batch translation error: {e}")
            return texts
    
    def get_usage(self) -> dict:
        """Get DeepL API usage statistics"""
        if not self.translator:
            return {'error': 'Translator not configured'}
        
        try:
            usage = self.translator.get_usage()
            return {
                'character_count': usage.character.count,
                'character_limit': usage.character.limit,
                'percentage_used': (usage.character.count / usage.character.limit) * 100
                                   if usage.character.limit else 0,
            }
        except Exception as e:
            return {'error': str(e)}


# Singleton instance
_translation_service = None

def get_translation_service() -> TranslationService:
    """Get the singleton translation service instance"""
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService()
    return _translation_service


def translate(text: str, target_lang: str, source_lang: str = 'fr') -> str:
    """Convenience function for translating text"""
    service = get_translation_service()
    return service.translate(text, target_lang, source_lang)
