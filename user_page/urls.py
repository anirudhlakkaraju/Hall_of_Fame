from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from user_page import settings

urlpatterns = [
    path('admin/', admin.site.urls),        
    path('api/userprofile/', include('userprofile.urls')),      # Root endpoint
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
