# Codebase Concerns

**Analysis Date:** 2026-04-24

## Tech Debt

### Hardcoded Django SECRET_KEY
- **Issue:** `SECRET_KEY` is hardcoded in `settings.py` with a known insecure prefix (`django-insecure-`)
- **Files:** `kimun/settings.py` (line 23)
- **Impact:** Session forgery, password reset token forgery, any cryptographic signing in Django becomes trivially breakable if source code leaks
- **Fix approach:** Load from environment variable; rotate the key immediately in production

### DEBUG Enabled in Production Configuration
- **Issue:** `DEBUG = True` is set unconditionally in `settings.py`
- **Files:** `kimun/settings.py` (line 26)
- **Impact:** Full stack traces exposed to end users, static/media file serving inefficiencies, potential security information leakage
- **Fix approach:** `DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'`

### Wildcard ALLOWED_HOSTS
- **Issue:** `ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']` includes a wildcard
- **Files:** `kimun/settings.py` (line 28)
- **Impact:** Host header attacks, cache poisoning, password reset link poisoning
- **Fix approach:** Restrict to actual production domains; use environment variable

### Raw POST Handling for Authentication
- **Issue:** Login view reads `username` and `password` directly from `request.POST` instead of using `AuthenticationForm`
- **Files:** `usuarios/views.py` (lines 42-43)
- **Impact:** No built-in CSRF protection verification on the form level, no rate limiting, no account lockout, susceptible to brute force
- **Fix approach:** Use Django's built-in `AuthenticationForm` and `LoginView`; add `django-ratelimit` or `axes`

### Inline Permission Checks (Duplicated Logic)
- **Issue:** Despite having reusable decorators (`admin_required`, `docente_or_admin_required`, `course_owner_or_admin`, `owner_or_admin`), many views still perform inline `request.user.rol` checks. This creates drift risk where permission logic diverges.
- **Files:** 
  - `cursos/views.py` (lines 114-120, 160-162, 301-307, 315-317, 370-376, 382-384)
  - `usuarios/views.py` (lines 68, 85, 90, 125, 133, 141)
  - `evaluaciones/views.py` (line 351)
  - `anuncios/views.py` (lines 14-15, 28-29)
- **Impact:** Maintenance burden, inconsistent authorization behavior, easy to miss edge cases
- **Fix approach:** Replace all inline checks with centralized decorators or use Django's built-in permission system

### Hardcoded Cargo/Role Mappings
- **Issue:** Lists of `colaborador_cargos`, `admin_cargos`, `docente_cargos` are duplicated verbatim in `usuario_create` and `usuario_edit`
- **Files:** `usuarios/views.py` (lines 238-256 and 283-301)
- **Impact:** Any change to role mappings requires editing both views; risk of inconsistency
- **Fix approach:** Extract to a constant in `usuarios/constants.py` or model method

### Console Email Backend
- **Issue:** `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` means all emails (notifications, reminders, certificate notifications) are printed to stdout and never sent
- **Files:** `kimun/settings.py` (line 143)
- **Impact:** Users never receive enrollment notifications, deadline reminders, or certificate alerts
- **Fix approach:** Configure SMTP or transactional email service (SendGrid, AWS SES) via environment variables

## Known Bugs

### Session-Based Evaluation Timer Not Multi-Server Safe
- **Symptoms:** Evaluation timer uses `request.session` to store `hora_inicio` and `preguntas_seleccionadas`
- **Files:** `evaluaciones/views.py` (lines 220-248, 269-273)
- **Trigger:** If the app runs on multiple servers behind a load balancer without sticky sessions, a user could refresh and get a different server with a fresh session, resetting or corrupting their timer/question subset
- **Workaround:** Use a database-backed session store or store attempt state in the `IntentoEvaluacion` model immediately on GET

### Lazy PDF Generation Race Condition
- **Symptoms:** Certificate PDF is generated on first download inside the request/response cycle
- **Files:** `certificados/views.py` (lines 68-84)
- **Trigger:** Two simultaneous download requests for the same uncached certificate could race, causing one to fail or corrupt the `archivo_pdf` field
- **Workaround:** Generate PDF in a background task (Celery, Django-Q) or use `select_for_update()` around the generation block

### Missing `unique_together` on `Evaluacion` Questions
- **Symptoms:** `Pregunta` model has no uniqueness constraint on `(evaluacion, orden)`, allowing duplicate question ordering
- **Files:** `evaluaciones/models.py` (lines 37-47)
- **Trigger:** Two questions with the same `orden` can be created for the same evaluation
- **Fix approach:** Add `ordering` Meta option and optionally a `UniqueConstraint` if ordering uniqueness is required

## Security Considerations

### File Upload Extension-Only Validation
- **Risk:** `MaterialForm.clean()` validates file types by extension only (`nombre.endswith('.pdf')`), not MIME type or file content
- **Files:** `cursos/forms.py` (lines 88-95)
- **Current mitigation:** File extension whitelist
- **Recommendations:** Add `python-magic` content-type validation; store uploads outside web root; use `django-supabase-storage` for all file types (currently only default storage is Supabase)

### No Content Security Policy (CSP)
- **Risk:** XSS attacks via CKEditor 5 rich content, user-uploaded files, or third-party scripts
- **Files:** `kimun/settings.py`
- **Current mitigation:** None
- **Recommendations:** Add `django-csp` middleware and configure strict CSP headers

### Missing Security Headers
- **Risk:** Clickjacking, MIME-type sniffing, XSS
- **Files:** `kimun/settings.py`
- **Current mitigation:** `SecurityMiddleware` and `XFrameOptionsMiddleware` are installed but no `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `SECURE_BROWSER_XSS_FILTER`, or `SESSION_COOKIE_SECURE`
- **Recommendations:** Add production security settings:
  ```python
  SECURE_SSL_REDIRECT = True
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  SECURE_HSTS_SECONDS = 31536000
  SECURE_HSTS_INCLUDE_SUBDOMAINS = True
  SECURE_HSTS_PRELOAD = True
  ```

### CKEditor 5 Image Upload Path
- **Risk:** CKEditor 5 upload endpoint (`ckeditor5/image_upload/`) is exposed at project root and delegates to `upload_file` without additional file type or size validation beyond the library defaults
- **Files:** `kimun/urls.py` (line 19), `cursos/views.py` (lines 15-19)
- **Current mitigation:** `@docente_or_admin_required` decorator restricts access
- **Recommendations:** Add file type whitelist and virus scanning for uploaded images

### Certificate Verification Page Leak
- **Risk:** `verificar_certificado` view is publicly accessible (no `@login_required`) and reveals full certificate details including user name, course, and status
- **Files:** `certificados/views.py` (lines 102-113)
- **Current mitigation:** UUID is unguessable
- **Recommendations:** Consider rate limiting this endpoint to prevent UUID enumeration

## Performance Bottlenecks

### N+1 Queries in Course Detail
- **Problem:** `curso_detail` loops over all classes and queries `ClaseCompletado` individually per class
- **Files:** `cursos/views.py` (lines 127-136)
- **Cause:** `ClaseCompletado.objects.filter(usuario=request.user, clase=clase).exists()` inside a `for` loop
- **Improvement path:** Use `prefetch_related` or annotate with a `Count`/`Exists` subquery:
  ```python
  clases_completadas_ids = set(ClaseCompletado.objects.filter(
      usuario=request.user, clase__in=clases
  ).values_list('clase_id', flat=True))
  ```

### N+1 Queries in Evaluation List
- **Problem:** `evaluacion_list` iterates evaluations and counts attempts per user in Python
- **Files:** `evaluaciones/views.py` (lines 44-46)
- **Cause:** `evaluacion.intentos.filter(usuario=request.user).count()` inside a loop
- **Improvement path:** Annotate with `Count` filtered by user using `Count(..., filter=Q(...))`

### Synchronous PDF Generation
- **Problem:** WeasyPrint blocks the Django worker thread during PDF rendering
- **Files:** `certificados/views.py` (line 80)
- **Cause:** `HTML(string=html_string).write_pdf()` is CPU-intensive and synchronous
- **Improvement path:** Offload to Celery, RQ, or Django-Q; return 202 Accepted with polling/download URL

### Dashboard Report Heavy Computation
- **Problem:** `get_at_risk_students()` performs many queries and Python-side set operations
- **Files:** `reportes/views.py` (lines 15-95)
- **Cause:** Multiple ORM queries, `values_list`, set constructions, and date arithmetic per enrollment
- **Improvement path:** Materialize as a daily management command; cache result in Redis/Memcached

## Fragile Areas

### JSON-Based Question Storage in Evaluations
- **Files:** `evaluaciones/views.py` (lines 65, 124, 263, 436)
- **Why fragile:** Evaluation questions and answers are transmitted as raw JSON strings in `request.POST`. Any malformed JSON causes a 500 error unless caught. The `validar_preguntas` function has broad exception handling but still allows partial data corruption.
- **Safe modification:** Always wrap `json.loads` in try/except and return form errors; consider using Django formsets for structured question data

### Signal-Driven Certificate Auto-Creation
- **Files:** `certificados/signals.py`, `usuarios/signals.py`
- **Why fragile:** Multiple signals (`post_save` on `IntentoEvaluacion` and `ClaseCompletado`) can fire simultaneously. The eligibility check uses `.exclude(estado='revocado')` but does not lock the row, creating a potential race condition for duplicate certificate creation under high concurrency.
- **Safe modification:** Use `get_or_create` with a unique constraint or `select_for_update` in the signal handler
- **Test coverage:** Tests exist but mock signals manually; no concurrency tests

### Owner Resolution via String Splitting
- **Files:** `usuarios/decorators.py` (lines 73-78)
- **Why fragile:** The `owner_or_admin` decorator resolves nested attributes via `owner_field.split('.')` and `getattr`. If an intermediate attribute is `None`, it silently falls through to the 403 response without logging, making debugging difficult.
- **Safe modification:** Add explicit logging or raise a more descriptive exception

## Scaling Limits

### Session Store
- **Current capacity:** Default database-backed sessions (implied by no `SESSION_ENGINE` override)
- **Limit:** Database becomes a bottleneck with many concurrent users; session table grows unbounded
- **Scaling path:** Switch to `django.contrib.sessions.backends.cache` with Redis

### File Storage
- **Current capacity:** Uses `django_supabase_storage.SupabaseMediaStorage` for default storage but still defines `MEDIA_ROOT` locally
- **Limit:** Local `MEDIA_ROOT` is used in DEBUG mode for serving files, which won't scale beyond a single server
- **Scaling path:** Ensure all uploads go to Supabase; remove local media serving in production

### Database Connection Pool
- **Current capacity:** Default Django connection handling (no `CONN_MAX_AGE`, no `django-db-connection-pool`)
- **Limit:** PostgreSQL connection overhead under load; Supabase connection limits may be hit
- **Scaling path:** Enable persistent connections (`CONN_MAX_AGE=60`) or use PgBouncer

## Dependencies at Risk

### django-supabase-storage
- **Risk:** Relatively new third-party package; limited community adoption and long-term maintenance track record
- **Impact:** File uploads break if package becomes incompatible with future Django/Supabase versions
- **Migration plan:** Monitor for updates; consider wrapping storage backend to allow fallback to S3-compatible API

### WeasyPrint
- **Risk:** Heavy system-level dependencies (GTK, Pango, Cairo) that can break during OS upgrades or container rebuilds
- **Impact:** Certificate generation fails entirely if system libraries are missing
- **Migration plan:** Containerize with pinned base image; evaluate `playwright` + headless Chrome or `pdfkit` as alternatives

### django-ckeditor-5
- **Risk:** CKEditor 5 is a large JS dependency; upload functionality has historically had security issues in various editor versions
- **Impact:** XSS via malicious image uploads or crafted HTML content
- **Migration plan:** Keep package updated; implement HTML sanitization on output (e.g., `bleach` or `nh3`)

## Missing Critical Features

### Rate Limiting / Brute Force Protection
- **Problem:** No rate limiting on login, certificate verification, or evaluation attempts
- **Blocks:** Secure public deployment
- **Priority:** High

### REST API / Mobile Support
- **Problem:** All interactions require server-side template rendering; no DRF or API layer
- **Blocks:** Mobile app, third-party integrations, SPA frontend
- **Priority:** Medium

### Background Task Queue
- **Problem:** PDF generation, bulk email sending, and report generation happen synchronously in the request cycle
- **Blocks:** Responsive UX under load
- **Priority:** Medium

### HTML Sanitization
- **Problem:** CKEditor 5 content is stored and rendered without sanitization; `|safe` filter is likely used in templates
- **Blocks:** Protection against stored XSS from compromised teacher accounts
- **Priority:** High

## Test Coverage Gaps

### Concurrency / Race Conditions
- **What's not tested:** Simultaneous certificate downloads, concurrent evaluation submissions, double class completion clicks
- **Files:** `certificados/views.py`, `evaluaciones/views.py`, `cursos/views.py`
- **Risk:** Data corruption, duplicate records, inconsistent state
- **Priority:** High

### Permission Edge Cases
- **What's not tested:** Decorator behavior when `pk` parameter is missing or malformed; decorator behavior with non-integer `pk` values
- **Files:** `usuarios/decorators.py`
- **Risk:** Information disclosure or unauthorized access via URL manipulation
- **Priority:** Medium

### Form Validation Extremes
- **What's not tested:** File uploads with forged extensions but malicious content; very large JSON payloads in evaluation question data
- **Files:** `cursos/forms.py`, `evaluaciones/views.py`
- **Risk:** Server-side DoS or file storage abuse
- **Priority:** Medium

### Database Constraint Enforcement
- **What's not tested:** Some models rely on Python-level validation rather than database constraints (e.g., `Pregunta.orden` uniqueness, `Evaluacion` ordering)
- **Files:** `evaluaciones/models.py`
- **Risk:** Data integrity violations under concurrent writes
- **Priority:** Medium

---

*Concerns audit: 2026-04-24*
