import uuid
from django.db import models
from django.conf import settings


class Certificado(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificados'
    )
    curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE, related_name='certificados')
    codigo_verificacion = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    archivo_pdf = models.FileField(upload_to='certificados/', null=True, blank=True)

    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'

    def __str__(self):
        return f"Certificado {self.usuario} - {self.curso.titulo}"