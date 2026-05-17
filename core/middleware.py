from django.utils import translation
from django.conf import settings

class SiteLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Force admin to always be English LTR
        if request.path.startswith('/admin/'):
            translation.activate('en')
        else:
            site_lang = request.COOKIES.get('site_lang')
            if site_lang and site_lang in dict(settings.LANGUAGES):
                translation.activate(site_lang)
        
        response = self.get_response(request)
        return response
