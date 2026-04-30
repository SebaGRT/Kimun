from django.db.models.signals import post_save
from django.dispatch import receiver
from evaluaciones.models import IntentoEvaluacion
from cursos.models import ClaseCompletado
from .services import CertificateEligibilityService
from .models import Certificado


@receiver(post_save, sender=IntentoEvaluacion)
def intento_post_save(sender, instance, created, **kwargs):
    if not created:
        return
    usuario = instance.usuario
    curso = instance.evaluacion.curso
    is_eligible, _ = CertificateEligibilityService.check_eligibility(usuario, curso)
    if is_eligible:
        Certificado.objects.create(usuario=usuario, curso=curso, estado='aprobado')


@receiver(post_save, sender=ClaseCompletado)
def clase_completado_post_save(sender, instance, created, **kwargs):
    if not created:
        return
    usuario = instance.usuario
    curso = instance.clase.curso
    is_eligible, _ = CertificateEligibilityService.check_eligibility(usuario, curso)
    if is_eligible:
        Certificado.objects.create(usuario=usuario, curso=curso, estado='aprobado')
