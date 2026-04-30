from functools import wraps
from django.http import HttpResponseForbidden
from cursos.models import Curso


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request, 'user') or not request.user.is_authenticated:
                return HttpResponseForbidden('Debes iniciar sesión.')
            
            if request.user.rol not in roles:
                return HttpResponseForbidden('No tienes permisos para acceder a esta página.')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def course_owner_or_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return HttpResponseForbidden('Debes iniciar sesión.')

        if request.user.rol == 'admin':
            return view_func(request, *args, **kwargs)

        if request.user.rol == 'docente':
            curso_pk = kwargs.get('pk') or kwargs.get('curso_pk')

            if curso_pk:
                try:
                    curso = Curso.objects.get(pk=curso_pk)
                    if curso.docente_creador == request.user:
                        return view_func(request, *args, **kwargs)
                except Curso.DoesNotExist:
                    pass

            return HttpResponseForbidden('No tienes permisos para acceder a este curso.')

        return HttpResponseForbidden('No tienes permisos para acceder a esta página.')
    return _wrapped_view


def owner_or_admin(model_class, owner_field='creado_por', pk_kwarg='pk'):
    """Generic ownership decorator.

    Args:
        model_class: The Django model to look up.
        owner_field: Dot-notation path to the owner attribute,
            e.g. 'creado_por' or 'curso.docente_creador'.
        pk_kwarg: The kwargs key containing the object PK.
    """
    from django.shortcuts import get_object_or_404

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request, 'user') or not request.user.is_authenticated:
                return HttpResponseForbidden('Debes iniciar sesión.')

            if request.user.rol == 'admin':
                return view_func(request, *args, **kwargs)

            pk = kwargs.get(pk_kwarg)
            if pk is None:
                return HttpResponseForbidden('No tienes permisos para acceder a esta página.')

            obj = get_object_or_404(model_class, pk=pk)

            # Resolve dot-notation owner field
            owner = obj
            for attr in owner_field.split('.'):
                owner = getattr(owner, attr, None)
                if owner is None:
                    break

            if owner == request.user:
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden('No tienes permisos para acceder a este recurso.')
        return _wrapped_view
    return decorator


def colaborador_required(view_func):
    return role_required('colaborador')(view_func)


def admin_required(view_func):
    return role_required('admin')(view_func)


def docente_or_admin_required(view_func):
    return role_required('admin', 'docente')(view_func)
