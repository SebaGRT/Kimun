# Architecture

**Analysis Date:** 2026-04-24

## Pattern Overview

**Overall:** Monolithic Django MVT (Model-View-Template) with function-based views and role-based access control.

**Key Characteristics:**
- Classic Django multi-app architecture with 8 custom apps
- Function-based views (FBV) with custom decorator authorization
- Server-side rendered HTML templates with Tailwind CSS
- PostgreSQL database via Supabase with SSL
- Supabase Storage for media files (django-supabase-storage)
- Custom user model extending AbstractUser
- Signal-driven audit logging and progress calculation
- No REST API — all interactions are traditional form posts and page loads

## Layers

**Project Configuration (`kimun/`):**
- Purpose: Django project settings, root URL routing, WSGI entry point
- Location: `kimun/`
- Contains: `settings.py`, `urls.py`, `wsgi.py`
- Depends on: All installed apps
- Used by: Django development server / WSGI runtime

**Authentication & Users (`usuarios/`):**
- Purpose: Custom user model, login/logout, user management, audit logging, reminders
- Location: `usuarios/`
- Contains: Models, views, forms, decorators, middleware, signals, utils
- Depends on: `cursos` (for enrollments), Django auth
- Used by: All other apps

**Courses (`cursos/`):**
- Purpose: Course content management, lessons, materials, enrollments, progress tracking
- Location: `cursos/`
- Contains: Models, views, forms, admin, utils
- Depends on: `usuarios` (custom user model)
- Used by: `evaluaciones`, `certificados`, `tareas`, `calendario`, `anuncios`, `reportes`

**Evaluations (`evaluaciones/`):**
- Purpose: Quiz/exam creation, question banks, attempt tracking, scoring
- Location: `evaluaciones/`
- Contains: Models, views, forms
- Depends on: `cursos` (Curso), `usuarios` (Usuario)
- Used by: `cursos` (progress calculation), `reportes`, `certificados`

**Certificates (`certificados/`):**
- Purpose: Certificate generation, approval workflow, PDF generation, verification
- Location: `certificados/`
- Contains: Models, views
- Depends on: `cursos` (Curso), `usuarios` (Usuario, Auditoria)
- Used by: `usuarios` (dashboard), `reportes`

**Tasks (`tareas/`):**
- Purpose: Assignment creation, submission, grading
- Location: `tareas/`
- Contains: Models, views, forms
- Depends on: `cursos` (Curso), `usuarios` (Usuario)
- Used by: None directly (standalone feature)

**Calendar (`calendario/`):**
- Purpose: Event management, calendar view, iCal export
- Location: `calendario/`
- Contains: Models, views, forms
- Depends on: `cursos` (Curso), `evaluaciones` (Evaluacion), `usuarios` (Usuario)
- Used by: None directly

**Announcements (`anuncios/`):**
- Purpose: Internal announcements, read receipts, priority levels
- Location: `anuncios/`
- Contains: Models, views, forms
- Depends on: `cursos` (Curso, optional), `usuarios` (Usuario)
- Used by: None directly

**Reports (`reportes/`):**
- Purpose: Admin dashboards, analytics, heatmaps, at-risk student detection
- Location: `reportes/`
- Contains: Views only (no models)
- Depends on: `usuarios`, `cursos`, `evaluaciones`, `certificados`
- Used by: None directly (read-only analytics)

## Data Flow

**Course Enrollment Flow:**
1. Admin/Docente creates a `Curso` in `cursos/views.py`
2. Admin enrolls users via `InscripcionCurso` (`usuarios/views.py`)
3. `notificar_inscripcion()` sends email notification (`usuarios/utils.py`)
4. Colaborador views course content, completes `Clase` instances
5. `ClaseCompletado` records are created (`cursos/views.py`)
6. Signal `actualizar_progreso_por_evaluacion` updates `ProgresoCurso` (`usuarios/signals.py`)

**Evaluation Flow:**
1. Docente creates `Evaluacion` with `Pregunta` and `Alternativa` records (`evaluaciones/views.py`)
2. Colaborador takes evaluation (`tomar_evaluacion` view)
3. `IntentoEvaluacion` is created with score and `aprobado` flag
4. Signal `log_evaluacion_intento` writes to `Auditoria` (`usuarios/signals.py`)
5. Signal `actualizar_progreso_por_evaluacion` triggers progress recalculation
6. If all evaluations passed, `InscripcionCurso.estado` changes to `completado`
7. Signal `log_curso_completado` writes to `Auditoria`

**Certificate Flow:**
1. When course is completed, `Certificado` record is created (pending state)
2. Docente/Admin reviews pending certificates (`certificados/views.py`)
3. On approval: `estado='aprobado'`, PDF generated on first download via WeasyPrint
4. `Auditoria` record created on approval
5. Public verification available via UUID (`verificar_certificado`)

**State Management:**
- Server-side session state for evaluation timing (`request.session` keys like `eval_{pk}_hora_inicio`)
- Database state for all persistent data
- No frontend state management framework

## Key Abstractions

**Custom User Model (`usuarios.models.Usuario`):**
- Purpose: Extends AbstractUser with `rut`, `rol` (admin/docente/colaborador), `cargo` (AreaCargo FK)
- Examples: `usuarios/models.py`
- Pattern: Standard Django custom user model with `AUTH_USER_MODEL = 'usuarios.Usuario'`

**Permission Decorators (`usuarios.decorators`):**
- Purpose: Reusable role-based and ownership access control
- Examples: `usuarios/decorators.py`
- Pattern: `role_required()`, `course_owner_or_admin()`, `owner_or_admin(model_class, owner_field)`

**Audit Logging (`usuarios.models.Auditoria`):**
- Purpose: Immutable event log with IP address, action type, object reference
- Examples: `usuarios/models.py`, `usuarios/signals.py`
- Pattern: Signal-driven write-once log with admin read-only interface

**Progress Tracking (`cursos.models.ProgresoCurso`):**
- Purpose: Cached progress percentage combining class completion and evaluation scores
- Examples: `cursos/models.py`, `cursos/utils.py`
- Pattern: get-or-create utility with `calcular_progreso()` method

## Entry Points

**WSGI Application:**
- Location: `kimun/wsgi.py`
- Triggers: Production WSGI server (gunicorn, etc.)
- Responsibilities: Bootstraps Django settings and application

**Root URL Router:**
- Location: `kimun/urls.py`
- Triggers: All HTTP requests
- Responsibilities: Delegates to app-level URL configs, serves CKEditor upload, static/media in DEBUG

**Django Admin:**
- Location: `usuarios/admin.py` (custom `KimunAdminSite`)
- Triggers: `/admin/` requests
- Responsibilities: Role-filtered app list (admin sees all, docente sees cursos/evaluaciones, colaborador sees cursos/certificados)

## Error Handling

**Strategy:** Django's built-in exception handling with custom `HttpResponseForbidden` for authorization failures.

**Patterns:**
- Views return `HttpResponseForbidden('message')` for unauthorized access
- Form validation errors are attached to form instances and rendered in templates
- Database `IntegrityError` is caught explicitly in `clase_create` and `clase_edit` for duplicate ordering
- `get_object_or_404()` used consistently for object retrieval
- `transaction.atomic()` used in evaluation creation/update for data consistency

## Cross-Cutting Concerns

**Logging:** `AuditoriaMiddleware` captures client IP into `request.auditoria_ip`; signals write structured audit records for login/logout, course completion, evaluation attempts, certificate approvals, user creation, and enrollments.

**Validation:** Form-level validation in `CursoForm`, `MaterialForm`, `ClaseForm`, `EvaluacionForm`, etc. Custom `clean()` methods enforce business rules (file types, ordering uniqueness, URL requirements).

**Authentication:** Django's session-based authentication. `login_required` on nearly all views. Custom decorators (`admin_required`, `docente_or_admin_required`, `course_owner_or_admin`, `colaborador_required`) enforce role-based access. `owner_or_admin` generic decorator supports dot-notation field resolution for nested ownership checks.

---

*Architecture analysis: 2026-04-24*
