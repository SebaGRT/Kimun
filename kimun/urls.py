from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuarios.views import inicio
from cursos.views import ckeditor5_upload_restricted

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('cursos/', include('cursos.urls')),
    path('evaluaciones/', include('evaluaciones.urls')),
    path('certificados/', include('certificados.urls')),
    path('reportes/', include('reportes.urls')),
    path('calendario/', include('calendario.urls')),
    path('anuncios/', include('anuncios.urls')),
    path('tareas/', include('tareas.urls')),
    path('', inicio, name='inicio'),
    path("ckeditor5/image_upload/", ckeditor5_upload_restricted, name="ck_editor_5_upload_file"),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
