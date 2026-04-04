from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from io import BytesIO
from weasyprint import HTML
from .models import Certificado
from cursos.models import Curso, InscripcionCurso


@login_required
def certificado_list(request):
    if request.user.rol == 'admin':
        certificados = Certificado.objects.select_related('usuario', 'curso').order_by('-fecha_emision')
        paginator = Paginator(certificados, 20)
        page_number = request.GET.get('page', 1)
        certificados_page = paginator.get_page(page_number)
        return render(request, 'certificados/admin_certificado_list.html', {
            'certificados': certificados_page,
            'page_obj': certificados_page
        })
    else:
        return redirect('certificados:mis_certificados')


@login_required
def mis_certificados(request):
    if request.user.rol == 'admin':
        return redirect('certificados:certificado_list')
    
    from django.db.models import Prefetch
    
    cursos_inscritos = InscripcionCurso.objects.filter(
        usuario=request.user,
        estado='completado'
    ).select_related('curso')
    
    certificados_por_curso = {
        c.curso_id: c 
        for c in Certificado.objects.filter(usuario=request.user)
    }
    
    disponibles = []
    for inscripcion in cursos_inscritos:
        cert = certificados_por_curso.get(inscripcion.curso_id)
        disponibles.append({
            'curso': inscripcion.curso,
            'certificado': cert,
            'aprobado': True
        })
    
    context = {'certificados': disponibles}
    return render(request, 'certificados/mis_certificados.html', context)


@login_required
def generar_certificado(request, curso_pk):
    curso = get_object_or_404(Curso, pk=curso_pk)
    
    if request.user.rol not in ['admin', 'docente']:
        messages.error(request, 'No tienes permisos para generar certificados.')
        return redirect('cursos:curso_detail', pk=curso_pk)
    
    try:
        from django.utils import timezone
        fecha_str = timezone.now().strftime('%d de %B de %Y')
        
        html_string = render_to_string('certificados/certificado_pdf.html', {
            'curso': curso,
            'fecha': fecha_str,
            'nombre_usuario': request.user.get_full_name() or request.user.username,
        })
        
        pdf_file = HTML(string=html_string).write_pdf()
        pdf_buffer = BytesIO(pdf_file)
        
        Certificado.objects.create(
            usuario=request.user,
            curso=curso,
            archivo_pdf=pdf_buffer
        )
        
        for inscripcion in InscripcionCurso.objects.filter(curso=curso):
            tiene_certificado = True
            for evaluacion in curso.evaluaciones.all():
                ultimo = evaluacion.intentos.filter(usuario=inscripcion.usuario).order_by('-fecha_intento').first()
                if not ultimo or not ultimo.aprobado:
                    tiene_certificado = False
                    break
            
            if tiene_certificado:
                pdf_copy = BytesIO(pdf_file)
                Certificado.objects.get_or_create(
                    usuario=inscripcion.usuario,
                    curso=curso,
                    defaults={'archivo_pdf': pdf_copy}
                )
        
        messages.success(request, 'Certificado generado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al generar certificado: {str(e)}')
    
    if request.user.rol == 'admin':
        return redirect('certificados:certificado_list')
    return redirect('cursos:curso_detail', pk=curso_pk)


@login_required
def descargar_certificado(request, pk):
    certificado = get_object_or_404(Certificado, pk=pk)
    
    if request.user != certificado.usuario and request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para descargar este certificado.')
        return redirect('certificados:mis_certificados')
    
    if certificado.archivo_pdf:
        certificado.archivo_pdf.seek(0)
        return FileResponse(certificado.archivo_pdf, content_type='application/pdf')
    raise Http404("Certificado no encontrado")


@login_required
def eliminar_certificado(request, pk):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para eliminar certificados.')
        return redirect('certificados:certificado_list')
    
    certificado = get_object_or_404(Certificado, pk=pk)
    
    if request.method == 'POST':
        certificado.delete()
        messages.success(request, 'Certificado eliminado.')
    
    return redirect('certificados:certificado_list')


def verificar_certificado(request, codigo):
    certificado = get_object_or_404(Certificado, codigo_verificacion=codigo)
    context = {'certificado': certificado, 'valido': True}
    return render(request, 'certificados/verificar_certificado.html', context)