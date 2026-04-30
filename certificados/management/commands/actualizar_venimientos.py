from django.core.management.base import BaseCommand
from django.utils import timezone
from certificados.models import Certificado


class Command(BaseCommand):
    help = 'Marca certificados vencidos como expirados'

    def handle(self, *args, **options):
        now = timezone.now()
        certificados_vencidos = Certificado.objects.filter(
            fecha_vencimiento__isnull=False,
            fecha_vencimiento__lt=now,
        ).exclude(
            estado__in=['expirado', 'revocado']
        )

        count = certificados_vencidos.count()
        certificados_vencidos.update(estado='expirado')

        self.stdout.write(self.style.SUCCESS(f'Se actualizaron {count} certificados a expirado'))
