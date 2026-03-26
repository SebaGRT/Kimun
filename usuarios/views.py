from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


STYLE_TEMPLATES = {
    'minimal': 'registration/login_minimal.html',
    'brutal': 'registration/login_brutal.html',
    'glass': 'registration/login_glass.html',
}

DASHBOARD_TEMPLATES = {
    'minimal': ('base_minimal.html', 'inicio_minimal.html'),
    'brutal': ('base_brutal.html', 'inicio_brutal.html'),
    'glass': ('base_glass.html', 'inicio_glass.html'),
}


def login_view(request):
    style = request.GET.get('style', 'default')
    template_name = STYLE_TEMPLATES.get(style, 'registration/login.html')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if style != 'default':
                request.session['kimun_style'] = style
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, template_name, {'form': {'errors': True}})
    
    return render(request, template_name, {'form': {}})


def style_selector_view(request):
    return render(request, 'registration/style_selector.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('usuarios:login')


@login_required(login_url='usuarios:login')
def inicio(request):
    style = request.session.get('kimun_style', 'default')
    if style in DASHBOARD_TEMPLATES:
        base_template, content_template = DASHBOARD_TEMPLATES[style]
        return render(request, content_template, {'base_template': base_template})
    return render(request, 'inicio.html')


@login_required
def dashboard_admin(request):
    return render(request, 'dashboard_admin.html')


@login_required
def dashboard_docente(request):
    return render(request, 'dashboard_docente.html')


@login_required
def dashboard_colaborador(request):
    return render(request, 'dashboard_colaborador.html')