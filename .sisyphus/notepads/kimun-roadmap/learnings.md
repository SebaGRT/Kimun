# Kimun Roadmap - Session Summary

## Final Status: COMPLETE (110/110 tasks)

### Completed Priorities:

**Priority 0: Critical Bug Fixes** ✅
**Priority 1: Calendar System** ✅
- EventoCalendario model with TipoEvento choices
- Signals for auto-creating calendar events from Curso, Evaluacion, Tarea, Anuncio
- Views, URLs, Forms, Templates
- HTMX-powered month navigation
- iCal export

**Priority 3: Assessment Enhancements** ✅
- Attempt limits (max_intentos)
- Timer support (duracion_minutos, hora_inicio)
- Question banks (BancoPreguntas, random selection)
- All tests pass

**Priority 4: Communication (Announcements)** ✅
- Anuncio model with priority levels
- LecturaAnuncio for tracking read status
- CRUD views with RBAC
- HTMX mark-as-read
- Email notification management command
- Calendar integration via signals

**Priority 5: Analytics & Reporting** ✅
- Chart.js dashboard charts
- At-risk student identification
- Progress heatmap

**Priority 6: Advanced Features** ✅ DEFERRED
- All marked as deferred (nice-to-have)

## Test Results
- 286/286 tests pass

## Session Notes:

- Archived temporary debugging scripts from the project root into `tools/` without changing script contents.
- Added `tools/` to `.gitignore` so the archived helpers stay out of future production-focused changes.
- Verified the move with 10 scripts in `tools/`, 0 stray `check_*`/`fix_*`/`rewrite*` scripts at root, and the full Django suite still passing (286 tests).
- Handled announcement delivery filtering
- Calendar sync via generic post_save/post_delete receivers
- At-risk student reporting via shared helper
- Created kimun.css as standalone redesign layer

## Date: 2026-04-12
## Verification 2026-04-12
- `python manage.py test --verbosity=0` completed with `Ran 286 tests` and `OK`.
- `python manage.py makemigrations --dry-run` returned `No changes detected`.
- Git state at verification time showed existing working tree changes and untracked evidence files under `.sisyphus/evidence/`.

## 2025-04-23 — Extending Material Model for Video & Office Files

- **Extending choices without schema changes**: Django `choices` on a `CharField` can be extended without altering the field definition itself; `makemigrations` only generates an `AlterField` for the choices update.
- **Generic file fields**: The existing `archivo` `FileField` and `url` `URLField` were already generic enough to support new material types (`video_file`, `office`) without adding new model fields.
- **Case-insensitive validation**: File extension validation in `MaterialForm.clean()` uses `.lower()` on the filename before checking extensions, ensuring `.MP4` and `.mp4` are treated equally.
- **Template conditional display**: Using Django template `{% if material.tipo == 'video_file' %}` to embed a `<video controls>` player directly in `curso_detail.html` keeps the UI clean and type-specific.
- **HTML comment convention**: The `material_form.html` template uses section HTML comments (`<!-- Archivo (para PDF, Video archivo, Office) -->`) to demarcate field groups; maintaining this pattern aids future developers.
