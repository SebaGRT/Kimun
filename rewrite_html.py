import re

with open("templates/cursos/curso_list.html", "r") as f:
    content = f.read()

# Regex to find the <!-- Lista de Cursos --> section up to {% if page_obj.has_other_pages %}
# We'll replace the content inside {% if cursos %} ... {% else %} (for the empty state)
# Wait, let's just do a string replacement.

part1 = """<!-- Lista de Cursos -->
{% if cursos %}
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {% for curso in cursos %}
    <div class="hybrid-card rounded-2xl p-6 group">
        <div class="flex items-start justify-between mb-4">
            <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl" 
                 style="background-color: var(--color-primary); color: white;">
                <i class="bi bi-book-fill"></i>
            </div>
            {% if curso.estado == 'borrador' %}
            <span class="px-3 py-1 rounded-full text-xs font-semibold" 
                  style="background-color: #fef3c7; color: #d97706;">
                Borrador
            </span>
            {% else %}
            <span class="px-3 py-1 rounded-full text-xs font-semibold" 
                  style="background-color: var(--color-success-bg); color: var(--color-success);">
                Público
            </span>
            {% endif %}
        </div>
        
        <h3 class="text-xl font-bold mb-2" style="color: var(--color-text);">
            {{ curso.titulo }}
        </h3>
        <p class="mb-4 line-clamp-2" style="color: var(--color-text-secondary);">
            {{ curso.descripcion }}
        </p>
        
        {% if curso.categoria %}
        <div class="mb-4">
            <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium" 
                  style="background-color: {{ curso.categoria.color }}20; color: {{ curso.categoria.color }};">
                <i class="bi bi-tag me-1"></i>{{ curso.categoria.nombre }}
            </span>
        </div>
        {% endif %}
        
        {% if curso.fecha_limite %}
        <div class="mb-4">
            {% if curso.fecha_limite < now %}
            <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium" style="background-color: #fee2e2; color: #dc2626;">
                <i class="bi bi-exclamation-triangle me-1"></i>Vencido
            </span>
            {% else %}
            <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium" style="background-color: var(--color-warning-bg); color: var(--color-warning);">
                <i class="bi bi-clock me-1"></i>{{ curso.fecha_limite|date:"d M" }}
            </span>
            {% endif %}
        </div>
        {% endif %}
        
        <div class="pt-4 border-t flex items-center justify-between" style="border-color: var(--color-border);">
            <span class="text-sm" style="color: var(--color-text-secondary);">
                <i class="bi bi-calendar me-1"></i>
                {{ curso.fecha_creacion|date:"d M Y" }}
            </span>
            <a href="{% url 'cursos:curso_detail' pk=curso.id %}" 
               class="text-sm font-medium transition-colors"
               style="color: var(--color-primary);">
                Ver más <i class="bi bi-arrow-right ms-1"></i>
            </a>
        </div>
    </div>
    {% endfor %}
</div>"""

replacement1 = """<!-- Lista de Cursos -->
{% if cursos %}

<!-- Destacado -->
<div class="mb-10 stagger-in">
    <h2 class="section-title">
        <i class="bi bi-star-fill"></i>
        Curso Destacado
    </h2>
    {% with curso=cursos.0 %}
    <div class="hybrid-card-featured p-8 group">
        <div class="flex flex-col md:flex-row gap-6 md:items-start">
            <div class="w-16 h-16 shrink-0 rounded-2xl flex items-center justify-center text-3xl shadow-sm" 
                 style="background-color: var(--color-primary); color: white;">
                <i class="bi bi-book-half"></i>
            </div>
            
            <div class="flex-1">
                <div class="flex items-center justify-between mb-3">
                    {% if curso.categoria %}
                    <span class="inline-flex items-center px-3 py-1 rounded-lg text-sm font-semibold" 
                          style="background-color: {{ curso.categoria.color }}20; color: {{ curso.categoria.color }};">
                        <i class="bi bi-tag me-1"></i>{{ curso.categoria.nombre }}
                    </span>
                    {% endif %}
                    
                    {% if curso.estado == 'borrador' %}
                    <span class="px-3 py-1 rounded-full text-sm font-bold shadow-sm" 
                          style="background-color: var(--color-warning-bg); color: var(--color-warning);">
                        Borrador
                    </span>
                    {% else %}
                    <span class="px-3 py-1 rounded-full text-sm font-bold shadow-sm" 
                          style="background-color: var(--color-success-bg); color: var(--color-success);">
                        Público
                    </span>
                    {% endif %}
                </div>
                
                <h3 class="text-3xl font-extrabold mb-3" style="color: var(--color-text);">
                    {{ curso.titulo }}
                </h3>
                <p class="mb-6 text-lg leading-relaxed line-clamp-2" style="color: var(--color-text-secondary);">
                    {{ curso.descripcion }}
                </p>
                
                <div class="flex flex-wrap items-center gap-4 pt-4 border-t" style="border-color: var(--color-border);">
                    <span class="text-sm font-medium" style="color: var(--color-text-secondary);">
                        <i class="bi bi-calendar3 me-1.5"></i>
                        {{ curso.fecha_creacion|date:"d M Y" }}
                    </span>
                    
                    {% if curso.fecha_limite %}
                    <span class="text-sm font-medium px-3 py-1.5 rounded-lg inline-flex items-center" 
                          style="{% if curso.fecha_limite < now %}background-color: var(--color-error-bg); color: var(--color-error);{% else %}background-color: var(--color-warning-bg); color: var(--color-warning);{% endif %}">
                        {% if curso.fecha_limite < now %}
                        <i class="bi bi-exclamation-triangle-fill me-1.5"></i>Vencido
                        {% else %}
                        <i class="bi bi-clock-fill me-1.5"></i>Límite: {{ curso.fecha_limite|date:"d M" }}
                        {% endif %}
                    </span>
                    {% endif %}
                    
                    <div class="ms-auto">
                        <a href="{% url 'cursos:curso_detail' pk=curso.id %}" 
                           class="inline-flex items-center px-5 py-2.5 rounded-xl font-bold transition-all hover:-translate-y-0.5 shadow-sm"
                           style="background-color: var(--color-primary); color: white;">
                            Acceder al Curso <i class="bi bi-arrow-right ms-2"></i>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endwith %}
</div>

<!-- Resto de los Cursos -->
{% if cursos|length > 1 %}
<div class="mb-6">
    <h2 class="section-title">
        <i class="bi bi-collection-fill"></i>
        Más Cursos
    </h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 stagger-in">
        {% for curso in cursos|slice:"1:" %}
        <div class="hybrid-card rounded-2xl p-6 group">
            <div class="flex items-start justify-between mb-4">
                <div class="w-12 h-12 rounded-xl flex items-center justify-center text-xl shadow-sm" 
                     style="background-color: var(--color-primary); color: white;">
                    <i class="bi bi-book-fill"></i>
                </div>
                {% if curso.estado == 'borrador' %}
                <span class="px-2.5 py-1 rounded-full text-xs font-bold" 
                      style="background-color: var(--color-warning-bg); color: var(--color-warning);">
                    Borrador
                </span>
                {% else %}
                <span class="px-2.5 py-1 rounded-full text-xs font-bold" 
                      style="background-color: var(--color-success-bg); color: var(--color-success);">
                    Público
                </span>
                {% endif %}
            </div>
            
            <h3 class="text-xl font-bold mb-2 transition-colors group-hover:text-primary" style="color: var(--color-text);">
                {{ curso.titulo }}
            </h3>
            <p class="mb-4 text-sm line-clamp-2" style="color: var(--color-text-secondary);">
                {{ curso.descripcion }}
            </p>
            
            {% if curso.categoria %}
            <div class="mb-4">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold" 
                      style="background-color: {{ curso.categoria.color }}20; color: {{ curso.categoria.color }};">
                    <i class="bi bi-tag-fill me-1.5"></i>{{ curso.categoria.nombre }}
                </span>
            </div>
            {% endif %}
            
            <div class="pt-4 border-t flex items-center justify-between mt-auto" style="border-color: var(--color-border);">
                {% if curso.fecha_limite %}
                    {% if curso.fecha_limite < now %}
                    <span class="text-xs font-semibold inline-flex items-center" style="color: var(--color-error);">
                        <i class="bi bi-exclamation-triangle-fill me-1"></i>Vencido
                    </span>
                    {% else %}
                    <span class="text-xs font-semibold inline-flex items-center" style="color: var(--color-warning);">
                        <i class="bi bi-clock-fill me-1"></i>{{ curso.fecha_limite|date:"d M" }}
                    </span>
                    {% endif %}
                {% else %}
                    <span class="text-xs font-medium" style="color: var(--color-text-secondary);">
                        <i class="bi bi-calendar3 me-1"></i>{{ curso.fecha_creacion|date:"d M Y" }}
                    </span>
                {% endif %}
                
                <a href="{% url 'cursos:curso_detail' pk=curso.id %}" 
                   class="text-sm font-bold inline-flex items-center transition-transform group-hover:translate-x-1"
                   style="color: var(--color-primary);">
                    Ver más <i class="bi bi-chevron-right ms-1"></i>
                </a>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endif %}"""

part2 = """<!-- Estado vacío -->
<div class="text-center py-16">
    <div class="w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center" 
         style="background-color: var(--color-bg);">
        <i class="bi bi-book text-4xl" style="color: var(--color-text-secondary);"></i>
    </div>
    <h3 class="text-xl font-medium mb-2" style="color: var(--color-text);">No hay cursos disponibles</h3>
    <p class="mb-6" style="color: var(--color-text-secondary);">
        {% if is_docente %}Crea el primer curso para comenzar{% else %}Próximamente habrá cursos disponibles{% endif %}
    </p>
    {% if is_docente %}
    <a href="{% url 'cursos:curso_create' %}" class="btn-primary px-5 py-2.5 rounded-xl font-medium inline-block">
        <i class="bi bi-plus-lg me-2"></i>Crear Curso
    </a>
    {% endif %}
</div>"""

replacement2 = """<!-- Estado vacío -->
<div class="empty-state stagger-in">
    <img src="{% static 'img/illustrations/empty-courses.svg' %}" alt="Sin cursos" class="w-48 h-48 mx-auto mb-6 opacity-80 animate-float">
    <h3 class="text-2xl font-bold mb-3" style="color: var(--color-text);">No hay cursos disponibles</h3>
    <p class="mb-8 max-w-md mx-auto text-lg" style="color: var(--color-text-secondary);">
        {% if is_docente %}Crea el primer curso interactivo para que tus estudiantes puedan comenzar a aprender.{% else %}Próximamente habrá nuevos e increíbles cursos disponibles para ti.{% endif %}
    </p>
    {% if is_docente %}
    <a href="{% url 'cursos:curso_create' %}" class="btn-primary px-6 py-3 rounded-xl font-bold inline-flex items-center shadow-md transition-transform hover:-translate-y-1">
        <i class="bi bi-plus-lg me-2 text-xl"></i> Crear tu primer curso
    </a>
    {% endif %}
</div>"""

content = content.replace(part1, replacement1)
content = content.replace(part2, replacement2)

with open("templates/cursos/curso_list.html", "w") as f:
    f.write(content)

