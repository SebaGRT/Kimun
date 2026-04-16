from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuarios.views import inicio

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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
