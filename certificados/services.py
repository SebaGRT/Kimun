from typing import Tuple, Dict


class CertificateEligibilityService:
    """Checks whether a user is eligible for a certificate for a given course.

    Eligibility requires ALL of:
    1. Active enrollment (estado != 'abandonado')
    2. All classes completed (100%, unless curso.certificado_requiere_clases is False)
    3. All evaluations passed (latest attempt per evaluation is aprobado=True,
       unless curso.certificado_requiere_evaluaciones is False)
    4. No existing non-revoked certificate for this (user, curso)
    5. curso.certificado_activo is True

    Returns: (is_eligible: bool, reasons: Dict[str, str])
        reasons is empty if eligible, otherwise describes each failure.
    """

    @staticmethod
    def check_eligibility(usuario, curso) -> Tuple[bool, Dict[str, str]]:
        from cursos.models import ClaseCompletado, InscripcionCurso
        from evaluaciones.models import IntentoEvaluacion
        from certificados.models import Certificado

        reasons = {}

        # 1. Check enrollment is active
        inscripcion = InscripcionCurso.objects.filter(
            usuario=usuario, curso=curso
        ).first()
        if not inscripcion:
            reasons['enrollment'] = 'Usuario no está inscrito en este curso.'
            return False, reasons
        if inscripcion.estado == 'abandonado':
            reasons['enrollment'] = 'La inscripción ha sido abandonada.'
            return False, reasons

        # 5. Check curso.certificado_activo
        activo = getattr(curso, 'certificado_activo', True)
        if not activo:
            reasons['curso'] = 'Este curso no emite certificados.'
            return False, reasons

        # 3. Check all evaluations passed
        requiere_evals = getattr(curso, 'certificado_requiere_evaluaciones', True)
        if requiere_evals:
            evaluaciones = curso.evaluaciones.all()
            if evaluaciones.exists():
                for ev in evaluaciones:
                    ultimo = ev.intentos.filter(usuario=usuario).order_by('-fecha_intento').first()
                    if not ultimo or not ultimo.aprobado:
                        reasons['evaluaciones'] = f'Evaluación "{ev.titulo}" no aprobada.'
                        break

        # 2. Check all classes completed
        requiere_clases = getattr(curso, 'certificado_requiere_clases', True)
        if requiere_clases:
            total_clases = curso.clases.count()
            if total_clases > 0:
                completadas = ClaseCompletado.objects.filter(
                    usuario=usuario, clase__curso=curso
                ).count()
                pct_min = getattr(curso, 'certificado_porcentaje_minimo_clases', 100)
                threshold = int(total_clases * pct_min / 100)
                if completadas < threshold:
                    reasons['clases'] = f'Solo {completadas}/{total_clases} clases completadas ({pct_min}% requerido).'

        # 4. Check no existing non-revoked certificate
        existente = Certificado.objects.filter(
            usuario=usuario, curso=curso
        ).exclude(estado='revocado').first()
        if existente:
            reasons['certificado_existente'] = 'Ya existe un certificado para este curso.'
            return False, reasons

        return len(reasons) == 0, reasons
