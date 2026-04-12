import os
import re

files_to_fix = [
    'templates/cursos/curso_form.html',
    'templates/cursos/material_form.html',
    'templates/cursos/clase_form.html',
    'templates/cursos/categoria_form.html',
    'templates/evaluaciones/evaluacion_form.html',
    'templates/tareas/tarea_form.html',
    'templates/tareas/entrega_form.html',
    'templates/anuncios/anuncio_form.html',
    'templates/calendario/evento_form.html'
]

def fix_html(content):
    # Replace mb-8 and mb-4 in field wrappers to mb-6 for consistent spacing between form fields
    # Look for div class="mb-4" or div class="mb-8"
    content = re.sub(r'<div class="mb-8([^"]*)">', r'<div class="mb-6\1">', content)
    content = re.sub(r'<div class="mb-4([^"]*)">', r'<div class="mb-6\1">', content)
    # What about padding or spaces? 
    # Just to be safe, any class matching mb-4 or mb-8 in a form container could be changed
    # to mb-6. However, let's keep mb-6 for fields.
    
    # ensure "section-title" has no extra classes like "mb-4" or "text-2xl font-bold"
    # because section-title has its own styling.
    content = re.sub(r'class="text-2xl font-bold section-title"', 'class="section-title"', content)
    
    return content

for f in files_to_fix:
    if not os.path.exists(f):
        continue
    with open(f, 'r') as file:
        original = file.read()
    
    modified = fix_html(original)
    
    with open(f, 'w') as file:
        file.write(modified)

