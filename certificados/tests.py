from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection, transaction
from django.db.models.signals import post_save
from certificados.models import Certificado
from certificados.signals import intento_post_save, clase_completado_post_save
from cursos.models import Curso, InscripcionCurso

Usuario = get_user_model()


class CertificadoModelTests(TestCase):
    def setUp(self):
        self.docente = Usuario.objects.create_user(
            username='docente', password='testpass', rol='docente', rut='11111111-1'
        )
        self.colaborador = Usuario.objects.create_user(
            username='colaborador', password='testpass', rol='colaborador', rut='22222222-2'
        )
        self.curso = Curso.objects.create(
            titulo='Curso Test',
            descripcion='Descripcion',
            docente_creador=self.docente
        )
        pdf_content = SimpleUploadedFile("certificado.pdf", b"PDF content", content_type="application/pdf")
        self.certificado = Certificado.objects.create(
            usuario=self.colaborador,
            curso=self.curso,
            archivo_pdf=pdf_content
        )

    def test_certificado_creation(self):
        self.assertEqual(self.certificado.usuario, self.colaborador)
        self.assertEqual(self.certificado.curso, self.curso)
        self.assertIsNotNone(self.certificado.codigo_verificacion)
        self.assertIsNotNone(self.certificado.fecha_emision)

    def test_certificado_str_method(self):
        expected = f'Certificado {self.colaborador} - Curso Test (Pendiente)'
        self.assertEqual(str(self.certificado), expected)

    def test_certificado_codigo_unico(self):
        certificado2 = Certificado.objects.create(
            usuario=self.docente,
            curso=self.curso
        )
        self.assertNotEqual(self.certificado.codigo_verificacion, certificado2.codigo_verificacion)

    def test_certificado_related_names(self):
        self.assertEqual(self.colaborador.certificados.count(), 1)
        self.assertEqual(self.curso.certificados.count(), 1)

    def test_certificado_default_estado(self):
        cert = Certificado.objects.create(usuario=self.colaborador, curso=self.curso)
        self.assertEqual(cert.estado, 'pendiente')

    def test_certificado_estado_choices(self):
        choices = dict(Certificado.ESTADO_CHOICES)
        self.assertIn('pendiente', choices)
        self.assertIn('aprobado', choices)
        self.assertIn('rechazado', choices)

    def test_certificado_str_includes_estado(self):
        cert = Certificado.objects.create(usuario=self.colaborador, curso=self.curso)
        self.assertIn('Pendiente', str(cert))


class CertificadoListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Usuario.objects.create_user(
            username='admin', password='testpass', rol='admin', rut='11111111-1'
        )
        self.docente = Usuario.objects.create_user(
            username='docente', password='testpass', rol='docente', rut='22222222-2'
        )
        self.curso = Curso.objects.create(
            titulo='Curso Test',
            descripcion='Descripcion',
            docente_creador=self.docente
        )

    def test_certificado_list_requires_admin(self):
        self.client.login(username='docente', password='testpass')
        response = self.client.get(reverse('certificados:certificado_list'))
        self.assertEqual(response.status_code, 403)

    def test_certificado_list_accessible_by_admin(self):
        self.client.login(username='admin', password='testpass')
        response = self.client.get(reverse('certificados:certificado_list'))
        self.assertEqual(response.status_code, 200)


class MisCertificadosViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Usuario.objects.create_user(
            username='admin', password='testpass', rol='admin', rut='11111111-1'
        )
        self.colaborador = Usuario.objects.create_user(
            username='colaborador', password='testpass', rol='colaborador', rut='22222222-2'
        )
        self.docente = Usuario.objects.create_user(
            username='docente', password='testpass', rol='docente', rut='33333333-3'
        )
        self.curso = Curso.objects.create(
            titulo='Curso Test',
            descripcion='Descripcion',
            docente_creador=self.docente
        )
        InscripcionCurso.objects.create(
            usuario=self.colaborador,
            curso=self.curso,
            estado='completado'
        )

    def test_mis_certificados_requires_login(self):
        response = self.client.get(reverse('certificados:mis_certificados'))
        self.assertEqual(response.status_code, 302)

    def test_mis_certificados_admin_redirects(self):
        self.client.login(username='admin', password='testpass')
        response = self.client.get(reverse('certificados:mis_certificados'))
        self.assertEqual(response.status_code, 302)

    def test_mis_certificados_colaborador(self):
        self.client.login(username='colaborador', password='testpass')
        response = self.client.get(reverse('certificados:mis_certificados'))
        self.assertEqual(response.status_code, 200)


class DescargarCertificadoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Usuario.objects.create_user(
            username='admin', password='testpass', rol='admin', rut='11111111-1'
        )
        self.colaborador = Usuario.objects.create_user(
            username='colaborador', password='testpass', rol='colaborador', rut='22222222-2'
        )
        self.docente = Usuario.objects.create_user(
            username='docente', password='testpass', rol='docente', rut='33333333-3'
        )
        self.curso = Curso.objects.create(
            titulo='Curso Test',
            descripcion='Descripcion',
            docente_creador=self.docente
        )
        pdf_content = SimpleUploadedFile("certificado.pdf", b"PDF content", content_type="application/pdf")
        self.certificado = Certificado.objects.create(
            usuario=self.colaborador,
            curso=self.curso,
            archivo_pdf=pdf_content,
            estado='aprobado'
        )

    def test_descargar_requires_login(self):
        response = self.client.get(reverse('certificados:descargar_certificado', kwargs={'pk': self.certificado.pk}))
        self.assertEqual(response.status_code, 302)

    def test_descargar_owner_can_access(self):
        self.client.login(username='colaborador', password='testpass')
        response = self.client.get(reverse('certificados:descargar_certificado', kwargs={'pk': self.certificado.pk}))
        self.assertEqual(response.status_code, 200)

    def test_descargar_admin_can_access(self):
        self.client.login(username='admin', password='testpass')
        response = self.client.get(reverse('certificados:descargar_certificado', kwargs={'pk': self.certificado.pk}))
        self.assertEqual(response.status_code, 200)

    def test_descargar_other_user_cannot_access(self):
        colaborador2 = Usuario.objects.create_user(
            username='colab2', password='testpass', rol='colaborador', rut='44444444-4'
        )
        self.client.login(username='colab2', password='testpass')
        response = self.client.get(reverse('certificados:descargar_certificado', kwargs={'pk': self.certificado.pk}))
        self.assertEqual(response.status_code, 302)

    def test_descargar_pending_certificado_blocked(self):
        cert = Certificado.objects.create(usuario=self.colaborador, curso=self.curso, estado='pendiente')
        self.client.login(username='colaborador', password='testpass')
        response = self.client.get(reverse('certificados:descargar_certificado', args=[cert.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('certificados:mis_certificados'))

    def test_descargar_rejected_certificado_blocked(self):
        cert = Certificado.objects.create(usuario=self.colaborador, curso=self.curso, estado='rechazado')
        self.client.login(username='colaborador', password='testpass')
        response = self.client.get(reverse('certificados:descargar_certificado', args=[cert.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('certificados:mis_certificados'))


class VerificarCertificadoViewTests(TestCase):
    def setUp(self):
        self.docente = Usuario.objects.create_user(
            username='docente', password='testpass', rol='docente', rut='11111111-1'
        )
        self.colaborador = Usuario.objects.create_user(
            username='colaborador', password='testpass', rol='colaborador', rut='22222222-2'
        )
        self.curso = Curso.objects.create(
            titulo='Curso Test',
            descripcion='Descripcion',
            docente_creador=self.docente
        )
        self.certificado = Certificado.objects.create(
            usuario=self.colaborador,
            curso=self.curso
        )

    def test_verificar_certificado_valid(self):
        from django.test import Client
        client = Client()
        response = client.get(reverse('certificados:verificar_certificado', kwargs={
            'codigo': self.certificado.codigo_verificacion
        }))
        self.assertEqual(response.status_code, 200)


class CertificadosPendientesViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Usuario.objects.create_user(username='admin', password='testpass', rol='admin', rut='11111111-1')
        self.docente = Usuario.objects.create_user(username='docente', password='testpass', rol='docente', rut='22222222-2')
        self.colaborador = Usuario.objects.create_user(username='colaborador', password='testpass', rol='colaborador', rut='33333333-3')
        self.curso = Curso.objects.create(titulo='Test Curso', descripcion='...', estado='publicado', docente_creador=self.docente)

    def test_admin_sees_all_pending(self):
        self.client.login(username='admin', password='testpass')
        response = self.client.get(reverse('certificados:certificados_pendientes'))
        self.assertEqual(response.status_code, 200)

    def test_docente_sees_own_pending(self):
        self.client.login(username='docente', password='testpass')
        response = self.client.get(reverse('certificados:certificados_pendientes'))
        self.assertEqual(response.status_code, 200)

    def test_colaborador_blocked(self):
        self.client.login(username='colaborador', password='testpass')
        response = self.client.get(reverse('certificados:certificados_pendientes'))
        self.assertEqual(response.status_code, 403)

    def test_aprobar_changes_estado(self):
        cert = Certificado.objects.create(usuario=self.colaborador, curso=self.curso, estado='pendiente')
        self.client.login(username='docente', password='testpass')
        response = self.client.post(reverse('certificados:aprobar_certificado', args=[cert.pk]))
        cert.refresh_from_db()
        self.assertEqual(cert.estado, 'aprobado')

    def test_rechazar_changes_estado(self):
        cert = Certificado.objects.create(usuario=self.colaborador, curso=self.curso, estado='pendiente')
        self.client.login(username='docente', password='testpass')
        response = self.client.post(reverse('certificados:rechazar_certificado', args=[cert.pk]))
        cert.refresh_from_db()
        self.assertEqual(cert.estado, 'rechazado')


class CertificateEligibilityServiceTests(TestCase):
    """Tests for the CertificateEligibilityService.

    The service checks whether a user is eligible for a certificate for a given course.
    Eligibility requires:
    1. Active enrollment (estado != 'abandonado')
    2. All classes completed (100%)
    3. All evaluations passed (latest attempt per evaluation is aprobado=True)
    4. No existing non-revoked certificate for this (user, course)
    """

    def setUp(self):
        from cursos.models import Clase, ClaseCompletado
        from evaluaciones.models import Evaluacion, IntentoEvaluacion

        self.Clase = Clase
        self.Evaluacion = Evaluacion
        self.ClaseCompletado = ClaseCompletado
        self.IntentoEvaluacion = IntentoEvaluacion

        post_save.disconnect(intento_post_save, sender=IntentoEvaluacion)
        post_save.disconnect(clase_completado_post_save, sender=ClaseCompletado)

        self.client = Client()
        self.docente = Usuario.objects.create_user(
            username='docente', password='testpass', rol='docente', rut='11111111-1'
        )
        self.colaborador = Usuario.objects.create_user(
            username='colaborador', password='testpass', rol='colaborador', rut='22222222-2'
        )
        self.curso = Curso.objects.create(
            titulo='Curso Test',
            descripcion='Test Desc',
            docente_creador=self.docente,
            estado='publicado',
        )
        self.clase1 = self.Clase.objects.create(curso=self.curso, titulo='Clase 1', orden=1)
        self.clase2 = self.Clase.objects.create(curso=self.curso, titulo='Clase 2', orden=2)
        self.eval1 = self.Evaluacion.objects.create(curso=self.curso, titulo='Eval 1', porcentaje_aprobacion=70)
        self.eval2 = self.Evaluacion.objects.create(curso=self.curso, titulo='Eval 2', porcentaje_aprobacion=70)
        self.inscripcion = InscripcionCurso.objects.create(
            usuario=self.colaborador,
            curso=self.curso,
            estado='en_progreso'
        )

    def tearDown(self):
        from cursos.models import ClaseCompletado
        from evaluaciones.models import IntentoEvaluacion
        post_save.connect(intento_post_save, sender=IntentoEvaluacion)
        post_save.connect(clase_completado_post_save, sender=ClaseCompletado)

    def _completar_clase(self, usuario, clase):
        self.ClaseCompletado.objects.create(usuario=usuario, clase=clase)

    def _aprobar_evaluacion(self, usuario, evaluacion, puntaje=100):
        self.IntentoEvaluacion.objects.create(
            usuario=usuario,
            evaluacion=evaluacion,
            puntaje_obtenido=puntaje,
            aprobado=True
        )

    # === ELIGIBLE CASES ===

    def test_eligible_when_all_complete(self):
        """User is eligible when all classes done AND all evaluations passed."""
        self._completar_clase(self.colaborador, self.clase1)
        self._completar_clase(self.colaborador, self.clase2)
        self._aprobar_evaluacion(self.colaborador, self.eval1)
        self._aprobar_evaluacion(self.colaborador, self.eval2)

        from certificados.services import CertificateEligibilityService
        is_eligible, reasons = CertificateEligibilityService.check_eligibility(self.colaborador, self.curso)
        self.assertTrue(is_eligible)
        self.assertEqual(reasons, {})

    def test_eligible_when_enrolled_asignado(self):
        """User is eligible even if enrolled with estado='asignado'."""
        self.inscripcion.estado = 'asignado'
        self.inscripcion.save()
        self._completar_clase(self.colaborador, self.clase1)
        self._completar_clase(self.colaborador, self.clase2)
        self._aprobar_evaluacion(self.colaborador, self.eval1)
        self._aprobar_evaluacion(self.colaborador, self.eval2)

        from certificados.services import CertificateEligibilityService
        is_eligible, reasons = CertificateEligibilityService.check_eligibility(self.colaborador, self.curso)
        self.assertTrue(is_eligible)

    # === NOT ELIGIBLE CASES ===

    def test_not_eligible_when_missing_class(self):
        """User is NOT eligible if a class is not completed."""
        self._completar_clase(self.colaborador, self.clase1)
        self._aprobar_evaluacion(self.colaborador, self.eval1)
        self._aprobar_evaluacion(self.colaborador, self.eval2)

        from certificados.services import CertificateEligibilityService
        is_eligible, reasons = CertificateEligibilityService.check_eligibility(self.colaborador, self.curso)
        self.assertFalse(is_eligible)
        self.assertIn('clases', reasons)

    def test_not_eligible_when_missing_evaluation(self):
        """User is NOT eligible if an evaluation is not passed."""
        self._completar_clase(self.colaborador, self.clase1)
        self._completar_clase(self.colaborador, self.clase2)
        self._aprobar_evaluacion(self.colaborador, self.eval1)

        from certificados.services import CertificateEligibilityService
        is_eligible, reasons = CertificateEligibilityService.check_eligibility(self.colaborador, self.curso)
        self.assertFalse(is_eligible)
        self.assertIn('evaluaciones', reasons)

    def test_not_eligible_when_evaluation_failed(self):
        """User is NOT eligible if latest attempt on an evaluation is not approved."""
        self._completar_clase(self.colaborador, self.clase1)
        self._completar_clase(self.colaborador, self.clase2)
        self._aprobar_evaluacion(self.colaborador, self.eval1)
        self.IntentoEvaluacion.objects.create(
            usuario=self.colaborador, evaluacion=self.eval2,
            puntaje_obtenido=30, aprobado=False
        )

        from certificados.services import CertificateEligibilityService
        is_eligible, reasons = CertificateEligibilityService.check_eligibility(self.colaborador, self.curso)
        self.assertFalse(is_eligible)
        self.assertIn('evaluaciones', reasons)

    def test_not_eligible_when_already_has_cert(self):
        """User is NOT eligible if they already have a non-revoked certificate."""
        self._completar_clase(self.colaborador, self.clase1)
        self._completar_clase(self.colaborador, self.clase2)
        self._aprobar_evaluacion(self.colaborador, self.eval1)
        self._aprobar_evaluacion(self.colaborador, self.eval2)
        Certificado.objects.create(
            usuario=self.colaborador, curso=self.curso, estado='aprobado'
        )

        from certificados.services import CertificateEligibilityService
        is_eligible, reasons = CertificateEligibilityService.check_eligibility(self.colaborador, self.curso)
        self.assertFalse(is_eligible)
        self.assertIn('certificado_existente', reasons)

    def test_eligible_when_previous_cert_revoked(self):
        """User IS eligible if the only existing cert is revoked (can re-earn)."""
        self._completar_clase(self.colaborador, self.clase1)
        self._completar_clase(self.colaborador, self.clase2)
        self._aprobar_evaluacion(self.colaborador, self.eval1)
        self._aprobar_evaluacion(self.colaborador, self.eval2)
        Certificado.objects.create(
            usuario=self.colaborador, curso=self.curso,
            estado='revocado', motivo_revocacion='Fraude detected'
        )

        from certificados.services import CertificateEligibilityService
        is_eligible, reasons = CertificateEligibilityService.check_eligibility(self.colaborador, self.curso)
        self.assertTrue(is_eligible)

    def test_not_eligible_when_enrollment_abandonado(self):
        """User is NOT eligible if enrollment estado is 'abandonado'."""
        self.inscripcion.estado = 'abandonado'
        self.inscripcion.save()
        self._completar_clase(self.colaborador, self.clase1)
        self._completar_clase(self.colaborador, self.clase2)
        self._aprobar_evaluacion(self.colaborador, self.eval1)
        self._aprobar_evaluacion(self.colaborador, self.eval2)

        from certificados.services import CertificateEligibilityService
        is_eligible, reasons = CertificateEligibilityService.check_eligibility(self.colaborador, self.curso)
        self.assertFalse(is_eligible)
        self.assertIn('enrollment', reasons)

    def test_not_eligible_when_course_certificado_activo_false(self):
        """User is NOT eligible if curso.certificado_activo is False."""
        self._completar_clase(self.colaborador, self.clase1)
        self._completar_clase(self.colaborador, self.clase2)
        self._aprobar_evaluacion(self.colaborador, self.eval1)
        self._aprobar_evaluacion(self.colaborador, self.eval2)
        self.curso.certificado_activo = False
        self.curso.save()

        from certificados.services import CertificateEligibilityService
        is_eligible, reasons = CertificateEligibilityService.check_eligibility(self.colaborador, self.curso)
        self.assertFalse(is_eligible)
        self.assertIn('curso', reasons)


class CertificadoSignalTests(TestCase):
    """Integration tests for signal-driven certificate generation.

    Signal handlers in certificados/signals.py create a Certificado with
    estado='aprobado' when all course requirements are met. These tests
    verify the signals fire correctly under various completion scenarios.
    """

    def setUp(self):
        from cursos.models import Clase, ClaseCompletado
        from evaluaciones.models import Evaluacion, IntentoEvaluacion

        self.Clase = Clase
        self.Evaluacion = Evaluacion
        self.ClaseCompletado = ClaseCompletado
        self.IntentoEvaluacion = IntentoEvaluacion

        self.docente = Usuario.objects.create_user(
            username='docente_signal', password='testpass', rol='docente', rut='55555555-5'
        )
        self.colaborador = Usuario.objects.create_user(
            username='colaborador_signal', password='testpass', rol='colaborador', rut='66666666-6'
        )
        self.curso = Curso.objects.create(
            titulo='Curso Signal Test',
            descripcion='Test Desc',
            docente_creador=self.docente,
            estado='publicado',
        )
        self.clase1 = self.Clase.objects.create(curso=self.curso, titulo='Clase 1', orden=1)
        self.clase2 = self.Clase.objects.create(curso=self.curso, titulo='Clase 2', orden=2)
        self.eval1 = self.Evaluacion.objects.create(curso=self.curso, titulo='Eval 1', porcentaje_aprobacion=70)
        self.eval2 = self.Evaluacion.objects.create(curso=self.curso, titulo='Eval 2', porcentaje_aprobacion=70)
        self.inscripcion = InscripcionCurso.objects.create(
            usuario=self.colaborador,
            curso=self.curso,
            estado='en_progreso'
        )

    def test_cert_created_on_last_evaluation_pass(self):
        """Complete all classes + pass all evals -> cert created with estado='aprobado'."""
        from django.db.models.signals import post_save

        with transaction.atomic():
            self.ClaseCompletado.objects.create(usuario=self.colaborador, clase=self.clase1)
            self.ClaseCompletado.objects.create(usuario=self.colaborador, clase=self.clase2)

            self.IntentoEvaluacion.objects.create(
                usuario=self.colaborador, evaluacion=self.eval1,
                puntaje_obtenido=100, aprobado=True
            )
            intento2 = self.IntentoEvaluacion.objects.create(
                usuario=self.colaborador, evaluacion=self.eval2,
                puntaje_obtenido=100, aprobado=True
            )

            post_save.send(sender=self.IntentoEvaluacion, instance=intento2, created=True)

        cert = Certificado.objects.filter(usuario=self.colaborador, curso=self.curso).first()
        self.assertIsNotNone(cert)
        self.assertEqual(cert.estado, 'aprobado')

    def test_no_cert_when_classes_incomplete(self):
        """Complete evals but not classes -> no cert created."""
        from django.db.models.signals import post_save

        with transaction.atomic():
            self.IntentoEvaluacion.objects.create(
                usuario=self.colaborador, evaluacion=self.eval1,
                puntaje_obtenido=100, aprobado=True
            )
            intento2 = self.IntentoEvaluacion.objects.create(
                usuario=self.colaborador, evaluacion=self.eval2,
                puntaje_obtenido=100, aprobado=True
            )

            post_save.send(sender=self.IntentoEvaluacion, instance=intento2, created=True)

        self.assertEqual(Certificado.objects.filter(usuario=self.colaborador, curso=self.curso).count(), 0)

    def test_no_duplicate_cert_on_evaluation_retry(self):
        """Cert already exists, user retries/repasses eval -> no duplicate cert created."""
        from django.db.models.signals import post_save

        with transaction.atomic():
            self.ClaseCompletado.objects.create(usuario=self.colaborador, clase=self.clase1)
            self.ClaseCompletado.objects.create(usuario=self.colaborador, clase=self.clase2)
            self.IntentoEvaluacion.objects.create(
                usuario=self.colaborador, evaluacion=self.eval1,
                puntaje_obtenido=100, aprobado=True
            )
            self.IntentoEvaluacion.objects.create(
                usuario=self.colaborador, evaluacion=self.eval2,
                puntaje_obtenido=100, aprobado=True
            )

            intento_retry = self.IntentoEvaluacion.objects.create(
                usuario=self.colaborador, evaluacion=self.eval2,
                puntaje_obtenido=100, aprobado=True
            )
            post_save.send(sender=self.IntentoEvaluacion, instance=intento_retry, created=True)

        self.assertEqual(Certificado.objects.filter(usuario=self.colaborador, curso=self.curso).count(), 1)

    def test_cert_created_when_classes_completed_last(self):
        """Complete classes last (after evals) -> cert created via ClaseCompletado signal."""
        from django.db.models.signals import post_save

        with transaction.atomic():
            self.IntentoEvaluacion.objects.create(
                usuario=self.colaborador, evaluacion=self.eval1,
                puntaje_obtenido=100, aprobado=True
            )
            self.IntentoEvaluacion.objects.create(
                usuario=self.colaborador, evaluacion=self.eval2,
                puntaje_obtenido=100, aprobado=True
            )

            self.ClaseCompletado.objects.create(usuario=self.colaborador, clase=self.clase1)
            completado = self.ClaseCompletado.objects.create(
                usuario=self.colaborador, clase=self.clase2
            )

            post_save.send(sender=self.ClaseCompletado, instance=completado, created=True)

        cert = Certificado.objects.filter(usuario=self.colaborador, curso=self.curso).first()
        self.assertIsNotNone(cert)
        self.assertEqual(cert.estado, 'aprobado')

    def test_cert_not_created_when_enrollment_abandonado(self):
        """Enrollment is 'abandonado' -> no cert even if all complete."""
        from django.db.models.signals import post_save

        self.inscripcion.estado = 'abandonado'
        self.inscripcion.save()

        with transaction.atomic():
            self.ClaseCompletado.objects.create(usuario=self.colaborador, clase=self.clase1)
            self.ClaseCompletado.objects.create(usuario=self.colaborador, clase=self.clase2)
            self.IntentoEvaluacion.objects.create(
                usuario=self.colaborador, evaluacion=self.eval1,
                puntaje_obtenido=100, aprobado=True
            )
            intento2 = self.IntentoEvaluacion.objects.create(
                usuario=self.colaborador, evaluacion=self.eval2,
                puntaje_obtenido=100, aprobado=True
            )

            post_save.send(sender=self.IntentoEvaluacion, instance=intento2, created=True)

        self.assertEqual(Certificado.objects.filter(usuario=self.colaborador, curso=self.curso).count(), 0)
