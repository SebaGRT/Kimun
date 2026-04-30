from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ClaseCompletado
from .utils import obtener_o_calcular_progreso


@receiver(post_save, sender=ClaseCompletado)
def actualizar_progreso_por_clase(sender, instance, **kwargs):
    obtener_o_calcular_progreso(instance.usuario, instance.clase.curso)
