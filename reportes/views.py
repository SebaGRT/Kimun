# pyright: reportAttributeAccessIssue=false

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Max
from django.utils import timezone
from datetime import timedelta
from cursos.models import Curso, InscripcionCurso
from evaluaciones.models import Evaluacion, IntentoEvaluacion
from certificados.models import Certificado
from usuarios.models import Usuario
from usuarios.decorators import admin_required


def get_at_risk_students():
    """Returns list of dicts with user and risk reason."""
    from collections import defaultdict
    from cursos.models import ClaseCompletado

    at_risk = []
    seven_days_ago = timezone.now() - timedelta(days=7)

    enrollments = InscripcionCurso.objects.filter(
        estado__in=['asignado', 'en_progreso']
    ).select_related('usuario', 'curso')

    usuario_ids = [e.usuario_id for e in enrollments]
    curso_ids = [e.curso_id for e in enrollments]

    progress_pairs = set(
        ClaseCompletado.objects.filter(
            usuario_id__in=usuario_ids,
            clase__curso_id__in=curso_ids
        ).values_list('usuario_id', 'clase__curso_id')
    )

    passed_pairs = set(
        IntentoEvaluacion.objects.filter(
            usuario_id__in=usuario_ids,
            evaluacion__curso_id__in=curso_ids,
            aprobado=True
        ).values_list('usuario_id', 'evaluacion__curso_id')
    )

    all_attempts = IntentoEvaluacion.objects.filter(
        usuario_id__in=usuario_ids,
        evaluacion__curso_id__in=curso_ids
    ).select_related('evaluacion')

    attempts_by_user_course = defaultdict(list)
    for attempt in all_attempts:
        attempts_by_user_course[(attempt.usuario_id, attempt.evaluacion.curso_id)].append(attempt)

    latest_progress_dates = {}
    for row in ClaseCompletado.objects.filter(
        usuario_id__in=usuario_ids,
        clase__curso_id__in=curso_ids
    ).values('usuario_id', 'clase__curso_id').annotate(max_fecha=Max('fecha_completado')):
        latest_progress_dates[(row['usuario_id'], row['clase__curso_id'])] = row['max_fecha']

    for enrollment in enrollments:
        risk_reason = None

        if enrollment.fecha_asignacion < seven_days_ago:
            if not hasattr(enrollment, 'completado') or not enrollment.completado:
                if (enrollment.usuario_id, enrollment.curso_id) not in progress_pairs:
                    risk_reason = "Sin actividad en 7+ días"

        if enrollment.curso.fecha_limite:
            days_to_deadline = (enrollment.curso.fecha_limite - timezone.now()).days
            if days_to_deadline <= 7 and days_to_deadline > 0:
                if (enrollment.usuario_id, enrollment.curso_id) not in passed_pairs:
                    risk_reason = f"Deadline en {days_to_deadline} días sin aprobar evaluaciones"

        failed_all = False
        attempts = attempts_by_user_course.get((enrollment.usuario_id, enrollment.curso_id), [])
        if attempts:
            if all(attempt.aprobado == False for attempt in attempts):
                failed_all = True
                risk_reason = "Ha reprobado todas las evaluaciones"

        if risk_reason:
            ultima_actividad = enrollment.fecha_asignacion
            max_fecha = latest_progress_dates.get((enrollment.usuario_id, enrollment.curso_id))
            if max_fecha and max_fecha > ultima_actividad:
                ultima_actividad = max_fecha

            at_risk.append({
                'usuario': enrollment.usuario,
                'estado': enrollment.get_estado_display(),
                'ultima_actividad': ultima_actividad.strftime("%d/%m/%Y %H:%M"),
                'riesgo': risk_reason
            })

    return at_risk


@login_required
@admin_required
def dashboard_reportes(request):
    total_usuarios = Usuario.objects.count()
    total_cursos = Curso.objects.count()
    total_inscripciones = InscripcionCurso.objects.count()
    total_certificados = Certificado.objects.count()
    
    cursos_con_mas_inscritos = Curso.objects.annotate(
        num_inscripciones=Count('inscripciones')
    ).order_by('-num_inscripciones')[:5]
    
    usuarios_por_rol = Usuario.objects.values('rol').annotate(count=Count('id'))
    
    inscripciones_por_estado = InscripcionCurso.objects.values('estado').annotate(count=Count('id'))
    
    evaluaciones_promedio = IntentoEvaluacion.objects.aggregate(promedio=Avg('puntaje_obtenido'))
    
    ultimas_inscripciones = InscripcionCurso.objects.select_related('usuario', 'curso').order_by('-fecha_asignacion')[:10]
    
    context = {
        'total_usuarios': total_usuarios,
        'total_cursos': total_cursos,
        'total_inscripciones': total_inscripciones,
        'total_certificados': total_certificados,
        'cursos_con_mas_inscritos': cursos_con_mas_inscritos,
        'usuarios_por_rol': usuarios_por_rol,
        'inscripciones_por_estado': inscripciones_por_estado,
        'promedio_evaluaciones': evaluaciones_promedio['promedio'] or 0,
        'ultimas_inscripciones': ultimas_inscripciones,
        'estudiantes_en_riesgo': get_at_risk_students(),
    }
    return render(request, 'reportes/dashboard.html', context)


@login_required
@admin_required
def reporte_curso(request, curso_pk):
    curso = get_object_or_404(Curso, pk=curso_pk)
    inscripciones = InscripcionCurso.objects.filter(curso=curso).select_related('usuario')
    
    evaluaciones = list(curso.evaluaciones.all())
    
    usuario_ids = [i.usuario_id for i in inscripciones]
    evaluacion_ids = [e.id for e in evaluaciones]
    
    all_attempts = IntentoEvaluacion.objects.filter(
        usuario_id__in=usuario_ids,
        evaluacion_id__in=evaluacion_ids
    ).select_related('evaluacion')
    
    latest_by_user_eval = {}
    for attempt in all_attempts:
        key = (attempt.usuario_id, attempt.evaluacion_id)
        if key not in latest_by_user_eval or attempt.fecha_intento > latest_by_user_eval[key].fecha_intento:
            latest_by_user_eval[key] = attempt
    
    for inscripcion in inscripciones:
        inscripcion.intentos_count = 0
        inscripcion.aprobado = True
        for evaluacion in evaluaciones:
            key = (inscripcion.usuario_id, evaluacion.id)
            ultimo = latest_by_user_eval.get(key)
            if ultimo:
                inscripcion.intentos_count += 1
                if not ultimo.aprobado:
                    inscripcion.aprobado = False
    
    context = {
        'curso': curso,
        'inscripciones': inscripciones,
        'evaluaciones': evaluaciones,
    }
    return render(request, 'reportes/reporte_curso.html', context)


@login_required
@admin_required
def reporte_usuario(request, usuario_pk):
    usuario = get_object_or_404(Usuario, pk=usuario_pk)
    inscripciones = InscripcionCurso.objects.filter(usuario=usuario).select_related('curso')
    intentos = IntentoEvaluacion.objects.filter(usuario=usuario).select_related('evaluacion')
    certificados = Certificado.objects.filter(usuario=usuario).select_related('curso')
    
    context = {
        'usuario': usuario,
        'inscripciones': inscripciones,
        'intentos': intentos,
        'certificados': certificados,
    }
    return render(request, 'reportes/reporte_usuario.html', context)


@login_required
@admin_required
def progreso_heatmap(request):
    from cursos.models import Curso, InscripcionCurso, Clase, ClaseCompletado
    from evaluaciones.models import Evaluacion, IntentoEvaluacion
    
    curso_id = request.GET.get('curso')
    cursos = Curso.objects.all()
    
    heatmap_data = []
    
    if curso_id:
        curso = get_object_or_404(Curso, pk=curso_id)
        enrollments = InscripcionCurso.objects.filter(curso=curso).select_related('usuario')
        
        clases = list(curso.clases.all())
        evaluaciones = list(curso.evaluaciones.all())
        
        if enrollments:
            usuario_ids = [e.usuario_id for e in enrollments]
            clase_ids = [c.id for c in clases]
            evaluacion_ids = [e.id for e in evaluaciones]
            
            completados_set = set(
                ClaseCompletado.objects.filter(
                    clase_id__in=clase_ids,
                    usuario_id__in=usuario_ids
                ).values_list('usuario_id', 'clase_id')
            )
            
            all_intentos = IntentoEvaluacion.objects.filter(
                evaluacion_id__in=evaluacion_ids,
                usuario_id__in=usuario_ids
            ).select_related('evaluacion')
            
            latest_intento_by_user_eval = {}
            intento_count_by_user_eval = {}
            for intento in all_intentos:
                key = (intento.usuario_id, intento.evaluacion_id)
                if key not in latest_intento_by_user_eval or intento.fecha_intento > latest_intento_by_user_eval[key].fecha_intento:
                    latest_intento_by_user_eval[key] = intento
                intento_count_by_user_eval[key] = intento_count_by_user_eval.get(key, 0) + 1
        
        for enrollment in enrollments:
            student_data = {
                'usuario': enrollment.usuario,
                'estado': enrollment.estado,
                'items': []
            }
            
            for clase in clases:
                completado = (enrollment.usuario_id, clase.id) in completados_set
                student_data['items'].append({
                    'tipo': 'clase',
                    'titulo': clase.titulo,
                    'completado': completado
                })
            
            for evaluacion in evaluaciones:
                key = (enrollment.usuario_id, evaluacion.id)
                ultimo_intento = latest_intento_by_user_eval.get(key)
                
                student_data['items'].append({
                    'tipo': 'evaluacion',
                    'titulo': evaluacion.titulo,
                    'completado': ultimo_intento.aprobado if ultimo_intento else False,
                    'intentos': intento_count_by_user_eval.get(key, 0)
                })
            
            heatmap_data.append(student_data)
    
    context = {
        'cursos': cursos,
        'curso_id': int(curso_id) if curso_id else None,
        'heatmap_data': heatmap_data,
    }
    return render(request, 'reportes/progreso_heatmap.html', context)

