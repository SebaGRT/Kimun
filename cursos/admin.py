from django.contrib import admin
from .models import Curso, Material, InscripcionCurso


class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1
    fields = ('titulo', 'tipo', 'archivo', 'url')
    verbose_name_plural = 'Materiales'


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'docente_creador', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')
    inlines = [MaterialInline]
    fieldsets = (
        ('Información del Curso', {
            'fields': ('titulo', 'descripcion', 'docente_creador', 'estado')
        }),
    )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('titulo', 'curso__titulo')


@admin.register(InscripcionCurso)
class InscripcionCursoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'estado', 'fecha_asignacion')
    list_filter = ('estado', 'fecha_asignacion')
    search_fields = ('usuario__username', 'usuario__first_name', 'curso__titulo')