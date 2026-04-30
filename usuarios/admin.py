from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Auditoria


class KimunAdminSite(AdminSite):
    site_title = 'Kimün - Administración'
    site_header = 'Kimün - Plataforma de Capacitación'
    index_title = 'Panel de Control'

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        
        user = request.user
        if not user.is_superuser:
            rol = getattr(user, 'rol', None)
            
            allowed_apps = []
            
            if rol == 'admin':
                allowed_apps = ['usuarios', 'cursos', 'evaluaciones', 'certificados']
            elif rol == 'docente':
                allowed_apps = ['cursos', 'evaluaciones']
            else:
                allowed_apps = ['cursos', 'certificados']
            
            app_list = [app for app in app_list if app['app_label'] in allowed_apps]
        
        return app_list


kimun_admin_site = KimunAdminSite(name='kimun_admin')


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'usuario', 'accion', 'descripcion', 'ip_address']
    list_filter = ['accion', 'fecha']
    search_fields = ['usuario__username', 'descripcion']
    readonly_fields = ['usuario', 'accion', 'descripcion', 'ip_address', 'fecha', 'objeto_tipo', 'objeto_id']
    date_hierarchy = 'fecha'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
