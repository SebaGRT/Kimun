import re
import os

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
    # Find all class="..." and replace mb-4 and mb-8 with mb-6 ONLY if it's a wrapper for fields.
    # To be safe, just replace all mb-8 and mb-4 inside class="..." with mb-6 
    # EXCEPT for the nav mb-4 or general layout ones.
    
    # We will do targeted replace on specific known lines that still have mb-8
    content = content.replace('gap-6 mb-8"', 'gap-6 mb-6"')
    content = content.replace('mb-8 flex', 'mb-6 flex')
    
    # Check if there's any mb-8 left:
    content = re.sub(r'class="mb-8"', 'class="mb-6"', content)
    
    # Check mb-4
    # Wait, the nav has 'class="text-sm mb-4 text-secondary"'. We probably shouldn't change nav.
    # We only change field wrappers.
    return content

for f in files_to_fix:
    if not os.path.exists(f):
        continue
    with open(f, 'r') as file:
        content = file.read()
    
    content = fix_html(content)
    
    with open(f, 'w') as file:
        file.write(content)
