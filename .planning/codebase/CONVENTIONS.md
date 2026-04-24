# Coding Conventions

**Analysis Date:** 2026-04-24

## Language & Framework

**Primary:** Python 3.14 with Django 6.0.3
**Frontend:** Django Templates (Jinja2-like syntax), Tailwind CSS utility classes, vanilla JavaScript
**Editor:** CKEditor 5 for rich text content

## Naming Patterns

**Files:**
- Lowercase with underscores: `models.py`, `tests.py`, `decorators.py`
- App directories use lowercase Spanish nouns: `cursos/`, `evaluaciones/`, `certificados/`, `usuarios/`, `tareas/`, `anuncios/`, `calendario/`, `reportes/`

**Classes:**
- Models: PascalCase, Spanish descriptive names
  - `Curso`, `Evaluacion`, `InscripcionCurso`, `ClaseCompletado`, `IntentoEvaluacion`, `Certificado`
- Forms: PascalCase + `Form` suffix
  - `CursoForm`, `MaterialForm`, `ClaseForm`, `EvaluacionForm`
- Mixins: PascalCase + `Mixin` suffix
  - `RoleRequiredMixin`, `CourseOwnerOrAdminMixin`

**Functions & Methods:**
- Views: lowercase with underscores, Spanish action names
  - `curso_list`, `curso_create`, `curso_detail`, `tomar_evaluacion`, `clase_completar`
- Model methods: lowercase, Spanish
  - `calcular_progreso`, `get_clase_anterior`, `get_siguiente_clase`
- Decorators: lowercase with underscores
  - `role_required`, `course_owner_or_admin`, `docente_or_admin_required`

**Variables:**
- Local variables: lowercase with underscores, Spanish
  - `cursos_page`, `clases_con_estado`, `puntaje_obtenido`, `fecha_limite`
- QuerySet variables: plural nouns
  - `cursos`, `evaluaciones`, `inscripciones`

**Templates:**
- `app_name/model_action.html` pattern
  - `cursos/curso_list.html`, `cursos/curso_form.html`, `cursos/curso_detail.html`
  - `evaluaciones/evaluacion_form.html`, `evaluaciones/resultado_evaluacion.html`
- Partial templates in `partials/` subdirectory
  - `anuncios/partials/anuncio_card.html`, `calendario/partials/eventos_list.html`

**URL Names:**
- App-scoped with `app_name` variable in each `urls.py`
- Pattern: `model_action` (lowercase, underscore-separated)
  - `cursos:curso_list`, `cursos:clase_detail`, `evaluaciones:tomar_evaluacion`
  - `usuarios:mis_cursos`, `usuarios:inscribir_curso_bulk`

## Import Organization

**Standard order observed:**
1. Python stdlib
2. Django core imports
3. Third-party packages
4. Project app imports (relative `.` for same app)

**Example from `cursos/views.py`:**
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Max
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Curso, Material, InscripcionCurso, Categoria, Clase, ClaseCompletado
from .forms import CursoForm, MaterialForm, CategoriaForm, ClaseForm
from usuarios.decorators import admin_required, docente_or_admin_required, course_owner_or_admin, owner_or_admin, colaborador_required
```

**No absolute imports for cross-app references** - always use app package paths:
- `from usuarios.decorators import admin_required`
- `from cursos.models import Curso`
- `from evaluaciones.models import IntentoEvaluacion`

## Code Style

**Formatting:** No automated formatter detected (no `black`, `autopep8`, `ruff` configuration found)
**Linting:** No linter configuration detected (no `.flake8`, `.pylintrc`, `pyproject.toml`)
**Indentation:** 4 spaces (standard Python)
**Line length:** Appears to follow ~100-120 character soft limit

**Docstrings:** Minimal usage. Only complex utilities have docstrings:
- `owner_or_admin` decorator has Google-style docstring
- `CertificateEligibilityService` tests have extensive docstrings explaining business rules
- Most views and models lack docstrings

## URL & Routing Patterns

**Django app-level URLs:**
- Each app defines `app_name` for URL namespacing
- Root `kimun/urls.py` includes all app URLs with path prefixes
- Named routes use Spanish verbs and nouns

**Example from `cursos/urls.py`:**
```python
app_name = 'cursos'

urlpatterns = [
    path('', views.curso_list, name='curso_list'),
    path('crear/', views.curso_create, name='curso_create'),
    path('<int:pk>/', views.curso_detail, name='curso_detail'),
    path('<int:pk>/editar/', views.curso_edit, name='curso_edit'),
    path('<int:pk>/eliminar/', views.curso_delete, name='curso_delete'),
]
```

## Model Conventions

**Field naming:** Spanish snake_case
- `titulo`, `descripcion`, `fecha_creacion`, `fecha_limite`, `puntaje_maximo`
- `docente_creador`, `creado_por`, `calificado_por`

**Related names:** Spanish plural, descriptive
- `curso.materiales`, `curso.clases`, `curso.inscripciones`, `curso.evaluaciones`
- `usuario.inscripciones`, `usuario.clases_completadas`, `usuario.cursos_creados`

**Choices:** UPPER_SNAKE_CASE constants with Spanish human-readable labels
```python
ESTADO_CHOICES = [
    ('borrador', 'Borrador'),
    ('publicado', 'Publicado'),
]
```

**Meta options:** Always include `verbose_name` and `verbose_name_plural` in Spanish
```python
class Meta:
    verbose_name = 'Clase Completada'
    verbose_name_plural = 'Clases Completadas'
```

## View Patterns

**Function-based views (FBV) exclusively** - no class-based views detected
- All views in `views.py` are functions
- Decorators applied in order: `@login_required` outermost, then role checks

**Example pattern:**
```python
@login_required
@course_owner_or_admin
def curso_edit(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            curso = form.save()
            messages.success(request, f'Curso "{curso.titulo}" actualizado.')
            return redirect('cursos:curso_detail', pk=curso.id)
    else:
        form = CursoForm(instance=curso)
    return render(request, 'cursos/curso_form.html', {
        'accion': 'editar',
        'curso': curso,
        'form': form,
        'categorias': Categoria.objects.all()
    })
```

**Permission checking:** Three-layer approach
1. `@login_required` for authentication
2. Custom decorators (`@admin_required`, `@docente_or_admin_required`, `@course_owner_or_admin`) for authorization
3. Inline checks in views for edge cases (e.g., draft course visibility)

## Form Patterns

**ModelForms with widget configuration inline:**
- Tailwind CSS utility classes directly in widget `attrs`
- Spanish placeholder text
- Custom `clean()` methods for cross-field validation
- Conditional fields injected in `__init__` (e.g., admin-only `docente_creador` field)

**Example from `cursos/forms.py`:**
```python
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo', 'descripcion', 'categoria', 'estado', 'fecha_limite']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'input-field w-full px-4 py-3 rounded-xl text-lg',
                'placeholder': 'Ej: Primeros Auxilios'
            }),
        }
```

## Static Files

**Organization:**
```
static/
├── css/
│   ├── kimun.css      # Main stylesheet
│   └── toast.css      # Toast notification styles
├── js/
│   └── toast.js       # Toast notification JS
└── img/
    └── illustrations/ # SVG illustrations
```

**CSS Framework:** Tailwind CSS (utility classes observed in templates and form widgets)

## Template Conventions

**Base template:** `templates/base.html`
**Template inheritance:** All templates extend `base.html` or admin overrides
**Block naming:** `title`, `content`, `extra_css`, `extra_js`
**Partial templates:** Prefixed with path `partials/`, included via `{% include %}`

## Decorator & Mixin Patterns

**Custom decorators in `usuarios/decorators.py`:**
- `role_required(*roles)` - generic role checker
- `course_owner_or_admin` - checks course ownership for docentes
- `owner_or_admin(model_class, owner_field, pk_kwarg)` - generic ownership via dot-notation

**Mixins in `usuarios/mixins.py`:**
- Mirror decorator functionality for CBV (though CBVs are not used)
- `RoleRequiredMixin`, `AdminRequiredMixin`, `CourseOwnerOrAdminMixin`

## Error Handling

**User-facing errors:**
- `messages.error(request, '...')` for form/validation errors
- `HttpResponseForbidden('...')` for permission denials
- `messages.success(request, '...')` for successful actions

**No centralized error handling** - each view handles its own edge cases

## Signals

**Signal handlers in `signals.py` per app:**
- `cursos/signals.py` - progress tracking on class completion
- `calendario/signals.py` - auto-creates calendar events for courses/evaluations
- `certificados/signals.py` - auto-generates certificates when requirements met
- `usuarios/signals.py` - audit logging

**Pattern:** Disconnect signals in tests when testing service logic independently (observed in `certificados/tests.py`)

---

*Convention analysis: 2026-04-24*
