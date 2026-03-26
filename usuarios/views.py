from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('usuarios:login')


@login_required(login_url='usuarios:login')
def inicio(request):
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