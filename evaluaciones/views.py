from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Evaluacion, Pregunta, Alternativa, IntentoEvaluacion
from cursos.models import Curso, InscripcionCurso
import json


def evaluacion_list(request, curso_pk):
    curso = get_object_or_404(Curso, pk=curso_pk)
    evaluaciones = curso.evaluaciones.prefetch_related('intentos').all()
    
    for evaluacion in evaluaciones:
        evaluacion.intentos_del_usuario = evaluacion.intentos.filter(usuario=request.user).count()
    
    context = {
        'curso': curso,
        'evaluaciones': evaluaciones,
    }
    return render(request, 'evaluaciones/evaluacion_list.html', context)


@login_required
def evaluacion_create(request, curso_pk):
    curso = get_object_or_404(Curso, pk=curso_pk)
    
    if request.user.rol not in ['admin', 'docente']:
        messages.error(request, 'No tienes permisos para crear evaluaciones.')
        return redirect('cursos:curso_detail', pk=curso_pk)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        porcentaje_aprobacion = request.POST.get('porcentaje_aprobacion', 70)
        
        evaluacion = Evaluacion.objects.create(
            curso=curso,
            titulo=titulo,
            porcentaje_aprobacion=int(porcentaje_aprobacion)
        )
        
        preguntas_data = json.loads(request.POST.get('preguntas', '[]'))
        
        for pregunta_data in preguntas_data:
            pregunta = Pregunta.objects.create(
                evaluacion=evaluacion,
                texto=pregunta_data['texto']
            )
            
            for alt_data in pregunta_data['alternativas']:
                Alternativa.objects.create(
                    pregunta=pregunta,
                    texto=alt_data['texto'],
                    es_correcta=alt_data.get('es_correcta', False)
                )
        
        messages.success(request, 'Evaluación creada exitosamente.')
        return redirect('evaluaciones:evaluacion_list', curso_pk=curso_pk)
    
    context = {'curso': curso}
    return render(request, 'evaluaciones/evaluacion_form.html', context)


@login_required
def evaluacion_edit(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    
    if request.user.rol not in ['admin', 'docente']:
        messages.error(request, 'No tienes permisos para editar evaluaciones.')
        return redirect('cursos:curso_detail', pk=evaluacion.curso.pk)
    
    if request.method == 'POST':
        evaluacion.titulo = request.POST.get('titulo')
        evaluacion.porcentaje_aprobacion = int(request.POST.get('porcentaje_aprobacion', 70))
        evaluacion.save()
        
        evaluacion.preguntas.all().delete()
        
        preguntas_data = json.loads(request.POST.get('preguntas', '[]'))
        
        for pregunta_data in preguntas_data:
            pregunta = Pregunta.objects.create(
                evaluacion=evaluacion,
                texto=pregunta_data['texto']
            )
            
            for alt_data in pregunta_data['alternativas']:
                Alternativa.objects.create(
                    pregunta=pregunta,
                    texto=alt_data['texto'],
                    es_correcta=alt_data.get('es_correcta', False)
                )
        
        messages.success(request, 'Evaluación actualizada.')
        return redirect('evaluaciones:evaluacion_list', curso_pk=evaluacion.curso.pk)
    
    context = {
        'evaluacion': evaluacion,
        'curso': evaluacion.curso,
    }
    return render(request, 'evaluaciones/evaluacion_form.html', context)


@login_required
def evaluacion_delete(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    
    if request.user.rol not in ['admin', 'docente']:
        messages.error(request, 'No tienes permisos para eliminar evaluaciones.')
        return redirect('cursos:curso_detail', pk=evaluacion.curso.pk)
    
    if request.method == 'POST':
        curso_pk = evaluacion.curso.pk
        evaluacion.delete()
        messages.success(request, 'Evaluación eliminada.')
        return redirect('evaluaciones:evaluacion_list', curso_pk=curso_pk)
    
    context = {'evaluacion': evaluacion}
    return render(request, 'evaluaciones/evaluacion_confirm_delete.html', context)


@login_required
def tomar_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    
    inscripcion = InscripcionCurso.objects.filter(
        usuario=request.user,
        curso=evaluacion.curso
    ).first()
    
    if not inscripcion:
        messages.error(request, 'No estás inscrito en este curso.')
        return redirect('cursos:curso_detail', pk=evaluacion.curso.pk)
    
    preguntas = evaluacion.preguntas.prefetch_related('alternativas').all()
    
    if request.method == 'POST':
        respuestas = json.loads(request.POST.get('respuestas', '{}'))
        
        total_preguntas = preguntas.count()
        respuestas_correctas = 0
        
        for pregunta in preguntas:
            respuesta_seleccionada = respuestas.get(str(pregunta.pk))
            if respuesta_seleccionada:
                alternativa_correcta = pregunta.alternativas.filter(es_correcta=True).first()
                if alternativa_correcta and str(alternativa_correcta.pk) == respuesta_seleccionada:
                    respuestas_correctas += 1
        
        puntaje = int((respuestas_correctas / total_preguntas) * 100) if total_preguntas > 0 else 0
        aprobado = puntaje >= evaluacion.porcentaje_aprobacion
        
        intento = IntentoEvaluacion.objects.create(
            usuario=request.user,
            evaluacion=evaluacion,
            puntaje_obtenido=puntaje,
            aprobado=aprobado
        )
        
        from cursos.models import InscripcionCurso
        curso = evaluacion.curso
        if curso.evaluaciones.exists():
            todas_aprobadas = True
            for ev in curso.evaluaciones.all():
                ultimo = ev.intentos.filter(usuario=request.user).order_by('-fecha_intento').first()
                if not ultimo or not ultimo.aprobado:
                    todas_aprobadas = False
                    break
            
            if todas_aprobadas:
                inscripcion = InscripcionCurso.objects.filter(
                    usuario=request.user,
                    curso=curso
                ).first()
                if inscripcion and inscripcion.estado != 'completado':
                    inscripcion.estado = 'completado'
                    inscripcion.save()
        
        return redirect('evaluaciones:resultado_evaluacion', pk=pk, intento_pk=intento.pk)
    
    context = {
        'evaluacion': evaluacion,
        'preguntas': preguntas,
    }
    return render(request, 'evaluaciones/tomar_evaluacion.html', context)


@login_required
def resultado_evaluacion(request, pk, intento_pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    intento = get_object_or_404(IntentoEvaluacion, pk=intento_pk, usuario=request.user, evaluacion=evaluacion)
    
    preguntas = evaluacion.preguntas.prefetch_related('alternativas').all()
    
    context = {
        'evaluacion': evaluacion,
        'intento': intento,
        'preguntas': preguntas,
    }
    return render(request, 'evaluaciones/resultado_evaluacion.html', context)


@login_required
@require_POST
def responder_pregunta_htmx(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    data = json.loads(request.body)
    pregunta_pk = data.get('pregunta_pk')
    alternativa_pk = data.get('alternativa_pk')
    
    pregunta = get_object_or_404(Pregunta, pk=pregunta_pk, evaluacion=evaluacion)
    alternativa = get_object_or_404(Alternativa, pk=alternativa_pk, pregunta=pregunta)
    
    es_correcta = alternativa.es_correcta
    
    return JsonResponse({'correcta': es_correcta})