from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("projetos/", include("projetos.urls")),
    path("", include("core.urls")),
]

# No seu computador (DEBUG=True) o próprio Django entrega os uploads.
# No PythonAnywhere quem entrega é o servidor, pelo mapeamento /media/ da aba Web.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
