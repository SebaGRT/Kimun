from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from cursos.models import Curso, InscripcionCurso
from evaluaciones.models import Evaluacion, IntentoEvaluacion
from certificados.models import Certificado
from usuarios.models import Usuario


@login_required
def dashboard_reportes(request):
    if request.user.rol != 'admin':
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No tienes acceso a reportes")
    
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
    }
    return render(request, 'reportes/dashboard.html', context)


@login_required
def reporte_curso(request, curso_pk):
    if request.user.rol != 'admin':
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No tienes acceso a reportes")
    
    curso = get_object_or_404(Curso, pk=curso_pk)
    inscripciones = InscripcionCurso.objects.filter(curso=curso).select_related('usuario')
    
    evaluaciones = curso.evaluaciones.all()
    
    for inscripcion in inscripciones:
        inscripcion.intentos_count = 0
        inscripcion.aprobado = True
        for evaluacion in evaluaciones:
            ultimo = evaluacion.intentos.filter(usuario=inscripcion.usuario).order_by('-fecha_intento').first()
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
def reporte_usuario(request, usuario_pk):
    if request.user.rol != 'admin':
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No tienes acceso a reportes")
    
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