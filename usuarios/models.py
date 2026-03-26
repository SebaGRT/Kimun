from django.db import models
from django.contrib.auth.models import AbstractUser


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