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
    # Fix heading to section-title
    content = re.sub(r'<h1 class="[^"]*text-2xl[^"]*"[^>]*>', r'<h1 class="section-title">', content)
    content = re.sub(r'<h1 class="text-2xl[^"]*"[^>]*>', r'<h1 class="section-title">', content)
    content = re.sub(r'<h1 class="text-xl[^"]*"[^>]*>', r'<h1 class="section-title">', content)
    
    # Check if section-title is used in h2
    content = re.sub(r'<h2 class="text-2xl[^"]*"[^>]*>', r'<h2 class="section-title">', content)
    content = re.sub(r'<h2 class="text-xl[^"]*"[^>]*>', r'<h2 class="section-title">', content)

    # Convert hardcoded inline styles to CSS classes from kimun.css
    content = re.sub(r'style="color:\s*var\(--color-text-secondary\);?"', 'class="text-secondary"', content)
    # If the element already has a class, combine them
    content = re.sub(r'class="([^"]*)"\s+class="text-secondary"', r'class="\1 text-secondary"', content)
    
    # Remove style="color: var(--color-text);" as it's the default
    content = re.sub(r'\s*style="color:\s*var\(--color-text\);?"', '', content)
    
    # Replace style="color: var(--color-primary);" with text-primary
    content = re.sub(r'style="color:\s*var\(--color-primary\);?"', 'class="text-primary"', content)
    content = re.sub(r'class="([^"]*)"\s+class="text-primary"', r'class="\1 text-primary"', content)

    # Check for hybrid-card wrapper
    # If it has something like <div class="bg-white ..."> we replace with <div class="hybrid-card rounded-2xl p-8 max-w-2xl mx-auto">
    # Let's do it manually if needed, but let's see how they look.
    return content

for f in files_to_fix:
    if not os.path.exists(f):
        print(f"Not found: {f}")
        continue
    with open(f, 'r') as file:
        original = file.read()
    
    modified = fix_html(original)
    
    # Save back
    with open(f, 'w') as file:
        file.write(modified)
        
    print(f"Processed: {f}")
