from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('util.urls', namespace='util')),
    path('facturacion_electronica', include('facturacion_electronica.urls', namespace='facturacion_electronica')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
