from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from weasyprint import HTML
from .models import Certificado
from cursos.models import Curso, InscripcionCurso
from usuarios.decorators import admin_required, docente_or_admin_required, course_owner_or_admin, owner_or_admin
from usuarios.models import Auditoria


@login_required
@admin_required
def certificado_list(request):
    certificados = Certificado.objects.select_related('usuario', 'curso').order_by('-fecha_emision')
    paginator = Paginator(certificados, 20)
    page_number = request.GET.get('page', 1)
    certificados_page = paginator.get_page(page_number)
    return render(request, 'certificados/admin_certificado_list.html', {
        'certificados': certificados_page,
        'page_obj': certificados_page
    })


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
            'estado': cert.estado if cert else None
        })
    
    context = {'certificados': disponibles}
    return render(request, 'certificados/mis_certificados.html', context)


@login_required
@owner_or_admin(Certificado, 'usuario')
def descargar_certificado(request, pk):
    certificado = get_object_or_404(Certificado, pk=pk)
    
    if certificado.estado != 'aprobado':
        messages.error(request, 'El certificado aún no ha sido aprobado.')
        return redirect('certificados:mis_certificados')
    
    # Lazy PDF generation: create PDF on first download if it doesn't exist
    if not certificado.archivo_pdf:
        from django.template.loader import render_to_string
        from django.utils import timezone
        from django.core.files.base import ContentFile
        from weasyprint import HTML
        
        fecha_str = timezone.now().strftime('%d de %B de %Y')
        html_string = render_to_string('certificados/certificado_pdf.html', {
            'curso': certificado.curso,
            'fecha': fecha_str,
            'nombre_usuario': certificado.usuario.get_full_name() or certificado.usuario.username,
        })
        pdf_file = HTML(string=html_string).write_pdf()
        certificado.archivo_pdf.save(
            f'certificado_{certificado.pk}.pdf',
            ContentFile(pdf_file)
        )
    
    certificado.archivo_pdf.seek(0)
    return FileResponse(certificado.archivo_pdf, content_type='application/pdf')


@login_required
@admin_required
def eliminar_certificado(request, pk):
    certificado = get_object_or_404(Certificado, pk=pk)
    
    if request.method == 'POST':
        certificado.delete()
        messages.success(request, 'Certificado eliminado.')
    
    return redirect('certificados:certificado_list')


def verificar_certificado(request, codigo):
    certificado = get_object_or_404(Certificado, codigo_verificacion=codigo)
    context = {'certificado': certificado}
    if certificado.estado == 'aprobado':
        context['valido'] = True
    elif certificado.estado == 'rechazado':
        context['valido'] = False
        context['razon'] = 'Este certificado ha sido rechazado.'
    else:
        context['valido'] = False
        context['razon'] = 'Este certificado aún no ha sido aprobado.'
    return render(request, 'certificados/verificar_certificado.html', context)


@login_required
@docente_or_admin_required
def certificados_pendientes(request):
    """Show pending certificates for approval."""
    if request.user.rol == 'admin':
        certificados = Certificado.objects.filter(
            estado='pendiente'
        ).select_related('usuario', 'curso')
    else:
        certificados = Certificado.objects.filter(
            estado='pendiente',
            curso__docente_creador=request.user
        ).select_related('usuario', 'curso')

    return render(request, 'certificados/certificados_pendientes.html', {
        'certificados': certificados
    })


@login_required
@owner_or_admin(Certificado, 'curso.docente_creador')
@docente_or_admin_required
def aprobar_certificado(request, pk):
    """Approve a pending certificate."""
    certificado = get_object_or_404(Certificado, pk=pk)

    if request.method == 'POST':
        from django.utils import timezone
        certificado.estado = 'aprobado'
        certificado.fecha_aprobacion = timezone.now()
        certificado.aprobado_por = request.user
        certificado.save()
        Auditoria.objects.create(
            usuario=request.user,
            accion='certificado_aprobado',
            descripcion=f'Certificado de {certificado.usuario.username} para {certificado.curso.titulo} aprobado',
            objeto_tipo='Certificado',
            objeto_id=certificado.pk
        )
        messages.success(request, f'Certificado de {certificado.usuario.get_full_name()} aprobado.')

    return redirect('certificados:certificados_pendientes')


@login_required
@owner_or_admin(Certificado, 'curso.docente_creador')
@docente_or_admin_required
def rechazar_certificado(request, pk):
    """Reject a pending certificate."""
    certificado = get_object_or_404(Certificado, pk=pk)

    if request.method == 'POST':
        certificado.estado = 'rechazado'
        certificado.save()
        messages.warning(request, f'Certificado de {certificado.usuario.get_full_name()} rechazado.')

    return redirect('certificados:certificados_pendientes')


@login_required
@owner_or_admin(Certificado, 'curso.docente_creador')
@docente_or_admin_required
def resetear_certificado(request, pk):
    """Reset a rejected certificate back to pending."""
    certificado = get_object_or_404(Certificado, pk=pk)

    if request.method == 'POST':
        certificado.estado = 'pendiente'
        certificado.save()
        messages.info(request, f'Certificado de {certificado.usuario.get_full_name()} reseteado a pendiente.')

    return redirect('certificados:certificados_pendientes')


@login_required
@owner_or_admin(Certificado, 'curso.docente_creador')
@docente_or_admin_required
def revocar_certificado(request, pk):
    """Revoke an approved certificate with a required reason."""
    certificado = get_object_or_404(Certificado, pk=pk)

    if request.method == 'POST':
        motivo_revocacion = request.POST.get('motivo_revocacion', '').strip()
        if not motivo_revocacion:
            messages.error(request, 'Debe proporcionar un motivo de revocación.')
            return redirect('certificados:certificado_list')

        certificado.estado = 'revocado'
        certificado.motivo_revocacion = motivo_revocacion
        certificado.save()
        messages.success(request, f'Certificado de {certificado.usuario.get_full_name()} revocado.')

    return redirect('certificados:certificado_list')
