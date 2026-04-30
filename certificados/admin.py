from django.contrib import admin
from .models import Certificado


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario', 'curso', 'codigo_verificacion', 'estado',
        'fecha_emision', 'fecha_vencimiento', 'motivo_revocacion_corto'
    )
    list_filter = ('estado', 'fecha_emision', 'fecha_vencimiento')
    search_fields = (
        'usuario__username', 'usuario__first_name', 'curso__titulo',
        'codigo_verificacion'
    )
    readonly_fields = ('codigo_verificacion', 'fecha_emision')
    fieldsets = (
        ('Información General', {
            'fields': ('usuario', 'curso', 'estado', 'aprobado_por')
        }),
        ('Fechas', {
            'fields': ('fecha_emision', 'fecha_aprobacion', 'fecha_vencimiento')
        }),
        ('Certificado', {
            'fields': ('codigo_verificacion', 'archivo_pdf')
        }),
        ('Revocación', {
            'fields': ('motivo_revocacion',),
            'classes': ('collapse',),
        }),
    )

    def motivo_revocacion_corto(self, obj):
        if obj.motivo_revocacion:
            if len(obj.motivo_revocacion) > 50:
                return obj.motivo_revocacion[:50] + '...'
            return obj.motivo_revocacion
        return '-'
    motivo_revocacion_corto.short_description = 'Motivo Revocación'
