from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Curso, Material, InscripcionCurso, Categoria


@login_required
def curso_list(request):
    query = request.GET.get('q', '')
    estado_filter = request.GET.get('estado', '')
    categoria_filter = request.GET.get('categoria', '')
    
    if request.user.rol in ['admin', 'docente']:
        cursos = Curso.objects.select_related('docente_creador', 'categoria')
    else:
        cursos = Curso.objects.filter(estado='publicado').select_related('categoria')
    
    if query:
        cursos = cursos.filter(titulo__icontains=query)
    
    if estado_filter:
        cursos = cursos.filter(estado=estado_filter)
    
    if categoria_filter:
        cursos = cursos.filter(categoria_id=categoria_filter)
    
    cursos = cursos.order_by('-fecha_creacion')
    
    paginator = Paginator(cursos, 15)
    page_number = request.GET.get('page', 1)
    cursos_page = paginator.get_page(page_number)
    
    return render(request, 'cursos/curso_list.html', {
        'cursos': cursos_page,
        'page_obj': cursos_page,
        'is_docente': request.user.rol in ['admin', 'docente'],
        'query': query,
        'estado_filter': estado_filter,
        'categoria_filter': categoria_filter,
        'categorias': Categoria.objects.all(),
        'now': timezone.now()
    })


@login_required
def curso_create(request):
    if request.user.rol not in ['admin', 'docente']:
        messages.error(request, 'No tienes permisos para crear cursos.')
        return redirect('cursos:curso_list')
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado', 'borrador')
        fecha_limite = request.POST.get('fecha_limite')
        
        curso = Curso.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            docente_creador=request.user,
            estado=estado,
            fecha_limite=fecha_limite or None,
            categoria_id=request.POST.get('categoria') or None
        )
        
        messages.success(request, f'Curso "{curso.titulo}" creado exitosamente.')
        return redirect('cursos:curso_detail', pk=curso.id)
    
    return render(request, 'cursos/curso_form.html', {
        'accion': 'crear',
        'curso': None,
        'categorias': Categoria.objects.all()
    })


@login_required
def curso_edit(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    
    # Permisos: docente creador o admin
    if request.user.rol not in ['admin', 'docente']:
        return HttpResponseForbidden('No tienes permisos para editar este curso.')
    if request.user.rol == 'docente' and curso.docente_creador != request.user and request.user.rol != 'admin':
        return HttpResponseForbidden('No puedes editar este curso.')
    
    if request.method == 'POST':
        curso.titulo = request.POST.get('titulo')
        curso.descripcion = request.POST.get('descripcion')
        curso.estado = request.POST.get('estado', 'borrador')
        curso.fecha_limite = request.POST.get('fecha_limite') or None
        curso.categoria_id = request.POST.get('categoria') or None
        curso.save()
        
        messages.success(request, f'Curso "{curso.titulo}" actualizado.')
        return redirect('cursos:curso_detail', pk=curso.id)
    
    return render(request, 'cursos/curso_form.html', {
        'accion': 'editar',
        'curso': curso,
        'categorias': Categoria.objects.all()
    })


@login_required
def curso_detail(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    
    # Si es borrador, solo lo ve el creador, admin, o usuarios inscritos
    if curso.estado == 'borrador':
        is_enrolled = InscripcionCurso.objects.filter(usuario=request.user, curso=curso).exists()
        if not is_enrolled:
            if request.user.rol not in ['admin', 'docente']:
                return HttpResponseForbidden('Este curso no está disponible.')
            if request.user.rol == 'docente' and curso.docente_creador != request.user:
                return HttpResponseForbidden('Este curso no está disponible.')
    
    materiales = curso.materiales.all()
    
    # Verificar si el usuario está InscripcionCurso
    inscripcion = None
    course_progress = None
    if request.user.rol == 'colaborador':
        inscripcion = InscripcionCurso.objects.filter(usuario=request.user, curso=curso).first()
        
        total_evals = curso.evaluaciones.count()
        if total_evals > 0:
            from evaluaciones.models import IntentoEvaluacion
            aprobadas = IntentoEvaluacion.objects.filter(
                evaluacion__curso=curso,
                usuario=request.user,
                aprobado=True
            ).values('evaluacion').distinct().count()
            course_progress = int((aprobadas / total_evals) * 100)
        else:
            course_progress = 0
    
    puede_editar = request.user.rol == 'admin' or (
        request.user.rol == 'docente' and curso.docente_creador == request.user
    )
    
    from django.utils import timezone
    
    return render(request, 'cursos/curso_detail.html', {
        'curso': curso,
        'materiales': materiales,
        'inscripcion': inscripcion,
        'puede_editar': puede_editar,
        'course_progress': course_progress,
        'now': timezone.now()
    })


@login_required
def curso_delete(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    
    # Solo admin o creador pueden eliminar
    if request.user.rol not in ['admin', 'docente']:
        return HttpResponseForbidden('No tienes permisos para eliminar este curso.')
    if request.user.rol == 'docente' and curso.docente_creador != request.user:
        return HttpResponseForbidden('No puedes eliminar este curso.')
    
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso eliminado exitosamente.')
        return redirect('cursos:curso_list')
    
    messages.error(request, 'Método no permitido.')
    return redirect('cursos:curso_detail', pk=pk)


@login_required
def material_create(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    
    # Solo docente creador o admin puede agregar material
    if request.user.rol not in ['admin', 'docente']:
        return HttpResponseForbidden('No tienes permisos para agregar material.')
    if request.user.rol == 'docente' and curso.docente_creador != request.user:
        return HttpResponseForbidden('No puedes agregar material a este curso.')
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        tipo = request.POST.get('tipo')
        archivo = request.FILES.get('archivo')
        url = request.POST.get('url')
        
        material = Material.objects.create(
            curso=curso,
            titulo=titulo,
            tipo=tipo,
            archivo=archivo,
            url=url
        )
        
        messages.success(request, f'Material "{material.titulo}" agregado.')
        return redirect('cursos:curso_detail', pk=curso.id)
    
    return render(request, 'cursos/material_form.html', {
        'curso': curso,
        'accion': 'crear'
    })


@login_required
def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    curso = material.curso
    
    # Solo docente creador o admin puede eliminar material
    if request.user.rol not in ['admin', 'docente']:
        return HttpResponseForbidden('No tienes permisos para eliminar material.')
    if request.user.rol == 'docente' and curso.docente_creador != request.user:
        return HttpResponseForbidden('No puedes eliminar este material.')
    
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Material eliminado.')
        return redirect('cursos:curso_detail', pk=curso.id)
    
    messages.error(request, 'Método no permitido.')
    return redirect('cursos:curso_detail', pk=curso.id)


@login_required
def categoria_list(request):
    if request.user.rol != 'admin':
        return HttpResponseForbidden('No tienes permisos para acceder a categorías.')
    
    categorias = Categoria.objects.all()
    return render(request, 'cursos/categoria_list.html', {'categorias': categorias})


@login_required
def categoria_create(request):
    if request.user.rol != 'admin':
        return HttpResponseForbidden('No tienes permisos para crear categorías.')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        color = request.POST.get('color', '#6366f1')
        descripcion = request.POST.get('descripcion', '')
        
        Categoria.objects.create(
            nombre=nombre,
            color=color,
            descripcion=descripcion
        )
        messages.success(request, f'Categoría "{nombre}" creada.')
        return redirect('cursos:categoria_list')
    
    return render(request, 'cursos/categoria_form.html', {'accion': 'crear'})


@login_required
def categoria_edit(request, pk):
    if request.user.rol != 'admin':
        return HttpResponseForbidden('No tienes permisos para editar categorías.')
    
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre')
        categoria.color = request.POST.get('color', '#6366f1')
        categoria.descripcion = request.POST.get('descripcion', '')
        categoria.save()
        messages.success(request, f'Categoría "{categoria.nombre}" actualizada.')
        return redirect('cursos:categoria_list')
    
    return render(request, 'cursos/categoria_form.html', {
        'accion': 'editar',
        'categoria': categoria
    })


@login_required
def categoria_delete(request, pk):
    if request.user.rol != 'admin':
        return HttpResponseForbidden('No tienes permisos para eliminar categorías.')
    
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada.')
        return redirect('cursos:categoria_list')
    
    return render(request, 'cursos/categoria_confirm_delete.html', {'categoria': categoria})