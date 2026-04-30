# Kimün LMS — Code Quality & Feature Completion Plan
## Option B + C

**Branch**: `development` | **Date**: 2025-04-21

---

## Summary

| Stream | Status | Effort |
|--------|--------|--------|
| **B1. RBAC Cleanup** | 68 inline checks found; replace with existing decorators + new generic `owner_or_admin` | Medium |
| **B2. ModelForms** | 7 raw POST patterns; replace 1 (`inscribir_curso`), document 6 | Low |
| **B3. Query Optimization** | Zero DB indexes; add 11 indexes + fix N+1 in reports | Medium |
| **C1. Evaluation Engine** | Timer bug + missing server-side expiry + no shuffle | Medium |
| **C2. Progress Tracking** | No unified model; create `ProgresoCurso` + signal updates | Medium |
| **C3. Audit Logging** | Zero audit trail; create `Auditoria` model + middleware + signals | Medium |

---

## Execution Waves

```
Wave 1 (Parallel, no deps):
├── B1.1 Audit inline checks          [explore]
├── B2.1 Audit raw POST               [explore]
├── B3.1 Add DB indexes               [quick]
├── C1.1 Write evaluation tests       [deep]
└── C3.1 Create Auditoria model       [deep]

Wave 2 (After Wave 1):
├── B1.2 Create missing decorators    [quick]
├── B1.3 Replace checks per-app       [deep x6]
├── B2.2 InscripcionDirectaForm       [quick]
├── B3.2 Fix N+1 queries              [deep]
├── C1.2 Fix timer + server expiry    [deep]
├── C1.3 Validate randomization       [quick]
└── C3.2 Wire audit signals           [quick]

Wave 3 (After Wave 2):
├── C2.1 Create ProgresoCurso model   [deep]
└── C3.3 Admin interface for audit    [quick]

Wave 4 (After Wave 3):
└── C2.2 Refactor views to use it     [deep]
```

---

## Key Decisions

1. **Keep login raw POST** — `AuthenticationForm` adds no value for a simple custom login.
2. **Keep evaluation JSON POST** — Nested question structures cannot be represented by ModelForms.
3. **Generic `owner_or_admin` decorator** — Avoids creating 5+ specific decorators.
4. **Keep dashboard role switches inline** — Feature toggling, not access control.
5. **Signals for audit logging** — Minimizes view code changes; only cert approval needs explicit call.
6. **ProgresoCurso recalculated on-demand** — Avoid stale data; `actualizado_en` allows future caching.

---

## Risk Assessment

| Risk | Prob | Impact | Mitigation |
|------|------|--------|------------|
| Breaking permission logic | Medium | **High** | TDD first, full suite after each app, commit per-app |
| Timer auto-submit loses answers | High (existing) | Medium | Fix template JS to populate hidden input before submit |
| N+1 optimization changes semantics | Low | Medium | Run report tests, verify output before/after |

---

## Verification Strategy

- **Per-app test runs** after each change
- **Migration check**: `python manage.py makemigrations --check --dry-run`
- **Query count verification** for N+1 fixes
- **Manual checklist**: admin/docente/colaborador access paths, timer behavior, audit log entries

---

## Files to Change (25 files across 8 apps)

| File | B1 | B2 | B3 | C1 | C2 | C3 |
|------|:--:|:--:|:--:|:--:|:--:|:--:|
| `usuarios/decorators.py` | ✅ | | | | | |
| `usuarios/mixins.py` | ✅ | | | | | |
| `usuarios/models.py` | | | | | | ✅ |
| `usuarios/middleware.py` (new) | | | | | | ✅ |
| `usuarios/signals.py` (new) | | | | | | ✅ |
| `usuarios/admin.py` | | | | | | ✅ |
| `usuarios/views.py` | ✅ | ✅ | | | | |
| `usuarios/tests.py` | ✅ | ✅ | | | | ✅ |
| `cursos/models.py` | | | ✅ | | ✅ | |
| `cursos/views.py` | ✅ | | ✅ | | ✅ | |
| `cursos/forms.py` | | ✅ | | | | |
| `cursos/utils.py` (new) | | | | | ✅ | |
| `cursos/tests.py` | | | | | ✅ | |
| `evaluaciones/views.py` | ✅ | | | ✅ | | |
| `evaluaciones/tests.py` | | | | ✅ | | |
| `evaluaciones/tomar_evaluacion.html` | | | | ✅ | | |
| `certificados/views.py` | ✅ | | | | | ✅ |
| `reportes/views.py` | | | ✅ | | | |
| `reportes/tests.py` | | | ✅ | | | |
| `tareas/views.py` | ✅ | | | | | |
| `anuncios/views.py` | ✅ | | | | | |
| `calendario/views.py` | ✅ | | | | | |
| `kimun/settings.py` | | | | | | ✅ |

---

## Detailed Task Breakdown

### Wave 1

#### B1.1 Audit inline role checks
Document every inline check with: file, line number, current logic, suggested replacement, risk level.

#### B2.1 Audit raw POST handling
Identify all raw POST patterns and decide: replace with ModelForm, document as intentional, or refactor to Form.

#### B3.1 Add DB indexes
Add `Meta.indexes` to: Curso, InscripcionCurso, IntentoEvaluacion, ClaseCompletado, Certificado, EventoCalendario, Auditoria.

#### C1.1 Write evaluation engine tests (TDD)
Add tests for: max_intentos enforcement, timer expiry rejection, question subset selection, shuffle order.

#### C3.1 Create Auditoria model + middleware
Create `Auditoria` model in `usuarios/models.py`, middleware in `usuarios/middleware.py`, update `settings.py`.

### Wave 2

#### B1.2 Create missing decorators
Add `colaborador_required` and generic `owner_or_admin` to `usuarios/decorators.py` and corresponding mixins.

#### B1.3 Replace inline checks (per-app)
Replace inline checks in: certificados, evaluaciones, cursos, tareas, anuncios, calendario.

#### B2.2 InscripcionDirectaForm
Create form in `cursos/forms.py`, replace raw POST in `usuarios/views.py`.

#### B3.2 Fix N+1 queries
Fix `get_at_risk_students()`, `progreso_heatmap()`, `reporte_curso()` with batch queries.

#### C1.2 Fix timer + server expiry
Fix template JS auto-submit, add server-side `hora_inicio` validation.

#### C1.3 Validate randomization
Add explicit `random.shuffle()` after subset selection.

#### C3.2 Wire audit signals
Create `usuarios/signals.py` with post_save and auth signal handlers.

### Wave 3

#### C2.1 Create ProgresoCurso model
Add model to `cursos/models.py`, utility in `cursos/utils.py`, signal-based auto-update.

#### C3.3 Admin interface for audit
Add read-only `AuditoriaAdmin` in `usuarios/admin.py`.

### Wave 4

#### C2.2 Refactor views to use ProgresoCurso
Replace inline progress in `cursos/views.py:curso_detail` and `usuarios/views.py:perfil`.
