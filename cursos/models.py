from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django_ckeditor_5.fields import CKEditor5Field


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#6366f1', help_text='Color en formato hex, ej: #6366f1')
    descripcion = models.TextField(blank=True, default='')
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Curso(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cursos'
    )
    docente_creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cursos_creados'
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField(null=True, blank=True, verbose_name='Fecha límite')

    certificado_activo = models.BooleanField(
        default=True,
        help_text='Este curso emite certificado al completarse'
    )
    certificado_requiere_clases = models.BooleanField(
        default=True,
        help_text='Requiere completar todas las clases para obtener el certificado'
    )
    certificado_porcentaje_minimo_clases = models.PositiveIntegerField(
        default=100,
        help_text='Porcentaje mínimo de clases requeridas (0-100)'
    )
    certificado_requiere_evaluaciones = models.BooleanField(
        default=True,
        help_text='Requiere aprobar todas las evaluaciones para obtener el certificado'
    )
    certificado_vigencia_meses = models.PositiveIntegerField(
        default=0,
        help_text='Meses de vigencia del certificado. 0 = sin vencimiento'
    )

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        indexes = [
            models.Index(fields=['estado', '-fecha_creacion']),
            models.Index(fields=['docente_creador']),
        ]

    def __str__(self):
        return self.titulo


class Material(models.Model):
    TIPO_CHOICES = [
        ('pdf', 'PDF'),
        ('video', 'Video URL'),
        ('video_file', 'Video (archivo)'),
        ('office', 'Documento Office'),
    ]

    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='materiales')
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    archivo = models.FileField(upload_to='materiales/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"


class InscripcionCurso(models.Model):
    ESTADO_CHOICES = [
        ('asignado', 'Asignado'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='asignado')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        unique_together = ['usuario', 'curso']
        indexes = [
            models.Index(fields=['usuario', 'estado']),
            models.Index(fields=['curso', 'estado']),
            models.Index(fields=['fecha_asignacion']),
        ]

    def __str__(self):
        return f"{self.usuario} - {self.curso} ({self.get_estado_display()})"


class Clase(models.Model):
    """Clase/Lección dentro de un curso - contenido rico con CKEditor"""
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='clases')
    titulo = models.CharField(max_length=200)
    contenido = CKEditor5Field(verbose_name='Contenido de la clase', config_name='default')
    orden = models.PositiveIntegerField(default=1, help_text='Orden de la clase en el curso')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'
        ordering = ['orden']
        constraints = [
            models.UniqueConstraint(
                fields=['curso', 'orden'],
                name='clase_curso_orden_uniq'
            ),
            models.CheckConstraint(
                condition=models.Q(orden__gte=1),
                name='clase_orden_minimo'
            ),
        ]

    def __str__(self):
        return f"{self.orden}. {self.titulo}"

    def clean(self):
        super().clean()
        if self.orden is not None and self.orden < 1:
            raise ValidationError({'orden': 'El orden debe ser mayor a 0.'})

    def get_clase_anterior(self):
        """Retorna la clase anterior en el orden, o None si es la primera"""
        return Clase.objects.filter(
            curso=self.curso,
            orden__lt=self.orden
        ).order_by('-orden').first()

    def get_siguiente_clase(self):
        """Retorna la siguiente clase en el orden, o None si es la última"""
        return Clase.objects.filter(
            curso=self.curso,
            orden__gt=self.orden
        ).order_by('orden').first()


class ClaseCompletado(models.Model):
    """Registro de completación de una clase por un usuario"""
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clases_completadas'
    )
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='completados')
    fecha_completado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Clase Completada'
        verbose_name_plural = 'Clases Completadas'
        unique_together = ['usuario', 'clase']
        indexes = [
            models.Index(fields=['usuario', 'clase']),
        ]

    def __str__(self):
        return f"{self.usuario} - {self.clase.titulo} ({self.fecha_completado.strftime('%d/%m/%Y')})"


class ProgresoCurso(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progresos')
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='progresos')
    porcentaje = models.PositiveIntegerField(default=0)
    clases_completadas = models.PositiveIntegerField(default=0)
    total_clases = models.PositiveIntegerField(default=0)
    evaluaciones_aprobadas = models.PositiveIntegerField(default=0)
    total_evaluaciones = models.PositiveIntegerField(default=0)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Progreso de Curso'
        verbose_name_plural = 'Progresos de Cursos'
        unique_together = ['usuario', 'curso']
        indexes = [
            models.Index(fields=['usuario', 'curso']),
            models.Index(fields=['porcentaje']),
        ]

    def calcular_progreso(self):
        from evaluaciones.models import IntentoEvaluacion

        total_clases = self.curso.clases.count()
        clases_completadas = ClaseCompletado.objects.filter(
            usuario=self.usuario, clase__curso=self.curso
        ).count()

        total_evals = self.curso.evaluaciones.count()
        if total_evals > 0:
            aprobadas = IntentoEvaluacion.objects.filter(
                usuario=self.usuario,
                evaluacion__curso=self.curso,
                aprobado=True
            ).values('evaluacion').distinct().count()
        else:
            aprobadas = 0

        self.clases_completadas = clases_completadas
        self.total_clases = total_clases
        self.evaluaciones_aprobadas = aprobadas
        self.total_evaluaciones = total_evals

        if total_clases > 0 and total_evals > 0:
            self.porcentaje = int(((clases_completadas / total_clases) * 0.5 + (aprobadas / total_evals) * 0.5) * 100)
        elif total_clases > 0:
            self.porcentaje = int((clases_completadas / total_clases) * 100)
        elif total_evals > 0:
            self.porcentaje = int((aprobadas / total_evals) * 100)
        else:
            self.porcentaje = 0

        self.save()
        return self.porcentaje
