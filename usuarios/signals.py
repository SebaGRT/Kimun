from django.contrib.auth import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Auditoria
from django.contrib.auth import get_user_model

Usuario = get_user_model()


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    Auditoria.objects.create(
        usuario=user,
        accion='login',
        descripcion=f'Usuario {user.username} inició sesión',
        ip_address=getattr(request, 'auditoria_ip', None)
    )


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    if user:
        Auditoria.objects.create(
            usuario=user,
            accion='logout',
            descripcion=f'Usuario {user.username} cerró sesión',
            ip_address=getattr(request, 'auditoria_ip', None)
        )


@receiver(post_save, sender=Usuario)
def log_usuario_creado(sender, instance, created, **kwargs):
    if created:
        Auditoria.objects.create(
            usuario=instance,
            accion='usuario_creado',
            descripcion=f'Usuario {instance.username} creado'
        )


@receiver(post_save, sender='evaluaciones.IntentoEvaluacion')
def log_evaluacion_intento(sender, instance, created, **kwargs):
    if created:
        Auditoria.objects.create(
            usuario=instance.usuario,
            accion='evaluacion_intento',
            descripcion=f'Intento en {instance.evaluacion.titulo}: {instance.puntaje_obtenido}%',
            objeto_tipo='Evaluacion',
            objeto_id=instance.evaluacion_id
        )


@receiver(post_save, sender='evaluaciones.IntentoEvaluacion')
def actualizar_progreso_por_evaluacion(sender, instance, **kwargs):
    from cursos.utils import obtener_o_calcular_progreso
    obtener_o_calcular_progreso(instance.usuario, instance.evaluacion.curso)


@receiver(post_save, sender='cursos.InscripcionCurso')
def log_curso_completado(sender, instance, **kwargs):
    if instance.estado == 'completado':
        Auditoria.objects.create(
            usuario=instance.usuario,
            accion='curso_completado',
            descripcion=f'Curso {instance.curso.titulo} completado',
            objeto_tipo='Curso',
            objeto_id=instance.curso_id
        )
