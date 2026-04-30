# Kimün LMS — Certificados Pipeline Overhaul Plan (v2)

**Date**: 2025-04-22
**Context**: Elderly-care skills training LMS (not just first-aid)
**Approval Strategy**: Auto-approval by default
**Expiration Alerts**: Dashboard indicator only

---

## 1. Executive Summary of Current Flaws

The Kimün certificate pipeline has a **critical logic bug** that generates certificates prematurely and repeatedly:

| # | Flaw | Severity | Evidence |
|---|------|----------|----------|
| 1 | **Certificate generated on every evaluation pass** | **CRITICAL** | `evaluaciones/views.py` auto-creates a `Certificado` every time `aprobado=True` on an `IntentoEvaluacion`, even if the user hasn't completed all classes or all evaluations |
| 2 | **No idempotency guard** | **CRITICAL** | No check prevents duplicate certificates for the same (user, course) pair. A user retaking a passed evaluation gets another certificate entry |
| 3 | **Eligibility logic fragmented** | High | Criteria are split between `evaluaciones/views.py` (evaluations only) and `certificados/views.py:generar_certificado` (batch logic). No single source of truth |
| 4 | **No material completion gating** | High | A user can pass all evaluations without completing classes and still get certified |
| 5 | **Manual batch generation is redundant** | Medium | `generar_certificado` loops through enrolled students creating certs, but auto-generation already (brokenly) does this per-evaluation |
| 6 | **Approval workflow is unnecessary overhead** | Medium | For theory-focused elderly-care training, mandatory manual approval slows down delivery without adding value |
| 7 | **No expiration handling** | Medium | Certificates should show validity period, even if only as a dashboard indicator |
| 8 | **No per-course certificate configuration** | Medium | All courses use the same hardcoded logic, but "Inducción" and "RCP Avanzado" should not behave identically |
| 9 | **PDF generation inconsistent** | Low | Eager for request.user, lazy for others |
| 10 | **No course completion validation** | Low | `InscripcionCurso.estado` is not checked before cert generation |

### Root Cause Analysis

The bug is in `evaluaciones/views.py`, approximately lines 298–321 inside `tomar_evaluacion()`:

```python
# Simplified current (broken) logic:
if intento.aprobado:
    Certificado.objects.create(usuario=request.user, curso=curso)
```

This runs **every time** a user passes **any** evaluation, regardless of:
- Whether other evaluations in the course are still pending
- Whether the user has completed all classes
- Whether a certificate already exists for this (user, course)

**Fix principle**: Certificate generation must be **idempotent**, **gated by full course completion**, and **triggered only once** when all eligibility criteria are first satisfied.

---

## 2. Recommended Eligibility Criteria for Elderly-Care Skills Training

Kimün trains staff in **diverse skills for elderly care** — RCP, prevención de caídas, manejo de demencia, nutrición geriátrica, etc. The certification logic must be **theory-first** (content mastery demonstrated via evaluations) but also **ensure full course engagement**.

### Core Eligibility Rule

A learner is eligible for a certificate **if and only if**:

1. **Enrollment is active** (`InscripcionCurso.estado != 'abandonado'`)
2. **All classes are completed** (100% of `Clase` records have a matching `ClaseCompletado` for this user)
3. **All evaluations are passed** (for every `Evaluacion` in the course, the user's latest `IntentoEvaluacion.aprobado == True`)
4. **No existing certificate** for this (user, course) pair in a non-revoked state

### Per-Course Configuration (Future-Proofing)

```python
class Curso(models.Model):
    # ... existing fields ...

    # Certificate settings
    certificado_requiere_clases = models.BooleanField(default=True)
    certificado_porcentaje_minimo_clases = models.PositiveIntegerField(default=100)
    certificado_requiere_evaluaciones = models.BooleanField(default=True)
    certificado_vigencia_meses = models.PositiveIntegerField(default=0, help_text="0 = sin vencimiento")
    certificado_activo = models.BooleanField(default=True, help_text="Este curso emite certificado al completarse")
```

### Auto-Approval Strategy

Since this is **theory-focused elderly-care training** (not high-stakes medical licensure):

- **Default**: Auto-approve on eligibility. `Certificado.estado = 'aprobado'` immediately.
- **Override**: Per-course `certificado_aprobacion_manual = True` can force `pendiente` state (for future use).
- **No tiered approval**: Unnecessary for current scope.

### Why This Prevents the Current Bug

```python
# CORRECT logic (in signal handler):
def intento_post_save(sender, instance, created, **kwargs):
    if not instance.aprobado:
        return

    curso = instance.evaluacion.curso
    usuario = instance.usuario

    # 1. Check if cert already exists (idempotency)
    if Certificado.objects.filter(usuario=usuario, curso=curso).exclude(estado='revocado').exists():
        return

    # 2. Check all evaluations passed
    evaluaciones = curso.evaluaciones.all()
    for ev in evaluaciones:
        ultimo = ev.intentos.filter(usuario=usuario).order_by('-fecha_intento').first()
        if not ultimo or not ultimo.aprobado:
            return  # Not all evaluations passed yet

    # 3. Check all classes completed
    total_clases = curso.clases.count()
    completadas = ClaseCompletado.objects.filter(usuario=usuario, clase__curso=curso).count()
    if completadas < total_clases:
        return  # Not all classes completed yet

    # 4. All criteria met → create certificate ONCE
    Certificado.objects.create(
        usuario=usuario,
        curso=curso,
        estado='aprobado',  # Auto-approval
    )
```

---

## 3. Five Overhaul Proposals

### Proposal 1: The Minimal Patch — "Stop the Bleeding"

**Concept**: Fix only the critical bug (duplicate/premature certs). Extract eligibility to a helper. Remove conflicting manual generation. Add idempotency check.

**Eligibility logic**: All evaluations passed + no existing cert.

**Generation trigger**: Keep auto-generation in `evaluaciones/views.py` but add guards.

**Approval workflow**: None (keep current implicit behavior).

**Data model changes**: None.

**UI/UX impact**: None.

**Pros**: Lowest effort, fixes the immediate pain.
**Cons**: Does not fix class completion gating, no per-course config, no expiration.
**Effort**: Low (1 day)
**Best for**: Emergency hotfix.

---

### Proposal 2: The Signal-Driven Eligibility Engine — "The Right Fix" (RECOMMENDED)

**Concept**: Build a centralized `CertificateEligibilityService`. Use Django signals on `IntentoEvaluacion` and `ClaseCompletado` to trigger eligibility checks. Idempotent, gated by full completion, auto-approved.

**Eligibility logic**: Multi-condition AND engine:
- Active enrollment
- All classes completed (configurable percentage)
- All evaluations passed
- No existing non-revoked certificate

**Generation trigger**: Automatic via signals. Only fires once when all criteria are first satisfied.

**Approval workflow**: Auto-approve (`aprobado`). Optional per-course manual override.

**Data model changes**:
```python
# certificados/models.py — add to Certificado:
estado = models.CharField(max_length=20, choices=[...], default='aprobado')  # Default changed
motivo_revocacion = models.TextField(blank=True, null=True)

# cursos/models.py — add to Curso:
certificado_activo = models.BooleanField(default=True)
certificado_requiere_clases = models.BooleanField(default=True)
certificado_porcentaje_minimo_clases = models.PositiveIntegerField(default=100)
certificado_requiere_evaluaciones = models.BooleanField(default=True)
certificado_vigencia_meses = models.PositiveIntegerField(default=0)
```

**UI/UX impact**:
- **Admin**: Can toggle `certificado_activo` per course. Can revoke certs with reason.
- **Docente**: No approval queue (auto-approve). Can see who has certs for their courses.
- **Colaborador**: Dashboard shows earned certificates with expiration date (if applicable). No "pending" state.

**Pros**:
- Fixes the core bug permanently.
- Idempotent — never duplicate certs.
- Gated by full completion (classes + evaluations).
- Per-course config allows flexibility.
- Auto-approval fits theory-focused training.
- Still manageable for university project.

**Cons**:
- No expiration alerts (but dashboard indicator is acceptable).
- No advanced workflows.

**Effort**: Medium (1 week)
**Best for**: **Kimün / ALUMCO**. This is the correct scope.

---

### Proposal 3: The Expiration-Aware Pipeline

**Concept**: Extends Proposal 2 with `fecha_vencimiento`, dashboard expiration indicators, and a management command to mark expired certs.

**Eligibility logic**: Same as Proposal 2.

**Generation trigger**: Auto via signals.

**Approval workflow**: Auto.

**Data model changes**:
```python
# Add to Certificado:
fecha_vencimiento = models.DateTimeField(null=True, blank=True)

# Add management command:
# python manage.py actualizar_vencimientos
```

**UI/UX impact**:
- **Colaborador dashboard**: Certs show "Válido hasta" date. Expired certs shown in separate section.

**Pros**: Adds compliance value without complexity.
**Cons**: Slightly more effort.
**Effort**: Medium (1.5 weeks)
**Best for**: If ALUMCO wants to track certification validity.

---

### Proposal 4: The Competency-Based System

**Concept**: Certs represent demonstrated skills, not just course completion. Granular competency tracking.

**Eligibility logic**: Per-competency thresholds mapped to evaluations.

**Generation trigger**: Competency audit on evaluation completion.

**Approval workflow**: Per-competency.

**Data model changes**: New `Competencia`, `EvaluacionCompetencia`, `CertificadoCompetencia` models.

**Pros**: Future-proof, micro-credential ready.
**Cons**: Overkill for current scope. Massive UI burden.
**Effort**: High (4–6 weeks)
**Best for**: Multi-skill workforce platforms.

---

### Proposal 5: The Full Workflow Engine

**Concept**: State machine, async generation, QR codes, per-course templates.

**Pros**: Most professional.
**Cons**: Extreme overkill for ALUMCO. Requires Celery, template editor, etc.
**Effort**: High (5–8 weeks)
**Best for**: SaaS LMS providers.

---

## 4. Comparative Matrix

| Criterion | Proposal 1 (Patch) | Proposal 2 (Recommended) | Proposal 3 (Expiration) | Proposal 4 (Competency) | Proposal 5 (Workflow) |
|---|---|---|---|---|---|
| **Effort** | Low | Medium | Medium | High | High |
| **Fixes duplicate cert bug** | Yes | Yes | Yes | Yes | Yes |
| **Fixes premature cert bug** | No | Yes | Yes | Yes | Yes |
| **Class completion gating** | No | Yes | Yes | Yes | Yes |
| **Idempotent generation** | Yes | Yes | Yes | Yes | Yes |
| **Auto-approval** | Implicit | Yes | Yes | Configurable | Configurable |
| **Per-course config** | No | Yes | Yes | Yes | Yes |
| **Expiration handling** | No | No | Yes | No | Yes |
| **Dashboard expiration** | No | No | Yes | No | Yes |
| **ALUMCO fit** | Poor | **Excellent** | Good | Overkill | Overkill |
| **University feasibility** | High | **High** | Medium | Low | Low |

---

## 5. Recommended Path — Proposal 2 with Expiration Fields

### Rationale

1. **Fixes the critical bug**: Idempotent, gated generation prevents duplicate/premature certificates.
2. **Theory-first, skills-focused**: Auto-approval is appropriate for elderly-care training (not medical licensure).
3. **Per-course flexibility**: Some courses may not require certs (`certificado_activo=False`).
4. **Dashboard-only expiration**: No email infrastructure needed. Simple `fecha_vencimiento` display.
5. **Feasible for university project**: Can be built and tested in 1 week.

### Scope

**IN SCOPE**:
- `CertificateEligibilityService` with full criteria checking
- Signal-driven auto-generation (`post_save` on `IntentoEvaluacion` and `ClaseCompletado`)
- Idempotency guard (no duplicates)
- Per-course certificate settings
- Auto-approval (`estado='aprobado'`)
- Revocation with reason (`motivo_revocacion`)
- `fecha_vencimiento` on Certificado
- Dashboard expiration indicator
- Remove/replace `generar_certificado` batch view
- Update all tests

**OUT OF SCOPE** (defer to future):
- Email alerts
- Renewal workflow
- Competency mapping
- Template system
- Async generation
- QR codes
- Tiered approval

---

## 6. TDD-Oriented Implementation Roadmap

### Phase A: Foundation — Eligibility Engine (Days 1–3)

**Commit A1**: `test: add failing tests for CertificateEligibilityService`
- Test: All evals passed, all classes complete → eligible
- Test: All evals passed, missing class → NOT eligible
- Test: All classes complete, missing eval → NOT eligible
- Test: Already has cert → NOT eligible (idempotency)
- Test: Revoked cert → eligible (can re-earn)

**Commit A2**: `feat: implement CertificateEligibilityService`
```python
class CertificateEligibilityService:
    @staticmethod
    def check_eligibility(usuario, curso):
        # Returns (is_eligible, reasons_dict)
```

**Commit A3**: `feat: add course certificate settings to Curso model`
- `certificado_activo`, `certificado_requiere_clases`, etc.

### Phase B: Signal-Driven Auto-Generation (Days 4–5)

**Commit B1**: `feat: add post_save signal on IntentoEvaluacion`
- Calls eligibility service
- Creates `Certificado(estado='aprobado')` if eligible and no existing cert

**Commit B2**: `feat: add post_save signal on ClaseCompletado`
- Same logic — catches users who finish classes after evaluations

**Commit B3**: `test: integration tests for signal-driven generation`
- Test: Pass last evaluation + all classes done → cert created
- Test: Pass evaluation but classes missing → no cert
- Test: Complete classes but evals missing → no cert
- Test: Retry passed evaluation → no duplicate cert

### Phase C: Remove Legacy Generation (Day 6)

**Commit C1**: `refactor: remove generar_certificado and fix evaluaciones/views.py`
- Delete `generar_certificado` view
- Remove old auto-generation logic from `evaluaciones/views.py:tomar_evaluacion()`
- Update URLs

### Phase D: Revocation & Expiration (Days 7–8)

**Commit D1**: `feat: add revocation and expiration fields`
- `motivo_revocacion`, `fecha_vencimiento`

**Commit D2**: `feat: add management command for expiration`
```bash
python manage.py actualizar_vencimientos
```

### Phase E: UI Updates (Days 9–10)

**Commit E1**: `feat: update dashboard for auto-approved certs`
- Show expiration date
- Show revoked status with reason

**Commit E2**: `feat: update admin for certificate settings`
- `CursoAdmin` inline for cert settings
- `CertificadoAdmin` list filters

### Phase F: Cleanup & Regression (Day 11)

**Commit F1**: `test: full regression suite`
- `python manage.py test` — all apps
- Verify no broken URLs

---

## 7. Key Technical Decisions

### Decision: Default `estado='aprobado'`

**Rationale**: For theory-focused elderly-care training, mandatory manual approval adds friction without value. The eligibility engine (classes + evaluations) IS the quality gate.

**Implication**: `certificados_pendientes`, `aprobar_certificado`, `rechazar_certificado` views become mostly unused. They can be kept for future manual-override courses but are not in the critical path.

### Decision: Signal-Driven vs. Celery

**Rationale**: Signals run synchronously in the request/response cycle. For Kimün's scale (<100 concurrent users), this is fine. PDF generation remains lazy (on download), so signals are lightweight.

**Implication**: No new infrastructure (Celery, Redis, etc.).

### Decision: Class Completion IS Required

**Rationale**: Even theory-focused training requires engagement with all content. A user who skips the "Prevención de caídas" video but passes the quiz should not be certified.

**Implication**: `certificado_requiere_clases = True` by default. Can be overridden per course.

### Decision: Revocation is Permanent

**Rationale**: If a cert is revoked (e.g., fraud discovered), the user must re-earn it. No "reset to pending."

**Implication**: `estado='revocado'` is terminal. A new cert can be created if the user re-satisfies eligibility.

---

## 8. Testing Strategy

### Unit Tests (CertificateEligibilityService)

```python
class CertificateEligibilityServiceTests(TestCase):
    def test_eligible_when_all_complete(self): ...
    def test_not_eligible_when_missing_class(self): ...
    def test_not_eligible_when_missing_evaluation(self): ...
    def test_not_eligible_when_already_has_cert(self): ...
    def test_eligible_when_previous_cert_revoked(self): ...
    def test_not_eligible_when_course_inactive(self): ...
```

### Integration Tests (Signals)

```python
class CertificadoSignalTests(TestCase):
    def test_cert_created_on_last_evaluation_pass(self): ...
    def test_no_cert_when_classes_incomplete(self): ...
    def test_no_duplicate_cert_on_evaluation_retry(self): ...
    def test_cert_created_when_classes_completed_last(self): ...
```

### Regression Tests

```python
class CertificadoRegressionTests(TestCase):
    def test_old_generar_certificado_url_returns_404(self): ...
    def test_existing_certs_still_downloadable(self): ...
```

---

*End of plan. Awaiting confirmation to proceed to implementation.*
