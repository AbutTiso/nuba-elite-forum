from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('articles/', include('articles.urls')),
    path('events/', include('events.urls')),
    path('members/', include('members.urls')),
    path('leadership/', include('leadership.urls')),
    path('contact/', include('contact.urls')),
    path('gallery/', include('gallery.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
