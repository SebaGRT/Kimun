from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class AreaCargo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Área/Cargo'
        verbose_name_plural = 'Áreas/Cargos'

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('docente', 'Docente'),
        ('colaborador', 'Colaborador'),
    ]

    rut = models.CharField(max_length=12, unique=True, verbose_name='RUT')
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='colaborador')
    cargo = models.ForeignKey(
        AreaCargo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"


class Recordatorio(models.Model):
    TIPO_CHOICES = [
        ('7_dias', '7 días antes'),
        ('3_dias', '3 días antes'),
        ('1_dia', '1 día antes'),
        ('vencimiento', 'Día del vencimiento'),
    ]

    usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='recordatorios'
    )
    curso = models.ForeignKey(
        'cursos.Curso',
        on_delete=models.CASCADE,
        related_name='recordatorios'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Recordatorio'
        verbose_name_plural = 'Recordatorios'
        unique_together = ['usuario', 'curso', 'tipo']

    def __str__(self):
        return f"{self.usuario} - {self.curso.titulo} ({self.get_tipo_display()})"


class Auditoria(models.Model):
    ACCION_CHOICES = [
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
        ('curso_completado', 'Curso completado'),
        ('evaluacion_intento', 'Intento de evaluación'),
        ('certificado_aprobado', 'Certificado aprobado'),
        ('usuario_creado', 'Usuario creado'),
        ('inscripcion_creada', 'Inscripción creada'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='auditorias')
    accion = models.CharField(max_length=30, choices=ACCION_CHOICES)
    descripcion = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    objeto_tipo = models.CharField(max_length=50, blank=True)
    objeto_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['usuario', '-fecha']),
            models.Index(fields=['accion', '-fecha']),
        ]