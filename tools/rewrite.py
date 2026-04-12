import re

with open('templates/inicio.html', 'r') as f:
    content = f.read()

new_content = """{% extends 'base.html' %}

{% block title %}Inicio - Kimün{% endblock %}

{% block content %}
<!-- Hero Section -->
<div class="hero-section mb-8 p-8 md:p-12">
    <div class="flex flex-col md:flex-row items-center gap-8">
        <div class="flex-1 text-center md:text-left">
            <h1 class="text-3xl md:text-4xl font-bold mb-4" style="color: white;">
                Bienvenido a Kimün, {{ user.get_full_name|default:user.username }}
            </h1>
            <p class="text-lg mb-6 opacity-90" style="color: white;">
                Plataforma de capacitación para el cuidado de personas mayores
            </p>
            <a href="{% url 'cursos:curso_list' %}" class="inline-block px-6 py-3 rounded-xl font-semibold transition-transform hover:-translate-y-1" style="background: var(--color-surface); color: var(--color-primary);">
                Ver Cursos
            </a>
        </div>
        <div class="flex-1 flex justify-center">
            <img src="{% static 'img/illustrations/hero-learning.svg' %}" alt="Aprendiendo" class="w-64 h-64 animate-float">
        </div>
    </div>
</div>

<!-- Quick Actions -->
<div class="hybrid-card p-6 mb-8 fade-in">
    <h3 class="text-lg font-bold mb-4" style="color: var(--color-text);">Acciones Rápidas</h3>
    <div class="flex flex-wrap gap-3">
        {% if user.rol == 'admin' %}
        <a href="{% url 'usuarios:usuario_list' %}" class="btn-subtle px-4 py-2 rounded-lg text-sm font-medium">
            <i class="bi bi-person-plus me-2"></i>Nuevo Usuario
        </a>
        <a href="{% url 'cursos:curso_create' %}" class="btn-subtle px-4 py-2 rounded-lg text-sm font-medium">
            <i class="bi bi-plus-circle me-2"></i>Crear Curso
        </a>
        <a href="{% url 'reportes:dashboard_reportes' %}" class="btn-subtle px-4 py-2 rounded-lg text-sm font-medium">
            <i class="bi bi-file-earmark-bar-graph me-2"></i>Ver Reportes
        </a>
        {% elif user.rol == 'docente' %}
        <a href="{% url 'cursos:curso_create' %}" class="btn-subtle px-4 py-2 rounded-lg text-sm font-medium">
            <i class="bi bi-plus-circle me-2"></i>Crear Curso
        </a>
        <a href="{% url 'usuarios:mis_cursos' %}" class="btn-subtle px-4 py-2 rounded-lg text-sm font-medium">
            <i class="bi bi-journal-text me-2"></i>Mis Capacitaciones
        </a>
        {% else %}
        <a href="{% url 'usuarios:mis_cursos' %}" class="btn-subtle px-4 py-2 rounded-lg text-sm font-medium">
            <i class="bi bi-journal-text me-2"></i>Mis Capacitaciones
        </a>
        <a href="{% url 'certificados:mis_certificados' %}" class="btn-subtle px-4 py-2 rounded-lg text-sm font-medium">
            <i class="bi bi-award me-2"></i>Mis Certificados
        </a>
        {% endif %}
    </div>
</div>

<!-- Stats Row (Asymmetric) -->
<div class="grid grid-cols-2 md:grid-cols-12 gap-4 mb-8">
    {% if user.rol == 'admin' %}
    <!-- Large stat cards -->
    <a href="{% url 'usuarios:usuario_list' %}" class="col-span-2 md:col-span-5 hybrid-card-featured p-6 group block fade-in">
        <div class="flex items-start justify-between mb-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-xl" style="background-color: var(--color-primary); color: white;">
                <i class="bi bi-people-fill"></i>
            </div>
            <span class="px-3 py-1 rounded-full text-xs font-bold" style="background-color: var(--color-primary); color: white;">{{ total_usuarios }}</span>
        </div>
        <h3 class="text-lg font-bold mb-1" style="color: var(--color-text);">Usuarios</h3>
        <p class="text-sm" style="color: var(--color-text-secondary);">Gestión de personal y roles</p>
    </a>
    
    <a href="{% url 'reportes:dashboard_reportes' %}" class="col-span-2 md:col-span-5 hybrid-card-featured p-6 group block fade-in" style="border-inline-start-color: var(--color-success);">
        <div class="flex items-start justify-between mb-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-xl" style="background-color: var(--color-success-bg); color: var(--color-success);">
                <i class="bi bi-bar-chart-fill"></i>
            </div>
            <span class="px-3 py-1 rounded-full text-xs font-bold" style="background-color: var(--color-success-bg); color: var(--color-success);">{{ total_inscripciones }}</span>
        </div>
        <h3 class="text-lg font-bold mb-1" style="color: var(--color-text);">Inscripciones</h3>
        <p class="text-sm" style="color: var(--color-text-secondary);">Reportes de cumplimiento</p>
    </a>

    <!-- Small stat cards -->
    <div class="col-span-1 md:col-span-2 flex flex-col gap-4">
        <a href="{% url 'cursos:curso_list' %}" class="flex-1 hybrid-card-stat p-4 flex flex-col justify-center items-center group fade-in">
            <i class="bi bi-book-fill text-xl mb-1" style="color: var(--color-warning);"></i>
            <span class="text-xl font-bold" style="color: var(--color-text);">{{ total_cursos }}</span>
        </a>
        <a href="{% url 'certificados:certificado_list' %}" class="flex-1 hybrid-card-stat p-4 flex flex-col justify-center items-center group fade-in">
            <i class="bi bi-award-fill text-xl mb-1" style="color: var(--color-purple);"></i>
            <span class="text-xl font-bold" style="color: var(--color-text);">{{ total_certificados }}</span>
        </a>
    </div>

    {% elif user.rol == 'docente' %}
    <!-- Large stat cards -->
    <a href="{% url 'cursos:curso_list' %}" class="col-span-2 md:col-span-5 hybrid-card-featured p-6 group block fade-in" style="border-inline-start-color: var(--color-warning);">
        <div class="flex items-start justify-between mb-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-xl" style="background-color: var(--color-warning-bg); color: var(--color-warning);">
                <i class="bi bi-book-fill"></i>
            </div>
            <span class="px-3 py-1 rounded-full text-xs font-bold" style="background-color: var(--color-warning-bg); color: var(--color-warning);">{{ mis_cursos_count|default:0 }}</span>
        </div>
        <h3 class="text-lg font-bold mb-1" style="color: var(--color-text);">Mis Cursos</h3>
        <p class="text-sm" style="color: var(--color-text-secondary);">Cursos que impartes</p>
    </a>
    
    <a href="{% url 'usuarios:mis_cursos' %}" class="col-span-2 md:col-span-5 hybrid-card-featured p-6 group block fade-in" style="border-inline-start-color: var(--color-pink);">
        <div class="flex items-start justify-between mb-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-xl" style="background-color: var(--color-pink-bg); color: var(--color-pink);">
                <i class="bi bi-mortarboard-fill"></i>
            </div>
            <span class="px-3 py-1 rounded-full text-xs font-bold" style="background-color: var(--color-pink-bg); color: var(--color-pink);">{{ mis_inscripciones|length|default:0 }}</span>
        </div>
        <h3 class="text-lg font-bold mb-1" style="color: var(--color-text);">Mis Capacitaciones</h3>
        <p class="text-sm" style="color: var(--color-text-secondary);">Cursos en los que participas</p>
    </a>

    <!-- Small stat cards -->
    <div class="col-span-2 md:col-span-2 flex flex-col gap-4">
        <a href="{% url 'certificados:mis_certificados' %}" class="flex-1 hybrid-card-stat p-4 flex flex-col justify-center items-center group fade-in">
            <i class="bi bi-award-fill text-xl mb-1" style="color: var(--color-purple);"></i>
            <span class="text-xl font-bold" style="color: var(--color-text);">{{ mis_certificados_count|default:0 }}</span>
        </a>
    </div>

    {% else %}
    <!-- Colaborador -->
    <a href="{% url 'usuarios:mis_cursos' %}" class="col-span-2 md:col-span-5 hybrid-card-featured p-6 group block fade-in" style="border-inline-start-color: var(--color-pink);">
        <div class="flex items-start justify-between mb-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-xl" style="background-color: var(--color-pink-bg); color: var(--color-pink);">
                <i class="bi bi-mortarboard-fill"></i>
            </div>
            <span class="px-3 py-1 rounded-full text-xs font-bold" style="background-color: var(--color-pink-bg); color: var(--color-pink);">{{ mis_inscripciones|length|default:0 }}</span>
        </div>
        <h3 class="text-lg font-bold mb-1" style="color: var(--color-text);">Mis Capacitaciones</h3>
        <p class="text-sm" style="color: var(--color-text-secondary);">Cursos asignados y en progreso</p>
    </a>

    <a href="{% url 'certificados:mis_certificados' %}" class="col-span-2 md:col-span-5 hybrid-card-featured p-6 group block fade-in" style="border-inline-start-color: var(--color-purple);">
        <div class="flex items-start justify-between mb-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-xl" style="background-color: var(--color-purple-bg); color: var(--color-purple);">
                <i class="bi bi-award-fill"></i>
            </div>
            <span class="px-3 py-1 rounded-full text-xs font-bold" style="background-color: var(--color-purple-bg); color: var(--color-purple);">{{ mis_certificados_count|default:0 }}</span>
        </div>
        <h3 class="text-lg font-bold mb-1" style="color: var(--color-text);">Mis Certificados</h3>
        <p class="text-sm" style="color: var(--color-text-secondary);">Diplomas obtenidos</p>
    </a>
    
    <!-- Empty space for the rest of the grid -->
    <div class="col-span-2 md:col-span-2"></div>
    {% endif %}
</div>

<!-- Deadline Warnings -->
{% if cursos_cercanos %}
<div class="mb-8 fade-in">
    {% for curso in cursos_cercanos %}
    <div class="flex items-center gap-4 p-4 rounded-xl mb-3 {% if curso.vencido %}bg-red-50 dark:bg-red-900/20{% else %}bg-yellow-50 dark:bg-yellow-900/20{% endif %}">
        <div class="w-10 h-10 rounded-full flex items-center justify-center {% if curso.vencido %}bg-red-100 dark:bg-red-900{% else %}bg-yellow-100 dark:bg-yellow-900{% endif %}">
            <i class="bi bi-{% if curso.vencido %}exclamation-triangle{% else %}clock{% endif %} {% if curso.vencido %}text-red-600{% else %}text-yellow-600{% endif %}"></i>
        </div>
        <div class="flex-1">
            <p class="font-medium {% if curso.vencido %}text-red-700 dark:text-red-300{% else %}text-yellow-700 dark:text-yellow-300{% endif %}">
                {% if curso.vencido %}
                El curso "{{ curso.titulo }}" ha vencido
                {% else %}
                "{{ curso.titulo }}" vence en {{ curso.dias }} día{{ curso.dias|pluralize }}
                {% endif %}
            </p>
            <p class="text-sm {% if curso.vencido %}text-red-500{% else %}text-yellow-600{% endif %}">
                Fecha límite: {{ curso.fecha_limite|date:"d M Y" }}
            </p>
        </div>
        <a href="{% url 'usuarios:mis_cursos' %}" class="btn-outline px-3 py-1.5 rounded-lg text-sm">
            Ver curso
        </a>
    </div>
    {% endfor %}
</div>
{% endif %}

<!-- Featured Courses Section -->
<div class="mb-8">
    <h2 class="section-title"><i class="bi bi-book"></i> Cursos Destacados / Actividad</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 stagger-in">
        {% if user.rol == 'colaborador' or user.rol == 'docente' %}
            {% if mis_inscripciones %}
                {% for inscripcion in mis_inscripciones|slice:":3" %}
                <div class="surface-panel surface-panel--padded group cursor-pointer hover:shadow-md transition-all" onclick="window.location='{% url 'cursos:curso_detail' pk=inscripcion.curso.id %}'">
                    <div class="flex justify-between items-start mb-3">
                        <div class="w-10 h-10 rounded-full flex items-center justify-center text-lg" 
                             style="background-color: {% if inscripcion.estado == 'completado' %}var(--color-success-bg){% elif inscripcion.estado == 'en_progreso' %}var(--color-warning-bg){% else %}var(--color-info-bg){% endif %}; 
                                    color: {% if inscripcion.estado == 'completado' %}var(--color-success){% elif inscripcion.estado == 'en_progreso' %}var(--color-warning){% else %}var(--color-info){% endif %};">
                            <i class="bi bi-{% if inscripcion.estado == 'completado' %}check-lg{% elif inscripcion.estado == 'en_progreso' %}play-circle{% else %}clock{% endif %}"></i>
                        </div>
                        <span class="badge badge-{% if inscripcion.estado == 'completado' %}success{% elif inscripcion.estado == 'en_progreso' %}warning{% else %}info{% endif %}">
                            {% if inscripcion.estado == 'completado' %}Completado{% elif inscripcion.estado == 'en_progreso' %}En progreso{% else %}Asignado{% endif %}
                        </span>
                    </div>
                    <h4 class="font-bold mb-1" style="color: var(--color-text);">{{ inscripcion.curso.titulo }}</h4>
                    <p class="text-sm mb-4" style="color: var(--color-text-secondary);">Asignado: {{ inscripcion.fecha_asignacion|date:"d M Y" }}</p>
                    <div class="flex items-center text-sm font-medium" style="color: var(--color-primary);">
                        Continuar <i class="bi bi-arrow-right ms-1 group-hover:translate-x-1 transition-transform"></i>
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div class="col-span-1 md:col-span-3 empty-state surface-panel">
                    <i class="bi bi-inbox text-4xl mb-3 inline-block" style="color: var(--color-text-secondary);"></i>
                    <p style="color: var(--color-text-secondary);">No tienes capacitaciones asignadas aún.</p>
                </div>
            {% endif %}
        {% elif user.rol == 'admin' %}
            {% if ultimas_inscripciones %}
                {% for inscripcion in ultimas_inscripciones|slice:":3" %}
                <div class="surface-panel surface-panel--padded group cursor-pointer hover:shadow-md transition-all" onclick="window.location='{% url 'reportes:reporte_usuario' inscripcion.usuario.id %}'">
                    <div class="flex justify-between items-start mb-3">
                        <div class="w-10 h-10 rounded-full flex items-center justify-center text-lg" 
                             style="background-color: {% if inscripcion.estado == 'completado' %}var(--color-success-bg){% elif inscripcion.estado == 'en_progreso' %}var(--color-warning-bg){% else %}var(--color-info-bg){% endif %}; 
                                    color: {% if inscripcion.estado == 'completado' %}var(--color-success){% elif inscripcion.estado == 'en_progreso' %}var(--color-warning){% else %}var(--color-info){% endif %};">
                            <i class="bi bi-{% if inscripcion.estado == 'completado' %}check-lg{% elif inscripcion.estado == 'en_progreso' %}play-circle{% else %}person-plus{% endif %}"></i>
                        </div>
                        <span class="badge badge-{% if inscripcion.estado == 'completado' %}success{% elif inscripcion.estado == 'en_progreso' %}warning{% else %}info{% endif %}">
                            {% if inscripcion.estado == 'completado' %}Completado{% elif inscripcion.estado == 'en_progreso' %}En progreso{% else %}Asignado{% endif %}
                        </span>
                    </div>
                    <h4 class="font-bold mb-1" style="color: var(--color-text);">{{ inscripcion.usuario.get_full_name|default:inscripcion.usuario.username }}</h4>
                    <p class="text-sm mb-1" style="color: var(--color-text-secondary);">{{ inscripcion.curso.titulo }}</p>
                    <p class="text-xs mb-4 opacity-70" style="color: var(--color-text-secondary);">{{ inscripcion.fecha_asignacion|date:"d M Y" }}</p>
                    <div class="flex items-center text-sm font-medium" style="color: var(--color-primary);">
                        Ver detalle <i class="bi bi-arrow-right ms-1 group-hover:translate-x-1 transition-transform"></i>
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div class="col-span-1 md:col-span-3 empty-state surface-panel">
                    <i class="bi bi-inbox text-4xl mb-3 inline-block" style="color: var(--color-text-secondary);"></i>
                    <p style="color: var(--color-text-secondary);">No hay inscripciones recientes.</p>
                </div>
            {% endif %}
        {% endif %}
    </div>
</div>

{% endblock %}
"""

with open('templates/inicio.html', 'w') as f:
    f.write(new_content)
