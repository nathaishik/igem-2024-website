from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings_prod

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notebook.urls')),
] + static(settings_prod.MEDIA_URL, document_root=settings_prod.MEDIA_ROOT)

if settings_prod.DEBUG == 'False':
    urlpatterns += static(settings_prod.STATIC_URL, document_root=settings_prod.STATIC_ROOT)
