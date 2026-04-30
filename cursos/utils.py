from .models import ProgresoCurso


def obtener_o_calcular_progreso(usuario, curso):
    progreso, _ = ProgresoCurso.objects.get_or_create(
        usuario=usuario,
        curso=curso,
        defaults={
            'total_clases': curso.clases.count(),
            'total_evaluaciones': curso.evaluaciones.count(),
        }
    )
    progreso.calcular_progreso()
    return progreso
