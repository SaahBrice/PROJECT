"""
SEO Middleware
Adds security headers and SEO-related headers.
"""

class SecurityHeadersMiddleware:
    """Add security headers to all responses"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response


class LocaleMiddleware:
    """Handle language preference from URL or cookie"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get language preference
        lang = request.GET.get('lang')
        if lang:
            from django.utils import translation
            translation.activate(lang)
            request.LANGUAGE_CODE = lang
        
        response = self.get_response(request)
        return response
