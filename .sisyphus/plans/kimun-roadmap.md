# Kimün Training Platform - Feature Roadmap

> Generated: 2026-04-11 | Stack: Django 6.0 + TailwindCSS + Alpine.js + HTMX + WeasyPrint
> Test baseline: 197 passing, 0 skipped (exam flow FIXED) | DB: SQLite (dev) / PostgreSQL (prod)

---

## Priority 0: Critical Bug Fixes (Complete First)

*Must fix before any new features. The exam-taking flow is completely broken.*

### 0.1 Fix UnboundLocalError in `tomar_evaluacion`

- [x] Remove duplicate inner import at `evaluaciones/views.py:237` (`from cursos.models import InscripcionCurso`)
- [x] Verify `InscripcionCurso` is already imported at module level (line 9 area) — if not, add it there
- [x] Unskip the 3 tests in `evaluaciones/tests.py:313-323` (`test_tomar_evaluacion_requires_inscripcion`, `test_tomar_evaluacion_post_aprobado`, `test_tomar_evaluacion_post_reprobado`)
- [x] Write new test: `test_tomar_evaluacion_creates_intento_on_pass`
- [x] Write new test: `test_tomar_evaluacion_marks_inscripcion_completado_when_all_evals_passed`

**Files to modify:**
- `evaluaciones/views.py` — remove line 237 inner import
- `evaluaciones/tests.py` — unskip tests, add new ones

**Acceptance Criteria:** All 3 previously-skipped tests pass + new tests pass. `tomar_evaluacion` POST completes without `UnboundLocalError`.

**Effort:** S (half a day)

---

### 0.2 Fix `resultado_evaluacion.html` to use attempt data

- [x] In `resultado_evaluacion` view (line 265-277), pass `respuestas_detalle` in context: a dict mapping `pregunta.pk → alternativa.pk` derived from the `IntentoEvaluacion` or stored alongside it
- [x] **Design decision needed**: Currently `IntentoEvaluacion` does NOT store which alternatives were selected — only the final score and pass/fail. Two options:
  - **Option A (Recommended)**: Add `respuestas` `JSONField` to `IntentoEvaluacion` model, populated during `tomar_evaluacion` POST. This persists answer data for result display and future analytics.
  - **Option B**: Store answers in a new `Respuesta` model (more normalized, more queries).
- [x] If Option A: Add `respuestas = models.JSONField(default=dict, blank=True)` to `IntentoEvaluacion`, create & run migration, update `tomar_evaluacion` to save `respuestas` dict when creating `IntentoEvaluacion`
- [x] Rewrite template `resultado_evaluacion.html` lines 73-111: replace `request.POST.respuestas` with `intento.respuestas` context variable
- [x] Fix typo on line 33: change `"No aprobbaste"` → `"No aprobaste"`
- [x] Add test: `test_resultado_evaluacion_shows_answer_summary`
- [x] Add test: `test_resultado_evaluacion_shows_correct_alternatives`

**Files to modify:**
- `evaluaciones/models.py` — add `respuestas` JSONField to `IntentoEvaluacion`
- `evaluaciones/views.py` — save respuestas in `tomar_evaluacion`, pass in context to `resultado_evaluacion`
- `templates/evaluaciones/resultado_evaluacion.html` — use `intento.respuestas` instead of `request.POST`
- `evaluaciones/tests.py` — add result display tests

**Acceptance Criteria:** Result page shows which questions the user got right/wrong with correct/incorrect highlighting. No empty result summary.

**Effort:** M (2-3 days with migration + template rewrite)

---

### 0.3 Decide on HTMX endpoint: wire or remove

- [x] **Decision**: The `responder_pregunta_htmx` endpoint (views.py:280-293) is dead code — no template calls it, and it expects JSON body which HTMX doesn't send by default
- [x] **Recommended action**: Remove the endpoint entirely for now. It can be re-added properly in P3 (Assessment Enhancements) if real-time per-question feedback is desired
- [x] Remove URL pattern from `evaluaciones/urls.py:13`
- [x] Remove the view function from `evaluaciones/views.py:280-293`
- [x] Remove unused `json` import if no longer needed elsewhere in views.py
- [x] Add test: verify `responder_pregunta_htmx` URL returns 404 (confirms removal)

**Files to modify:**
- `evaluaciones/views.py` — remove function
- `evaluaciones/urls.py` — remove URL pattern

**Acceptance Criteria:** Dead endpoint removed. All existing tests still pass. URL returns 404.

**Effort:** S (1 hour)

---

### P0 Commit Strategy

| Commit | Description | Files |
|--------|-------------|-------|
| `fix: remove duplicate InscripcionCurso import causing UnboundLocalError` | `evaluaciones/views.py` | 
| `test: unskip tomar_evaluacion tests` | `evaluaciones/tests.py` |
| `feat: store respuestas in IntentoEvaluacion for result display` | `evaluaciones/models.py`, migration, `evaluaciones/views.py` |
| `fix: use intento.respuestas in result template, fix typo` | `templates/evaluaciones/resultado_evaluacion.html` |
| `test: add result display tests` | `evaluaciones/tests.py` |
| `refactor: remove unused responder_pregunta_htmx endpoint` | `evaluaciones/views.py`, `evaluaciones/urls.py` |

---

## Priority 1: Calendar System (Custom Build)

### 1.1 Calendar — Model & Migrations

- [x] Create `calendario/` app: `python manage.py startapp calendario`
- [x] Add `'calendario'` to `INSTALLED_APPS` in `kimun/settings.py`
- [x] Create `EventoCalendario` model:
  ```python
  class TipoEvento(models.TextChoices):
      CLASE_DEADLINE = 'clase_deadline', 'Plazo de Clase'
      EVALUACION_DEADLINE = 'evaluacion_deadline', 'Plazo de Evaluación'
      CURSO_START = 'curso_start', 'Inicio de Curso'
      CURSO_END = 'curso_end', 'Fin de Curso'
      EVENTO_GENERAL = 'evento_general', 'Evento General'

  class EventoCalendario(models.Model):
      titulo = models.CharField(max_length=200)
      descripcion = models.TextField(blank=True, default='')
      tipo = models.CharField(max_length=25, choices=TipoEvento.choices, default=TipoEvento.EVENTO_GENERAL)
      fecha_inicio = models.DateTimeField()
      fecha_fin = models.DateTimeField()
      curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE, null=True, blank=True, related_name='eventos_calendario')
      evaluacion = models.ForeignKey('evaluaciones.Evaluacion', on_delete=models.CASCADE, null=True, blank=True, related_name='eventos_calendario')
      creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='eventos_creados')
      color = models.CharField(max_length=7, default='#6366f1', help_text='Color hex, ej: #6366f1')
      
      class Meta:
          verbose_name = 'Evento de Calendario'
          verbose_name_plural = 'Eventos de Calendario'
          ordering = ['fecha_inicio']
      
      def __str__(self):
          return f"{self.titulo} ({self.get_tipo_display()})"
  ```
- [x] Run `makemigrations calendario` and `migrate`
- [x] Write model tests in `calendario/tests.py`: creation, `__str__`, default color, ordering

**Files to create:**
- `calendario/__init__.py`, `calendario/models.py`, `calendario/apps.py`, `calendario/admin.py`

**Files to modify:**
- `kimun/settings.py` — add to `INSTALLED_APPS`

**Dependencies:** P0 complete

**Acceptance Criteria:** Model created, migration runs, model tests pass.

**Effort:** S (1 day)

---

### 1.2 Calendar — Auto-Generation Sync

- [x] Create `calendario/signals.py` with signal handlers:
  - `post_save` on `Curso` → auto-create `curso_start` and `curso_end` events from `fecha_limite`
  - `post_save` on `Evaluacion` → auto-create `evaluacion_deadline` event
  - `post_save` on `Clase` → optionally create `clase_deadline` event (if Clase gets a deadline field in future)
- [x] Register signals in `calendario/apps.py` `ready()` method
- [x] Write signal tests: creating a Curso creates 1-2 calendar events; updating Curso.fecha_limite updates the event
- [x] Create management command `generar_eventos_calendario` to backfill events from existing Curso/Evaluacion data
- [x] Add `calendario/apps.py` with `CalendarioConfig`

**Files to create:**
- `calendario/signals.py`
- `calendario/management/commands/generar_eventos_calendario.py`

**Files to modify:**
- `calendario/apps.py`

**Dependencies:** P1.1

**Acceptance Criteria:** Creating/updating Curso or Evaluacion auto-creates/updates EventoCalendario records. Backfill command creates events from all existing data.

**Effort:** M (2-3 days)

---

### 1.3 Calendar — Views & URL Routing

- [x] Create `calendario/views.py` with function-based views:
  - `calendario_view(request)` — main calendar page (month view default)
  - `calendario_eventos(request)` — HTMX partial: returns event list for a date range (JSON or HTML partial)
  - `evento_create(request)` — create manual event (admin/docente only)
  - `evento_edit(request, pk)` — edit event (admin/docente only)
  - `evento_delete(request, pk)` — delete event (admin/docente only)
  - `calendario_ical_export(request)` — iCal export of user's events
- [x] Create `calendario/urls.py` with `app_name = 'calendario'`:
  ```
  path('', calendario_view, name='calendario'),
  path('eventos/', calendario_eventos, name='calendario_eventos'),
  path('evento/crear/', evento_create, name='evento_create'),
  path('evento/<int:pk>/editar/', evento_edit, name='evento_edit'),
  path('evento/<int:pk>/eliminar/', evento_delete, name='evento_delete'),
  path('exportar.ics', calendario_ical_export, name='calendario_ical_export'),
  ```
- [x] Include `calendario.urls` in `kimun/urls.py` at `path('calendario/', ...)`
- [x] Apply RBAC decorators: `@login_required` on all views, `@docente_or_admin_required` on create/edit/delete

**Files to create:**
- `calendario/views.py`, `calendario/urls.py`

**Files to modify:**
- `kimun/urls.py` — include calendario URLs

**Dependencies:** P1.1

**Acceptance Criteria:** URL routing works, RBAC enforced, 403 for colaborador on create/edit/delete.

**Effort:** M (2-3 days)

---

### 1.4 Calendar — Forms

- [x] Create `calendario/forms.py` with:
  - `EventoCalendarioForm(ModelForm)` — titulo, descripcion, tipo, fecha_inicio, fecha_fin, curso (optional), color
  - Widget attrs: `input-field` class, datetime-local for date fields
  - Validation: `fecha_fin >= fecha_inicio`
  - `clean()` method per existing form patterns
- [x] Write form tests: valid data, invalid date range, required fields

**Files to create:**
- `calendario/forms.py`

**Dependencies:** P1.1

**Acceptance Criteria:** Form validates correctly, follows existing `input-field` pattern.

**Effort:** S (1 day)

---

### 1.5 Calendar — Templates (Month/Week/Day Views)

- [x] Create `templates/calendario/base_calendario.html` extending `base.html`
- [x] Create `templates/calendario/calendario.html` — month grid view:
  - Calendar grid using HTML table / CSS Grid
  - Alpine.js `x-data` for month navigation state
  - HTMX `hx-get` to `calendario:eventos` for partial month updates
  - Color-coded event badges by `tipo` (matching `Curso.categoria.color` pattern)
  - Filter sidebar: filter by course, event type
- [x] Create `templates/calendario/partials/evento_badge.html` — reusable event badge partial
- [x] Create `templates/calendario/partials/dia_celda.html` — day cell partial for HTMX swap
- [x] Create `templates/calendario/evento_form.html` — create/edit event form
- [x] Create `templates/calendario/evento_confirm_delete.html` — delete confirmation
- [x] Add "Calendario" link to `templates/base.html` navbar
- [x] All user-facing text in Spanish

**Files to create:**
- `templates/calendario/calendario.html`
- `templates/calendario/partials/evento_badge.html`
- `templates/calendario/partials/dia_celda.html`
- `templates/calendario/evento_form.html`
- `templates/calendario/evento_confirm_delete.html`

**Files to modify:**
- `templates/base.html` — add nav link

**Dependencies:** P1.3, P1.4

**Acceptance Criteria:** Calendar renders with month view. HTMX navigation works. Events color-coded by type. Filters work. Mobile-responsive (Tailwind grid).

**Effort:** M (3-4 days)

---

## Priority 3: Assessment Enhancements (COMPLETE)

### 3.1 Attempt Limits

- [x] Add `max_intentos` field to `Evaluacion` model
- [x] Add `max_intentos` to `EvaluacionForm` and views
- [x] In `tomar_evaluacion` view: check attempt count before allowing new attempt
- [x] Display attempt count and limit on evaluation detail/list page

### 3.2 Timer Support

- [x] Add `duracion_minutos` field to `Evaluacion`
- [x] Add `hora_inicio` field to `IntentoEvaluacion`
- [x] In `tomar_evaluacion` view: set `hora_inicio` in GET, check elapsed time in POST
- [x] In `tomar_evaluacion.html`: Alpine.js countdown timer with auto-submit

### 3.3 Question Banks (Banco de Preguntas)

- [x] Add `BancoPreguntas` model
- [x] Add `banco` FK from `Pregunta`
- [x] Add `preguntas_por_intento` to `Evaluacion`
- [x] Create bank management views (list, create, edit, delete, detail)
- [x] Update `tomar_evaluacion` to randomly select N questions when configured

### 3.4 Assessment — Tests

- [x] Existing tests cover new functionality

**Effort:** M (3-4 days)

### 3.1 Attempt Limits

- [x] Add `max_intentos` field to `Evaluacion` model: `models.IntegerField(default=0, help_text='0 = sin límite')`
- [x] Add `max_intentos` to `EvaluacionForm` and `evaluacion_create/edit` views
- [x] In `tomar_evaluacion` view: check `IntentoEvaluacion.objects.filter(usuario=request.user, evaluacion=evaluacion).count() >= evaluacion.max_intentos` before allowing a new attempt (skip if max_intentos=0)
- [x] Display attempt count and limit on evaluation detail/list page
- [x] Add migration, form test, view test

**Files to modify:**
- `evaluaciones/models.py`
- `evaluaciones/forms.py`
- `evaluaciones/views.py`
- `templates/evaluaciones/evaluacion_form.html`, `evaluacion_list.html`

**Dependencies:** P0 complete

**Acceptance Criteria:** When max_intentos > 0, users exceeding the limit see a clear message. Unlimited attempts work with max_intentos=0.

**Effort:** S (1-2 days)

---

### 3.2 Timer Support

- [x] Add `duracion_minutos` field to `Evaluacion`: `models.IntegerField(null=True, blank=True, help_text='Minutos, vacío = sin límite')`
- [x] Add field to `EvaluacionForm`
- [x] In `tomar_evaluacion.html`: if `evaluacion.duracion_minutos`, add Alpine.js countdown timer:
  - `x-data="{ timeLeft: {{ evaluacion.duracion_minutos }} * 60 }"`
  - `x-init="setInterval(() => { timeLeft--; if(timeLeft <= 0) document.getElementById('eval-form').submit() }, 1000)"`
  - Display remaining time visually
- [x] Add `hora_inicio` field to `IntentoEvaluacion`: `models.DateTimeField(null=True, blank=True)`
- [x] Set `hora_inicio` in `tomar_evaluacion` GET, check elapsed time in POST
- [x] Write tests: timer display, auto-submit on timeout

**Files to modify:**
- `evaluaciones/models.py`, `forms.py`, `views.py`
- `templates/evaluaciones/tomar_evaluacion.html`

**Dependencies:** P0 complete

**Acceptance Criteria:** Timed evaluations show a visible countdown. Form auto-submits when timer expires. Server-side validation rejects late submissions.

**Effort:** M (2-3 days)

---

### 3.3 Question Banks (Banco de Preguntas)

- [x] Add `BancoPreguntas` model to `evaluaciones/models.py`:
  ```python
  class BancoPreguntas(models.Model):
      nombre = models.CharField(max_length=200)
      descripcion = models.TextField(blank=True, default='')
      curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE, null=True, blank=True, related_name='bancos_preguntas')
      creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bancos_creados')
      es_publico = models.BooleanField(default=False)
      fecha_creacion = models.DateTimeField(auto_now_add=True)
      
      class Meta:
          verbose_name = 'Banco de Preguntas'
          verbose_name_plural = 'Bancos de Preguntas'
  ```
- [x] Add FK from `Pregunta` to `BancoPreguntas`: `banco = models.ForeignKey(BancoPreguntas, on_delete=models.SET_NULL, null=True, blank=True, related_name='preguntas')`
- [x] Add field to `Evaluacion`: `preguntas_por_intento = models.IntegerField(null=True, blank=True, help_text='Aleatorizar N preguntas del banco')`
- [x] Create views for bank management: `banco_list`, `banco_create`, `banco_detail`, `banco_add_preguntas`
- [x] Update `tomar_evaluacion`: if `evaluacion.preguntas_por_intentos` is set, randomly select N questions from linked banks
- [x] Create templates for bank CRUD
- [x] Write tests

**Files to modify:**
- `evaluaciones/models.py`, `forms.py`, `views.py`, `urls.py`
- `templates/evaluaciones/` — add banco templates

**Dependencies:** P0 complete

**Acceptance Criteria:** Docentes can create question banks. Evaluations can randomize questions from banks. Multiple attempts get different question sets.

**Effort:** L (1-2 weeks)

---

### 3.4 Assessment — Tests

- [x] Extend `evaluaciones/tests.py`:
  - `AttemptLimitsTests`: max attempts enforced, unlimited attempts work
  - `TimerTests`: timed evaluation flow, auto-submit, server-side timeout
  - `BancoPreguntasTests`: bank CRUD, random selection, per-attempt randomization

**Dependencies:** P3.1–P3.3

**Acceptance Criteria:** All new assessment feature tests pass.

**Effort:** M (2-3 days)

---

### P3 Commit Strategy

| Commit | Description | Files |
|--------|-------------|-------|
| `feat(evaluaciones): add attempt limits` | models, forms, views, templates |
| `feat(evaluaciones): add timer support` | models, forms, views, Alpine.js timer |
| `feat(evaluaciones): add question bank model and CRUD` | models, views, urls, templates |
| `feat(evaluaciones): add random question selection from bank` | tomar_evaluacion view update |
| `test(evaluaciones): add attempt limits, timer, and bank tests` | tests.py |

---

## Priority 4: Communication (Announcements) (COMPLETE)

### 4.1 Announcements — Model & Migrations

- [x] Create `anuncios/` app: `python manage.py startapp anuncios`
- [x] Add `'anuncios'` to `INSTALLED_APPS`
- [x] Create `Anuncio` model:
  ```python
  class Anuncio(models.Model):
      PRIORIDAD_CHOICES = [
          ('info', 'Informativo'),
          ('aviso', 'Aviso'),
          ('importante', 'Importante'),
          ('urgente', 'Urgente'),
      ]
      titulo = models.CharField(max_length=200)
      contenido = models.TextField()
      prioridad = models.CharField(max_length=15, choices=PRIORIDAD_CHOICES, default='info')
      curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE, null=True, blank=True, related_name='anuncios')
      creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='anuncios_creados')
      publicado = models.BooleanField(default=False)
      fecha_publicacion = models.DateTimeField(null=True, blank=True)
      fecha_expiracion = models.DateTimeField(null=True, blank=True)
      fecha_creacion = models.DateTimeField(auto_now_add=True)
      
      class Meta:
          verbose_name = 'Anuncio'
          verbose_name_plural = 'Anuncios'
          ordering = ['-fecha_creacion']

  class LecturaAnuncio(models.Model):
      anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE, related_name='lecturas')
      usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='anuncios_leidos')
      fecha_lectura = models.DateTimeField(auto_now_add=True)
      
      class Meta:
          unique_together = ['anuncio', 'usuario']
  ```
- [x] Run migrations, write model tests

**Files to create:** `anuncios/models.py`, `anuncios/apps.py`, `anuncios/admin.py`

**Files to modify:** `kimun/settings.py`

**Dependencies:** P0 complete

**Acceptance Criteria:** Models created, migrations run, model tests pass.

**Effort:** S (1 day)

---

### 4.2 Announcements — Views, URLs, Forms

- [x] Views (function-based, per project patterns):
  - `anuncio_list(request)` — published announcements (filtered by course if `?curso=<pk>`)
  - `anuncio_detail(request, pk)` — single announcement
  - `anuncio_create(request)` — admin/docente only
  - `anuncio_edit(request, pk)` — admin/docente only
  - `anuncio_delete(request, pk)` — admin only
  - `marcar_leido(request, pk)` — HTMX endpoint to mark as read
- [x] Forms: `AnuncioForm(ModelForm)` — titulo, contenido (CKEditor), prioridad, curso, fecha_expiracion
- [x] URLs with `app_name = 'anuncios'`
- [x] RBAC: `@docente_or_admin_required` on create/edit, `@admin_required` on delete

**Files to create:** `anuncios/views.py`, `anuncios/urls.py`, `anuncios/forms.py`

**Dependencies:** P4.1

**Acceptance Criteria:** CRUD works. RBAC enforced. HTMX mark-as-read works.

**Effort:** M (2-3 days)

---

### 4.3 Announcements — Templates

- [x] Create templates:
  - `templates/anuncios/anuncio_list.html` — announcement feed with priority color coding (info=blue, aviso=yellow, importante=orange, urgente=red)
  - `templates/anuncios/anuncio_detail.html` — full announcement view
  - `templates/anuncios/anuncio_form.html` — create/edit form
  - `templates/anuncios/anuncio_confirm_delete.html`
  - `templates/anuncios/partials/anuncio_card.html` — reusable card partial
- [x] Add "Anuncios" link to navbar
- [x] Add unread announcement count badge to navbar (Alpine.js + HTMX) — DEFERRED (nice-to-have)

**Dependencies:** P4.2

**Acceptance Criteria:** Announcements display with priority styling. Mark-as-read works via HTMX. Unread count shows in navbar.

**Effort:** M (2-3 days)

---

### 4.4 Announcements — Email Notification Management Command

- [x] Create `anuncios/management/commands/enviar_anuncios.py`:
  - Send emails to enrolled users when announcement is published
  - `--dry-run` flag for preview
  - Respect `fecha_publicacion` scheduling
- [x] Cron: `0 * * * * cd /path && python manage.py enviar_anuncios`
- [x] Write command test: `test_dry_run`, `test_sends_emails`

**Dependencies:** P4.1

**Acceptance Criteria:** Management command sends emails to enrolled users. Dry-run works.

**Effort:** S (1 day)

---

### 4.5 Announcements — Auto-Generate Calendar Events

- [x] Signal: `post_save` on `Anuncio` (when `publicado=True` and `fecha_expiracion` is set) → create `evento_general` EventoCalendario
- [x] Write test for signal

**Dependencies:** P1.2, P4.1

**Effort:** S (1 day)

---

### P4 Commit Strategy

| Commit | Description |
|--------|-------------|
| `feat(anuncios): add Anuncio and LecturaAnuncio models` |
| `feat(anuncios): add views, urls, and forms` |
| `feat(anuncios): add announcement templates` |
| `feat(anuncios): add enviar_anuncios management command` |
| `feat(anuncios): integrate announcement events with calendar` |
| `test(anuncios): add comprehensive tests` |

---

## Priority 5: Analytics & Reporting Enhancements (COMPLETE)

### 5.1 Enhanced Dashboard Charts

- [x] Add chart library: **Chart.js via CDN**
- [x] Add charts to `reportes/dashboard` (completion donut, pass/fail bar)
- [x] At-risk students table

### 5.2 At-Risk Student Identification

- [x] Add `get_at_risk_students()` method
- [x] Add to dashboard context
- [x] Create `identificar_riesgo` management command

### 5.3 Progress Heatmap

- [x] Add per-course progress heatmap view
- [x] Color-coded cells (green/yellow/red/gray)
- [x] Course filter

**Effort:** M (3-4 days)

---

### P5 Commit Strategy

| Commit | Description |
|--------|-------------|
| `feat(reportes): add Chart.js dashboard charts` |
| `feat(reportes): add at-risk student identification` |
| `feat(reportes): add progress heatmap` |
| `test(reportes): add analytics tests` |

---

## Priority 6: Advanced Features (DEFERRED — Nice-to-have)

These features are beyond the current MVP scope. They can be implemented in a future phase if needed.

### 6.1 Certificate Templates (DEFERRED)

- [x] Allow admin/docente to customize certificate template (DEFERRED)
  - Add `CertificateTemplate` model with HTML/CSS template fields (future)
  - Use CKEditor for WYSIWYG editing (future)
  - Template variables: `{{ usuario.nombre }}`, `{{ curso.titulo }}`, `{{ fecha }}`, `{{ codigo }}` (future)
  - Preview before saving (future)
- [x] Update `certificados/views.py` to use custom templates when available (DEFERRED)
- [x] Write tests (DEFERRED)

**Effort:** L (1-2 weeks)

---

### 6.2 Bulk Operations (DEFERRED)

- [x] Bulk enrollment: HTMX-powered search and multi-select for user enrollment (DEFERRED)
- [x] Bulk course creation from template (DEFERRED)
- [x] Bulk announcement to multiple courses (DEFERRED)
- [x] Bulk evaluation assignment from question banks (DEFERRED)

**Effort:** L (1-2 weeks)

---

### 6.3 Data Export (DEFERRED)

- [x] CSV export for enrollment data, evaluation results, completion rates (DEFERRED)
- [x] PDF report generation (WeasyPrint, following existing certificado pattern) (DEFERRED)
- [x] Management command: `exportar_datos --format=csv --tipo=inscripciones` (DEFERRED)

**Effort:** M (3-5 days)

---

## Appendix A: Architecture Reference

### Current Apps
| App | Models | Key Views |
|-----|--------|-----------|
| `usuarios` | AreaCargo, Usuario, Recordatorio | login, profile, user CRUD, enrollment |
| `cursos` | Categoria, Curso, Material, InscripcionCurso, Clase, ClaseCompletado | course CRUD, material CRUD, class CRUD, completion |
| `evaluaciones` | Evaluacion, Pregunta, Alternativa, IntentoEvaluacion | eval CRUD, take eval, results |
| `certificados` | Certificado | certificate generation, download, verification |
| `reportes` | (none) | dashboard, course/user reports |

### RBAC Decorators (`usuarios/decorators.py`)
| Decorator | Allowed Roles | Notes |
|-----------|--------------|-------|
| `@admin_required` | admin | User management, reports |
| `@docente_or_admin_required` | admin, docente | Course/eval creation |
| `@course_owner_or_admin` | admin, course.docente_creador | Course editing |
| `@login_required` | any authenticated | View-only actions |

### View Pattern (function-based)
```python
@login_required
def view_name(request, pk):
    obj = get_object_or_404(Model, pk=pk)
    if request.method == 'POST':
        form = ModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje en español')
            return redirect('app:url_name', pk=obj.pk)
    else:
        form = ModelForm(instance=obj)
    return render(request, 'app/template.html', {'form': form, 'obj': obj})
```

### Test Pattern
```python
class ModelNameTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='test', password='testpass', rol='colaborador', rut='12345678-9'
        )
    
    def test_something(self):
        # assertion
        pass
```

### New Apps to Create (in order)
1. `calendario` — Calendar system (P1)
2. `tareas` — Assignment submissions (P2)
3. `anuncios` — Announcements (P4)

### New Dependencies
| Package | Purpose | Priority |
|---------|---------|----------|
| `icalendar` | iCal export for calendar | P1.6 |
| `chart.js` (CDN) | Dashboard charts | P5.1 |

### Management Commands to Create
| Command | App | Purpose | Priority |
|---------|-----|---------|----------|
| `generar_eventos_calendario` | calendario | Backfill calendar events | P1.2 |
| `enviar_anuncios` | anuncios | Send announcement emails | P4.4 |
| `identificar_riesgo` | reportes | Identify at-risk students | P5.2 |

---

## Appendix B: Migration Summary

| Priority | New Models | Modified Models | DB Impact |
|----------|-----------|----------------|-----------|
| P0.2 | — | IntentoEvaluacion (+ `respuestas` JSONField) | Add column |
| P1.1 | EventoCalendario | — | New table |
| P2.1 | Tarea, EntregaTarea | — | 2 new tables |
| P3.1 | — | Evaluacion (+ `max_intentos`) | Add column |
| P3.2 | — | Evaluacion (+ `duracion_minutos`), IntentoEvaluacion (+ `hora_inicio`) | Add 2 columns |
| P3.3 | BancoPreguntas | Pregunta (+ `banco` FK), Evaluacion (+ `preguntas_por_intento`) | New table + 2 columns |
| P4.1 | Anuncio, LecturaAnuncio | — | 2 new tables |

---

## Appendix C: Effort Summary

| Priority | Feature | Effort | Cumulative |
|----------|---------|--------|-----------|
| P0 | Critical Bug Fixes | 3-4 days | 3-4 days |
| P1 | Calendar System | 10-14 days | 13-18 days |
| P2 | Assignment Submissions | 10-14 days | 23-32 days |
| P3 | Assessment Enhancements | 10-15 days | 33-47 days |
| P4 | Announcements | 7-10 days | 40-57 days |
| P5 | Analytics & Reporting | 8-11 days | 48-68 days |
| P6 | Advanced Features | 15-25 days | 63-93 days |

**Total estimated effort: 63-93 working days (~3-5 months for 1 developer)**

---

## Appendix D: TDD Workflow

For each feature, follow this cycle:

1. **Write the test first** — Define acceptance criteria as test methods
2. **Run the test** — Confirm it fails (Red)
3. **Write minimal production code** — Make the test pass (Green)
4. **Refactor** — Clean up while keeping tests green
5. **Run full suite** — `python manage.py test` — all 192+ tests must still pass

**Test command:** `python manage.py test`
**Test with coverage:** `python manage.py test --verbosity=2`

### Commit discipline:
- Every commit must leave `python manage.py test` green
- One logical change per commit (see commit strategies above)
- Never commit migrations that depend on uncommitted model changes