# Vercel Deployment — Kimün (Staging Preview)

## TL;DR

> **Quick Summary**: Deploy the Kimün Django app from the `stable` branch to Vercel as a staging/preview environment at `kimun.vercel.app`, replacing WeasyPrint with xhtml2pdf for serverless compatibility.
>
> **Deliverables**:
> - `requirements.txt` with Python 3.12-pinned dependencies
> - `.vercelignore` excluding non-essential files
> - `vercel.json` for Django auto-detection
> - Production-safe `settings.py` (env-driven DEBUG, SECRET_KEY, ALLOWED_HOSTS)
> - ASGI/WSGI conflict resolution
> - xhtml2pdf migration (certificate PDF generation)
> - Configured Vercel environment variables
> - Deployed staging site at `kimun.vercel.app`
> - QA evidence (Playwright screenshots + curl responses)
>
> **Estimated Effort**: Medium
> **Parallel Execution**: YES — 3 waves
> **Critical Path**: Task 1 → Task 3 → Task 5 → Task 11 → Task 12-14 → F1-F4

---

## Context

### Original Request
User wants to upload their Django project (Kimün) to Vercel.

### Interview Summary
**Key Discussions**:
- **Scope**: Staging/preview environment (not production), domain `kimun.vercel.app`
- **Branch**: `stable` (QA/demostraciones)
- **PDF Strategy**: Replace WeasyPrint with xhtml2pdf — WeasyPrint needs Cairo/Pango system libs incompatible with Vercel serverless
- **Python Version**: Pin to Python 3.12 (Vercel's stable default; current venv uses 3.14.4)
- **Email**: Keep console backend (no SMTP config for staging)
- **Verification**: Agent-executed QA with Playwright (browser UI) + curl (API endpoints)

**Research Findings**:
- Vercel auto-detects Django from `manage.py`; no explicit build command needed
- Vercel auto-runs `collectstatic` when `STATIC_ROOT` is configured — do NOT add to build command
- Vercel prefers ASGI when both `WSGI_APPLICATION` and `ASGI_APPLICATION` are defined — potential conflict
- Migrations must run **locally** via `vercel env pull` + `manage.py migrate`, NOT in the Vercel build step
- 500MB bundle size limit — removing WeasyPrint helps significantly
- Supabase DB + Storage already cloud-native — ideal for Vercel

### Metis Review
**Identified Gaps** (addressed):
- **ASGI/WSGI conflict**: settings.py defines `WSGI_APPLICATION` and `asgi.py` exists. Vercel may prefer ASGI. Fix: remove ASGI from settings or ensure WSGI-only.
- **xhtml2pdf is NOT a drop-in replacement**: Templates need restructuring (flexbox → tables, SVGs → PNGs, Google Fonts → local fonts). This is a substantial task, not a library swap.
- **No collectstatic in build**: Vercel runs it automatically — must NOT duplicate.
- **Migrations not in build**: Must run locally before/after deploy.
- **Missing .vercelignore**: Need to exclude `venv/`, `db.sqlite3`, `tools/`, `docs/` from deployment bundle.

---

## Work Objectives

### Core Objective
Deploy the Kimün Django application from the `stable` branch to Vercel as a functional staging environment, with all critical code changes (security fixes, PDF replacement, ASGI resolution) made on the `stable` branch.

### Concrete Deliverables
- `requirements.txt` at project root
- `.vercelignore` at project root
- `vercel.json` at project root
- Modified `kimun/settings.py` (env-driven production settings)
- Modified `certificados/views.py` + certificate templates (xhtml2pdf migration)
- Configured Vercel project with all environment variables
- Live staging URL: `https://kimun.vercel.app`

### Definition of Done
- [ ] `python manage.py check --deploy` passes with no errors
- [ ] Vercel build succeeds (green checkmark in Vercel dashboard)
- [ ] Staging URL loads login page successfully
- [ ] Login with admin credentials works
- [ ] Certificate PDF generation works (xhtml2pdf)
- [ ] All Playwright QA scenarios pass
- [ ] All curl API scenarios pass

### Must Have
- Production-safe settings (DEBUG from env, SECRET_KEY from env, ALLOWED_HOSTS restricted)
- Vercel-compatible Python version (3.12)
- Working xhtml2pdf replacement for WeasyPrint
- All environment variables configured on Vercel
- Valid `.vercelignore`
- ASGI/WSGI conflict resolved

### Must NOT Have (Guardrails)
- WeasyPrint or any Cairo/Pango dependency in requirements.txt
- `collectstatic` in Vercel build command (Vercel auto-runs it)
- `python manage.py migrate` in build command
- Hardcoded SECRET_KEY or DEBUG=True
- Wildcard `ALLOWED_HOSTS = ['*']` in production settings
- Unused files (venv/, db.sqlite3, tools/, docs/) in the Vercel deployment bundle
- ASGI_APPLICATION defined (Vercel prefers ASGI; project is WSGI-only)

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: YES (Django test suite, Playwright for browser)
- **Automated tests**: Tests-after (run existing Django test suite after changes)
- **Framework**: Django `python manage.py test`, Playwright for browser QA, curl for API

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Frontend/UI**: Use Playwright — Navigate, interact, assert DOM, screenshot
- **API/Backend**: Use Bash (curl) — Send requests, assert status + response fields
- **Build verification**: Use Bash — `python manage.py check --deploy`

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — foundation):
├── Task 1: Generate requirements.txt [quick]
├── Task 2: Create .vercelignore [quick]
├── Task 3: Fix settings.py for production [quick]
├── Task 4: Resolve ASGI/WSGI conflict [quick]
└── Task 5: Create vercel.json [quick]

Wave 2 (After Wave 1 — code migration, MAX PARALLEL):
├── Task 6: Replace WeasyPrint with xhtml2pdf [deep]
├── Task 7: Run Django test suite + fix regressions [unspecified-high]
└── Task 8: Create env reference + verify .env.example [quick]

Wave 3 (After Wave 2 — Vercel platform + QA):
├── Task 9: Vercel project setup + env vars [quick]
├── Task 10: Deploy to Vercel [deep]
├── Task 11: Playwright QA — auth flows [visual-engineering]
├── Task 12: Playwright QA — core features [visual-engineering]
└── Task 13: curl QA — API endpoints [quick]

Wave FINAL (After ALL tasks):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high)
└── Task F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay
```

**Critical Path**: Task 1 → Task 3 → Task 5 → Task 10 → Task 11 → F1-F4 → user okay
**Parallel Speedup**: ~60% faster than sequential
**Max Concurrent**: 5 (Wave 1)

### Agent Dispatch Summary

- **Wave 1**: **5** — T1 → `quick`, T2 → `quick`, T3 → `quick`, T4 → `quick`, T5 → `quick`
- **Wave 2**: **3** — T6 → `deep`, T7 → `unspecified-high`, T8 → `quick`
- **Wave 3**: **5** — T9 → `quick`, T10 → `deep`, T11 → `visual-engineering`, T12 → `visual-engineering`, T13 → `quick`
- **FINAL**: **4** — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

---

## TODOs

- [x] 1. Generate requirements.txt (Python 3.12 compatible)

  **What to do**:
  - Activate venv: `source venv/bin/activate`
  - Run `pip freeze > requirements.txt` to capture all installed packages
  - Remove any local-path packages or editable installs (`-e` entries)
  - Pin exact versions (pip freeze already does this)
  - Verify all packages are available on PyPI (no private repos)
  - Remove WeasyPrint and its transitive deps (cairocffi, cairosvg, cssselect2, etc.) from the generated file
  - Add `xhtml2pdf>=0.2.17` as the replacement
  - Add `whitenoise>=6.0` for static file serving
  - Add `gunicorn>=22.0` for WSGI server (Vercel uses it internally)
  - Verify Python 3.12 compatibility: `pip check` (after installing xhtml2pdf instead of weasyprint)
  - Keep `python-dotenv>=1.0` (needed for local .env loading)
  - Keep `psycopg2-binary` (PostgreSQL adapter for Supabase)

  **Must NOT do**:
  - Do NOT include WeasyPrint, cairocffi, cairosvg, or any Cairo/Pango bindings
  - Do NOT include `playwright` (browser automation — not needed on server)
  - Do NOT include dev-only packages (`pytest`, coverage tools if any)
  - Do NOT pin to Python 3.14-specific package versions

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple file generation — running one pip command, editing a text file
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - N/A — straightforward task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3, 4, 5)
  - **Blocks**: Tasks 6, 7, 10 (all need requirements.txt)
  - **Blocked By**: None (can start immediately)

  **References**:
  - `venv/lib/python3.14/site-packages/` — Source of truth for current dependencies
  - `.planning/codebase/STACK.md` — Documents key dependencies and versions
  - `kimun/settings.py:87-99` — Database config uses `psycopg2-binary` + Supabase

  **Acceptance Criteria**:
  - [ ] `requirements.txt` exists at project root
  - [ ] Running `pip install -r requirements.txt` succeeds in a fresh venv with Python 3.12
  - [ ] `grep -i weasyprint requirements.txt` returns nothing (empty output)
  - [ ] `grep -i xhtml2pdf requirements.txt` returns a match
  - [ ] `grep -i whitenoise requirements.txt` returns a match
  - [ ] `grep -i gunicorn requirements.txt` returns a match

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: requirements.txt is valid and installable
    Tool: Bash
    Preconditions: Python 3.12 available on the system
    Steps:
      1. cd /home/sebacc/Documents/UDD/Ingeniería\ de\ Software/Proyecto-Kimün
      2. python3 -m venv /tmp/test-venv-vercel
      3. /tmp/test-venv-vercel/bin/pip install -r requirements.txt
      4. /tmp/test-venv-vercel/bin/pip check
    Expected Result: All packages install successfully; `pip check` reports no conflicts
    Failure Indicators: Any installation error or dependency conflict
    Evidence: .sisyphus/evidence/task-1-reqs-install.txt

  Scenario: WeasyPrint and Cairo deps are NOT in requirements.txt
    Tool: Bash
    Preconditions: requirements.txt exists
    Steps:
      1. grep -iE "weasyprint|cairocffi|cairosvg|cssselect2" requirements.txt
    Expected Result: grep returns nothing (exit code 1, no matches)
    Failure Indicators: grep finds any WeasyPrint or Cairo-related package
    Evidence: .sisyphus/evidence/task-1-no-weasyprint.txt
  ```

  **Evidence to Capture**:
  - [ ] `task-1-reqs-install.txt` — pip install output
  - [ ] `task-1-no-weasyprint.txt` — grep result (should be empty)

  **Commit**: YES
  - Message: `chore: add requirements.txt for Vercel deployment (Python 3.12, xhtml2pdf)`
  - Files: `requirements.txt`

- [x] 2. Create .vercelignore

  **What to do**:
  - Create `.vercelignore` at project root
  - Exclude: `venv/`, `db.sqlite3`, `tools/`, `.sisyphus/`, `.planning/`, `media/`, `*.pyc`, `__pycache__/`, `.env`, `.git/`
  - The `.vercelignore` syntax mirrors `.gitignore`
  - Vercel uses this to exclude files from the deployment bundle (helps stay under the 500MB limit)

  **Must NOT do**:
  - Do NOT exclude `staticfiles/` (Vercel needs this or will rebuild it)
  - Do NOT exclude `templates/` (needed by Django)
  - Do NOT exclude `static/` (source static files)
  - Do NOT exclude `manage.py` (Vercel auto-detection needs it)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single file creation with predictable content
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3, 4, 5)
  - **Blocks**: Task 10 (deployment uses it)
  - **Blocked By**: None

  **References**:
  - `.gitignore` at project root — Use same patterns where applicable
  - `venv/lib/python3.14/site-packages/` — venv directory structure confirms what to exclude
  - Vercel docs: `.vercelignore` uses same syntax as `.gitignore`

  **Acceptance Criteria**:
  - [ ] `.vercelignore` exists at project root
  - [ ] Contains exclusion for `venv/`
  - [ ] Contains exclusion for `db.sqlite3`
  - [ ] Contains exclusion for `tools/`
  - [ ] Contains exclusion for `.sisyphus/`
  - [ ] Contains exclusion for `.planning/`
  - [ ] Contains exclusion for `media/`
  - [ ] Contains exclusion for `*.pyc` and `__pycache__/`
  - [ ] Contains exclusion for `.env`

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: .vercelignore exists with required exclusions
    Tool: Bash
    Preconditions: .vercelignore has been created
    Steps:
      1. test -f .vercelignore && echo "EXISTS" || echo "MISSING"
      2. grep -q "^venv/" .vercelignore && echo "venv OK" || echo "venv MISSING"
      3. grep -q "db.sqlite3" .vercelignore && echo "sqlite OK" || echo "sqlite MISSING"
      4. grep -q "tools/" .vercelignore && echo "tools OK" || echo "tools MISSING"
      5. grep -q ".sisyphus/" .vercelignore && echo "sisyphus OK" || echo "sisyphus MISSING"
    Expected Result: All checks pass (EXISTS + all OK)
    Failure Indicators: Missing file or missing any exclusion pattern
    Evidence: .sisyphus/evidence/task-2-vercelignore-check.txt
  ```

  **Evidence to Capture**:
  - [ ] `task-2-vercelignore-check.txt` — validation output

  **Commit**: YES (groups with Task 1)
  - Message: `chore: add .vercelignore to exclude dev files from Vercel bundle`
  - Files: `.vercelignore`

- [x] 3. Fix settings.py for production deployment

  **What to do**:
  - Change `DEBUG = True` to `DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'`
  - Change `SECRET_KEY` from hardcoded string to `SECRET_KEY = os.environ.get('SECRET_KEY')` (with fallback for local dev only)
  - Change `ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']` to env-driven: 
    ```python
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
    ```
    Also include Vercel preview URL patterns: `.vercel.app` in the env var
  - Add `CSRF_TRUSTED_ORIGINS` to include Vercel domains from env:
    ```python
    CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://127.0.0.1:8000,http://localhost:8000').split(',')
    ```
  - Add production security settings conditionally:
    ```python
    if not DEBUG:
        SECURE_SSL_REDIRECT = True
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True
        SECURE_HSTS_SECONDS = 31536000
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True
    ```
  - Keep `load_dotenv()` at the top for local development (Vercel uses real env vars, not .env file)

  **Must NOT do**:
  - Do NOT remove `load_dotenv()` — it's harmless on Vercel and essential for local dev
  - Do NOT hardcode the Vercel domain — use env vars for flexibility
  - Do NOT enable `SECURE_SSL_REDIRECT` in DEBUG mode (breaks local dev)
  - Do NOT remove `STATIC_ROOT` or `STATIC_URL` settings

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single file edit with well-known Django production patterns
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 4, 5)
  - **Blocks**: Task 10 (deployment)
  - **Blocked By**: None

  **References**:
  - `kimun/settings.py:22-33` — Current DEBUG, SECRET_KEY, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS
  - `.env.example:10-12` — Shows DEBUG and SECRET_KEY as env vars
  - Django deployment checklist: `python manage.py check --deploy`

  **Acceptance Criteria**:
  - [ ] `DEBUG` reads from `os.environ.get('DEBUG', 'False').lower() == 'true'`
  - [ ] `SECRET_KEY` reads from `os.environ.get('SECRET_KEY')`
  - [ ] `ALLOWED_HOSTS` reads from env var (comma-separated)
  - [ ] `CSRF_TRUSTED_ORIGINS` reads from env var (comma-separated)
  - [ ] `python manage.py check --deploy` produces no errors (only warnings are acceptable)

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: DEBUG is false by default (production-safe)
    Tool: Bash
    Preconditions: No .env file loaded with DEBUG=True, or .env has DEBUG=False
    Steps:
      1. cd project root
      2. UNSET DEBUG env var
      3. python -c "import os; os.environ['SECRET_KEY']='test'; os.environ['ALLOWED_HOSTS']='*'; os.environ.setdefault('DJANGO_SETTINGS_MODULE','kimun.settings'); from django.conf import settings; print('DEBUG=', settings.DEBUG)"
    Expected Result: Prints "DEBUG= False"
    Failure Indicators: Prints "DEBUG= True"
    Evidence: .sisyphus/evidence/task-3-debug-false.txt

  Scenario: Production security settings activated when DEBUG=False
    Tool: Bash
    Preconditions: DEBUG=False environment
    Steps:
      1. python -c "import os; os.environ['DEBUG']='False'; os.environ['SECRET_KEY']='test'; os.environ['ALLOWED_HOSTS']='test.vercel.app'; os.environ.setdefault('DJANGO_SETTINGS_MODULE','kimun.settings'); from django.conf import settings; print('SECURE_SSL_REDIRECT=', getattr(settings, 'SECURE_SSL_REDIRECT', 'NOT SET')); print('CSRF_COOKIE_SECURE=', getattr(settings, 'CSRF_COOKIE_SECURE', 'NOT SET'))"
    Expected Result: Both print True when DEBUG is False
    Failure Indicators: Prints False or 'NOT SET'
    Evidence: .sisyphus/evidence/task-3-security-settings.txt
  ```

  **Evidence to Capture**:
  - [ ] `task-3-debug-false.txt` — DEBUG verification
  - [ ] `task-3-security-settings.txt` — Security settings verification

  **Commit**: YES (groups with Task 1)
  - Message: `fix(settings): make DEBUG, SECRET_KEY, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS env-driven`
  - Files: `kimun/settings.py`

- [x] 4. Resolve ASGI/WSGI conflict

  **What to do**:
  - Check if `ASGI_APPLICATION` is explicitly defined in `kimun/settings.py`
  - If defined: remove it (project is WSGI-only, no async features)
  - If not defined but asgi.py exists: Vercel may still try to use ASGI. Add explicit `ASGI_APPLICATION = None` or ensure only WSGI is set
  - Verify `WSGI_APPLICATION = 'kimun.wsgi.application'` remains set
  - Verify `wsgi.py` correctly exposes an `application` variable (it does — `get_wsgi_application()`)
  - Run `python manage.py check` to verify no ASGI-related issues

  **Must NOT do**:
  - Do NOT delete `asgi.py` — it may be needed for future async features
  - Do NOT change `WSGI_APPLICATION` value

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Check one config line, potentially remove one line
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 3, 5)
  - **Blocks**: Task 10 (deployment — Vercel auto-detection)
  - **Blocked By**: None

  **References**:
  - `kimun/settings.py:84` — `WSGI_APPLICATION = 'kimun.wsgi.application'`
  - `kimun/asgi.py` — ASGI entrypoint (exists but not used)
  - Vercel docs: prefers ASGI when both are defined → must ensure WSGI-only

  **Acceptance Criteria**:
  - [ ] `grep "ASGI_APPLICATION" kimun/settings.py` returns nothing OR returns a None/empty value
  - [ ] `grep "WSGI_APPLICATION" kimun/settings.py` returns `WSGI_APPLICATION = 'kimun.wsgi.application'`
  - [ ] `python manage.py check` passes with no errors

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Only WSGI_APPLICATION is set (ASGI not configured)
    Tool: Bash
    Preconditions: settings.py has been modified
    Steps:
      1. python -c "
  import os
  os.environ['SECRET_KEY']='test'
  os.environ['ALLOWED_HOSTS']='*'
  os.environ.setdefault('DJANGO_SETTINGS_MODULE','kimun.settings')
  from django.conf import settings
  wsgi = getattr(settings, 'WSGI_APPLICATION', 'NOT SET')
  asgi = getattr(settings, 'ASGI_APPLICATION', 'NOT SET')
  print(f'WSGI={wsgi}')
  print(f'ASGI={asgi}')
  "
    Expected Result: WSGI shows 'kimun.wsgi.application', ASGI shows 'NOT SET' or None
    Failure Indicators: ASGI shows a configured application path
    Evidence: .sisyphus/evidence/task-4-asgi-check.txt
  ```

  **Evidence to Capture**:
  - [ ] `task-4-asgi-check.txt` — ASGI/WSGI config verification

  **Commit**: YES (groups with Task 1)
  - Message: `fix(settings): ensure WSGI-only config for Vercel (remove ASGI_APPLICATION)`
  - Files: `kimun/settings.py`

- [x] 5. Create vercel.json

  **What to do**:
  - Create `vercel.json` at project root with the following structure:
    ```json
    {
      "$schema": "https://openapi.vercel.sh/vercel.json",
      "framework": "django",
      "buildCommand": "pip install -r requirements.txt",
      "functions": {
        "api/**/*.py": {
          "maxDuration": 30,
          "memory": 3009
        }
      },
      "rewrites": [
        { "source": "/(.*)", "destination": "/api" }
      ],
      "env": {
        "DEBUG": "False",
        "PYTHON_VERSION": "3.12"
      }
    }
    ```
  - The `$schema` provides IDE autocompletion
  - `framework: "django"` explicitly tells Vercel to use Django detection
  - `buildCommand` installs dependencies (Vercel auto-runs collectstatic separately)
  - `functions.maxDuration: 30` allows time for xhtml2pdf generation (Hobby plan max is 10s, but Pro plan supports up to 300s)
  - Note: Vercel auto-detects Django from manage.py, so this config is mostly explicit overrides

  **Must NOT do**:
  - Do NOT include `collectstatic` in buildCommand (Vercel auto-runs it)
  - Do NOT include `python manage.py migrate` in buildCommand (must run locally)
  - Do NOT include `python manage.py createsuperuser` in buildCommand
  - Do NOT hardcode any secrets (use Vercel dashboard env vars instead)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single JSON file creation with known structure
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 3, 4)
  - **Blocks**: Task 10 (deployment)
  - **Blocked By**: None

  **References**:
  - Vercel Django docs: auto-detects Django from manage.py, WSGI_APPLICATION
  - `kimun/settings.py:84,128-134` — WSGI_APPLICATION, STATIC_ROOT, STATIC_URL
  - `manage.py` — Entry point for Vercel auto-detection

  **Acceptance Criteria**:
  - [ ] `vercel.json` exists at project root
  - [ ] Valid JSON: `python -c "import json; json.load(open('vercel.json')); print('PASS')"` prints PASS
  - [ ] `framework` is set to `"django"`
  - [ ] `buildCommand` does NOT contain "collectstatic"
  - [ ] `buildCommand` does NOT contain "migrate"
  - [ ] `functions` config exists with maxDuration >= 10

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: vercel.json is valid JSON with required fields
    Tool: Bash
    Preconditions: vercel.json exists
    Steps:
      1. python -c "
  import json
  v = json.load(open('vercel.json'))
  assert v.get('framework') == 'django', 'Missing/incorrect framework'
  bc = v.get('buildCommand', '')
  assert 'collectstatic' not in bc, 'collectstatic found in buildCommand'
  assert 'migrate' not in bc, 'migrate found in buildCommand'
  print('PASS: vercel.json is valid')
  "
    Expected Result: Prints "PASS: vercel.json is valid"
    Failure Indicators: AssertionError with message
    Evidence: .sisyphus/evidence/task-5-vercel-json-valid.txt

  Scenario: vercel.json has function configuration
    Tool: Bash
    Preconditions: vercel.json exists
    Steps:
      1. python -c "
  import json
  v = json.load(open('vercel.json'))
  funcs = v.get('functions', {})
  assert funcs, 'No functions configured'
  for key, cfg in funcs.items():
      print(f'{key}: maxDuration={cfg.get(\"maxDuration\", \"default\")}, memory={cfg.get(\"memory\", \"default\")}')
  "
    Expected Result: Shows function config with maxDuration and memory
    Failure Indicators: No functions key or empty functions
    Evidence: .sisyphus/evidence/task-5-vercel-functions.txt
  ```

  **Evidence to Capture**:
  - [ ] `task-5-vercel-json-valid.txt` — JSON validation
  - [ ] `task-5-vercel-functions.txt` — Function config verification

  **Commit**: YES (groups with Task 1)
  - Message: `chore: add vercel.json for Django deployment`
  - Files: `vercel.json`

- [x] 6. Replace WeasyPrint with xhtml2pdf for certificate PDF generation

  **What to do**:
  - Read the current certificate generation code in `certificados/views.py` to understand the full flow
  - Read the certificate HTML template to understand what CSS/layout is used
  - Replace `import weasyprint` with `from xhtml2pdf import pisa`
  - **Critical**: xhtml2pdf does NOT support Flexbox, CSS Grid, CSS transforms, Google Fonts, or SVG images. Certificate templates must be restructured:
    - Replace flexbox layouts with table-based or block layouts
    - Replace CSS `transform: rotate()` or similar with static positioning
    - Replace Google Fonts references with system fonts or locally-hosted fonts
    - Replace SVG images with PNG/JPG versions (xhtml2pdf has limited SVG support)
    - Replace any CSS `position: absolute` patterns with table/inline-block approaches
    - Use inline CSS styles (xhtml2pdf works best with inline or `<style>` blocks, NOT external stylesheets)
  - Update the PDF generation function to use `pisa.CreatePDF()` instead of WeasyPrint's API
  - The xhtml2pdf API pattern:
    ```python
    from xhtml2pdf import pisa
    from django.template.loader import render_to_string
    from django.http import HttpResponse
    
    html = render_to_string('certificados/certificado_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificado.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response
    ```
  - Add `@login_required` decorator or verify auth on PDF view
  - Test the PDF generation locally: `python manage.py runserver` and navigate to a certificate URL

  **Must NOT do**:
  - Do NOT leave any WeasyPrint import or usage
  - Do NOT use Flexbox, CSS Grid, CSS transforms in the certificate template
  - Do NOT reference Google Fonts in the template (use system fonts: Helvetica, Arial, 'DejaVu Sans')
  - Do NOT use external CSS files in the PDF template (inline styles only)
  - Do NOT use SVG elements (convert to PNG)
  - Do NOT change the certificate data logic — only change the rendering

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Complex refactoring involving template redesign for a different rendering engine. Requires understanding of both WeasyPrint and xhtml2pdf APIs, CSS-to-PDF rendering differences, and PDF layout constraints.
  - **Skills**: []
  - **Skills Evaluated but Omitted**:
    - N/A — Django refactoring task

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 7, 8)
  - **Blocks**: Task 11, 12 (QA scenarios verify certificate generation)
  - **Blocked By**: Task 1 (needs xhtml2pdf in requirements.txt)

  **References**:
  - `certificados/views.py` — Current WeasyPrint-based PDF generation code
  - `certificados/templates/certificados/` — Certificate HTML templates (find exact path)
  - `kimun/settings.py:157-180` — CKEditor 5 config (file upload handling)
  - `kimun/settings.py:136-137` — MEDIA_URL and MEDIA_ROOT
  - xhtml2pdf docs: `https://xhtml2pdf.readthedocs.io/` — API reference for `pisa.CreatePDF()`

  **Acceptance Criteria**:
  - [ ] No WeasyPrint import in `certificados/views.py`
  - [ ] xhtml2pdf import present: `from xhtml2pdf import pisa`
  - [ ] Certificate PDF generation returns a valid PDF (not a 500 error)
  - [ ] Generated PDF opens correctly in a PDF viewer
  - [ ] Certificate content (name, course, date, verification code) is visible in the PDF
  - [ ] `grep -r "weasyprint" certificados/` returns nothing

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Certificate PDF endpoint returns a valid PDF
    Tool: Bash (curl)
    Preconditions: Django dev server running at localhost:8000, user authenticated
    Steps:
      1. Login via curl to get session cookie:
         curl -c /tmp/cookies.txt -X POST http://127.0.0.1:8000/usuarios/login/ \
           -d "username=admin&password=admin123" -H "Content-Type: application/x-www-form-urlencoded"
      2. Request a certificate PDF (find a valid certificate ID first via admin or shell):
         curl -b /tmp/cookies.txt http://127.0.0.1:8000/certificados/1/pdf/ \
           -o /tmp/test-cert.pdf -w "%{http_code}" -s
      3. file /tmp/test-cert.pdf
    Expected Result: HTTP 200, `file` command reports "PDF document"
    Failure Indicators: HTTP 500, empty file, or `file` reports "HTML document" (error page)
    Evidence: .sisyphus/evidence/task-6-cert-pdf-valid.txt

  Scenario: No WeasyPrint references remain in certificados app
    Tool: Bash
    Preconditions: Code changes committed
    Steps:
      1. grep -r "weasyprint" certificados/ --include="*.py"
      2. echo "Exit code: $?"
    Expected Result: No matches found (exit code 1)
    Failure Indicators: Any WeasyPrint reference found (exit code 0)
    Evidence: .sisyphus/evidence/task-6-no-weasyprint-refs.txt
  ```

  **Evidence to Capture**:
  - [ ] `task-6-cert-pdf-valid.txt` — PDF validity check output
  - [ ] `task-6-no-weasyprint-refs.txt` — grep result (should be empty)

  **Commit**: YES (separate)
  - Message: `refactor(certificados): replace WeasyPrint with xhtml2pdf for Vercel compatibility`
  - Files: `certificados/views.py`, `certificados/templates/certificados/*.html`, `requirements.txt` (if added here)

- [x] 7. Run Django test suite and fix regressions

  **What to do**:
  - Run the existing Django test suite: `python manage.py test`
  - Identify any failing tests related to:
    - Certificate PDF generation (xhtml2pdf may produce different output)
    - Settings changes (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
    - Database connection (psycopg2 on Supabase)
  - Fix any test regressions caused by the settings.py changes
  - If certificate PDF tests fail due to the WeasyPrint→xhtml2pdf migration, update test assertions to match new PDF format
  - Run `python manage.py check --deploy` and address any warnings

  **Must NOT do**:
  - Do NOT delete failing tests — fix them or update assertions
  - Do NOT skip the test suite — run ALL tests
  - Do NOT change test logic to make tests pass without verifying behavior

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Running test suite, analyzing failures, fixing regressions. Requires Django testing knowledge.
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 6, 8)
  - **Blocks**: Task 10 (deployment — tests must pass before deploy)
  - **Blocked By**: Tasks 1, 3, 4, 6 (depends on requirements, settings, and code changes)

  **References**:
  - `.planning/codebase/TESTING.md` — Documents ~4,462 test lines across 8 apps
  - `certificados/tests.py` — Certificate-specific tests
  - `kimun/settings.py` — Settings that may affect test behavior
  - `certificados/views.py` — Code under test

  **Acceptance Criteria**:
  - [ ] `python manage.py test` runs with zero failures
  - [ ] `python manage.py check --deploy` produces no errors
  - [ ] Certificate-related tests pass with xhtml2pdf

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Django test suite passes with zero failures
    Tool: Bash
    Preconditions: All code changes completed, virtual environment active
    Steps:
      1. source venv/bin/activate
      2. python manage.py test --verbosity=2 2>&1 | tee /tmp/test-output.txt
      3. grep -E "FAIL:|ERROR:" /tmp/test-output.txt ; echo "Failures: $?"
    Expected Result: Exit code from grep is 1 (no FAIL or ERROR lines)
    Failure Indicators: Any FAIL or ERROR in test output
    Evidence: .sisyphus/evidence/task-7-test-output.txt

  Scenario: Django deployment check passes
    Tool: Bash
    Preconditions: Settings modified for production
    Steps:
      1. python manage.py check --deploy 2>&1
    Expected Result: No errors (warnings are acceptable for staging)
    Failure Indicators: Any ERROR-level messages
    Evidence: .sisyphus/evidence/task-7-deploy-check.txt
  ```

  **Evidence to Capture**:
  - [ ] `task-7-test-output.txt` — Full test suite output
  - [ ] `task-7-deploy-check.txt` — Django deploy check output

  **Commit**: YES (groups with Task 6 or separate)
  - Message: `test: verify all tests pass after WeasyPrint→xhtml2pdf migration and settings changes`
  - Files: Any modified test files or settings

- [x] 8. Create environment variable reference and verify .env.example

  **What to do**:
  - Update `.env.example` to include ALL required environment variables for Vercel:
    ```env
    # Supabase Database Configuration
    SUPABASE_DB_NAME=postgres
    SUPABASE_DB_USER=postgres.oyeqwhdljbqibcpmkdqt
    SUPABASE_DB_PASSWORD=your_database_password_here
    SUPABASE_DB_HOST=aws-1-us-east-2.pooler.supabase.com
    SUPABASE_DB_PORT=5432

    # Django Settings (for Vercel deployment)
    DEBUG=False
    SECRET_KEY=generate-a-random-secret-key-here-min-50-chars
    ALLOWED_HOSTS=kimun.vercel.app,*.vercel.app
    CSRF_TRUSTED_ORIGINS=https://kimun.vercel.app

    # Supabase Storage (for media files)
    SUPABASE_URL=https://oyeqwhdljbqibcpmkdqt.supabase.co
    SUPABASE_KEY=your_anon_key_here
    ```
  - Verify the existing `.env` file contains all the same keys (for local dev)
  - Create a note in the README or a separate `VERCEL.md` documenting:
    - How to set up Vercel deployment
    - Required environment variables
    - How to run migrations (locally via `vercel env pull`)
    - Known limitations (WeasyPrint replaced, no background workers)

  **Must NOT do**:
  - Do NOT put real secrets in .env.example (keep placeholder values)
  - Do NOT commit .env file (it's in .gitignore)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Updating a template file with known env vars
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 6, 7)
  - **Blocks**: Task 9 (Vercel env var setup uses this as reference)
  - **Blocked By**: Task 3 (settings.py changes define what env vars are needed)

  **References**:
  - `.env.example:1-16` — Current env example (incomplete for production)
  - `kimun/settings.py:87-99,145-155` — Database and Supabase config
  - `.env` — Current local env values (for reference, not to copy secrets)

  **Acceptance Criteria**:
  - [ ] `.env.example` contains: SUPABASE_DB_NAME, SUPABASE_DB_USER, SUPABASE_DB_PASSWORD, SUPABASE_DB_HOST, SUPABASE_DB_PORT
  - [ ] `.env.example` contains: DEBUG, SECRET_KEY, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS
  - [ ] `.env.example` contains: SUPABASE_URL, SUPABASE_KEY
  - [ ] All values are placeholders (not real secrets)

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: .env.example has all required keys for Vercel deployment
    Tool: Bash
    Preconditions: .env.example updated
    Steps:
      1. for key in SUPABASE_DB_NAME SUPABASE_DB_USER SUPABASE_DB_PASSWORD SUPABASE_DB_HOST SUPABASE_DB_PORT DEBUG SECRET_KEY ALLOWED_HOSTS CSRF_TRUSTED_ORIGINS SUPABASE_URL SUPABASE_KEY; do
           grep -q "^$key=" .env.example && echo "$key: FOUND" || echo "$key: MISSING"
         done
    Expected Result: All 11 keys show "FOUND"
    Failure Indicators: Any key shows "MISSING"
    Evidence: .sisyphus/evidence/task-8-env-keys.txt
  ```

  **Evidence to Capture**:
  - [ ] `task-8-env-keys.txt` — Environment variable key validation

  **Commit**: YES (groups with Task 7)
  - Message: `docs: update .env.example with all Vercel-required environment variables`
  - Files: `.env.example`

- [x] 9. Set up Vercel project and configure environment variables

  **What to do**:
  - Install Vercel CLI: `npm install -g vercel` (or use `npx vercel` without global install)
  - Run `vercel login` and authenticate with Vercel account
  - Checkout the `stable` branch: `git checkout stable`
  - Run `vercel link` in the project directory to link to an existing Vercel project (or create new)
  - Run `vercel env pull` to pull any existing env vars to `.env.vercel.local` for local testing
  - Configure environment variables via Vercel dashboard or CLI:
    ```bash
    # Database
    vercel env add SUPABASE_DB_NAME production
    vercel env add SUPABASE_DB_USER production
    vercel env add SUPABASE_DB_PASSWORD production  # will prompt for value
    vercel env add SUPABASE_DB_HOST production
    vercel env add SUPABASE_DB_PORT production
    
    # Django
    vercel env add DEBUG production
    vercel env add SECRET_KEY production          # will prompt for value
    vercel env add ALLOWED_HOSTS production        # value: kimun.vercel.app,*.vercel.app
    vercel env add CSRF_TRUSTED_ORIGINS production  # value: https://kimun.vercel.app
    
    # Supabase Storage
    vercel env add SUPABASE_URL production
    vercel env add SUPABASE_KEY production         # will prompt for value
    ```
  - Set env for preview/staging as well (same values)
  - Ensure GitHub integration is connected in Vercel dashboard (repo: `SebaGRT/Kimun`)
  - Configure the deployment to watch the `stable` branch

  **Must NOT do**:
  - Do NOT commit the `.env.vercel.local` file (add to .gitignore)
  - Do NOT set DEBUG=True on Vercel (staging can use True, but prefer False)
  - Do NOT use the hardcoded SECRET_KEY from settings.py — generate a new one

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: CLI commands and dashboard configuration, well-documented steps
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (Vercel project setup depends on all prior tasks)
  - **Parallel Group**: Wave 3 (sequential with Task 10, parallel with Task 11-13 after Task 10)
  - **Blocks**: Task 10 (deployment needs project ready)
  - **Blocked By**: Tasks 1-8 (all code changes must be committed and pushed first)

  **References**:
  - `vercel.json` — Project configuration
  - `.env.example` — Environment variable key reference
  - `.env` — Current local values for Supabase credentials
  - `requirements.txt` — Vercel reads this during build

  **Acceptance Criteria**:
  - [ ] `vercel link` confirms project is linked
  - [ ] All 11 environment variables configured on Vercel
  - [ ] GitHub integration shows `SebaGRT/Kimun` connected
  - [ ] `stable` branch is configured for automatic deployment

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Vercel project is linked and env vars are configured
    Tool: Bash (vercel CLI)
    Preconditions: vercel CLI installed and authenticated
    Steps:
      1. vercel env ls 2>&1 | head -30
      2. vercel project ls 2>&1
    Expected Result: Shows linked project info and list of environment variables
    Failure Indicators: "Error: No project linked" or empty env list
    Evidence: .sisyphus/evidence/task-9-vercel-env.txt
  ```

  **Evidence to Capture**:
  - [ ] `task-9-vercel-env.txt` — vercel env ls output

  **Commit**: NO (platform configuration, not code)

- [ ] 10. Deploy to Vercel

  **What to do**:
  - Ensure all code changes are committed and pushed to the `stable` branch on GitHub
  - Push to trigger deployment (or run `vercel --prod` for manual deploy)
  - Wait for Vercel build to complete — monitor the Vercel dashboard or CLI
  - If build fails:
    - Read the build logs to identify the error
    - Common issues: missing requirements.txt, Python version mismatch, missing env vars, package install failure
    - Fix the issue, commit, push again
  - Once build succeeds:
    - Run `vercel env pull` to verify env vars are accessible
    - Run `python manage.py migrate` LOCALLY pointing to the Supabase DB (already set up)
    - If migrations are already applied to the Supabase DB, this is a no-op
  - Verify the deployment URL (should be `kimun.vercel.app` or similar)
  - Test the live URL in a browser: navigate to the login page
  - Verify static files are served (CSS, JS, images load correctly)

  **Must NOT do**:
  - Do NOT run `python manage.py migrate` as part of the Vercel build
  - Do NOT deploy from a branch other than `stable`
  - Do NOT merge to `main` before confirming staging works

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Deployment troubleshooting may require log analysis, debugging build failures, and iterative fixes
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (after Task 9, before Tasks 11-13)
  - **Blocks**: Tasks 11, 12, 13 (QA runs against deployed URL)
  - **Blocked By**: Tasks 1-9 (all prior work must be done)

  **References**:
  - `vercel.json` — Deployment configuration
  - `requirements.txt` — Dependencies for build
  - `kimun/settings.py` — Production settings (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
  - Vercel dashboard: build logs, deployment URL

  **Acceptance Criteria**:
  - [ ] Vercel build succeeds (green checkmark)
  - [ ] Deployment URL resolves and loads the login page
  - [ ] Static files (CSS, JS, images) load correctly
  - [ ] Login form appears and is functional
  - [ ] No console errors (404 on static files, 500 on API calls)

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Deployed staging URL loads the login page
    Tool: Bash (curl) + Playwright
    Preconditions: Deployment completed, VERCEL_URL known
    Steps:
      1. curl -sL https://kimun.vercel.app/ -o /tmp/index.html -w "HTTP %{http_code}"
      2. grep -q "login" /tmp/index.html && echo "Login form found" || echo "Login form MISSING"
      3. grep -q "stylesheet" /tmp/index.html && echo "CSS references found" || echo "CSS MISSING"
    Expected Result: HTTP 200, login form found, CSS references found
    Failure Indicators: HTTP 500, empty page, missing CSS/form
    Evidence: .sisyphus/evidence/task-10-deploy-landing.txt

  Scenario: Vercel build logs show success
    Tool: Bash (vercel CLI)
    Preconditions: Deployment completed
    Steps:
      1. vercel logs --limit 50 2>&1 | tail -30
    Expected Result: Shows build completion with no errors
    Failure Indicators: Error messages in build logs
    Evidence: .sisyphus/evidence/task-10-build-logs.txt
  ```

  **Evidence to Capture**:
  - [ ] `task-10-deploy-landing.txt` — Landing page check
  - [ ] `task-10-build-logs.txt` — Vercel build logs

  **Commit**: NO (deployment step, not code)

- [ ] 11. Playwright QA — Authentication flows

  **What to do**:
  - Use Playwright to verify authentication on the deployed staging URL
  - Test scenarios:
    1. **Login success**: Navigate to `https://kimun.vercel.app/usuarios/login/`, fill credentials (admin/admin123), submit, verify redirect to dashboard
    2. **Login failure**: Submit invalid credentials, verify error message appears
    3. **Logout**: After login, click logout, verify redirect to login page
    4. **Protected routes**: Attempt to access `/cursos/` while logged out, verify redirect to login
  - Capture screenshots at each step
  - Save evidence to `.sisyphus/evidence/`

  **Must NOT do**:
  - Do NOT test against localhost — use the actual Vercel staging URL
  - Do NOT run tests without waiting for page loads (use `waitForLoadState` and proper timeouts)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: Browser automation with Playwright — navigating, filling forms, asserting DOM state, capturing screenshots
  - **Skills**: [`playwright`]
    - `playwright`: Required for browser automation — login forms, navigation, DOM assertions
  - **Skills Evaluated but Omitted**:
    - N/A

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 12, 13 — all against deployed URL)
  - **Blocks**: None
  - **Blocked By**: Task 10 (needs deployed URL to test against)

  **References**:
  - `usuarios/views.py` — Login view logic
  - `kimun/settings.py:139-141` — LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
  - README.md:55-57 — Test credentials (admin/admin123)
  - Deployed staging URL: `https://kimun.vercel.app`

  **Acceptance Criteria**:
  - [ ] Login with valid credentials succeeds (redirect to dashboard)
  - [ ] Login with invalid credentials shows error message
  - [ ] Logout works and redirects to login
  - [ ] Protected routes redirect to login when unauthenticated

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Login success with valid credentials
    Tool: Playwright
    Preconditions: Staging URL is live
    Steps:
      1. Navigate to https://kimun.vercel.app/usuarios/login/
      2. Wait for page load (waitForLoadState: 'networkidle', timeout: 15s)
      3. Fill input[name="username"] with "admin"
      4. Fill input[name="password"] with "admin123"
      5. Click button[type="submit"]
      6. Wait for navigation (timeout: 15s)
      7. Assert URL does NOT contain "/login"
      8. Assert page contains text "Inicio" or "Dashboard" or user's name
      9. Take screenshot: login-success.png
    Expected Result: Redirected away from login page, dashboard content visible
    Failure Indicators: Still on login page, error message shown, timeout on navigation
    Evidence: .sisyphus/evidence/task-11-login-success.png

  Scenario: Login failure with invalid credentials
    Tool: Playwright
    Preconditions: Staging URL is live
    Steps:
      1. Navigate to https://kimun.vercel.app/usuarios/login/
      2. Fill input[name="username"] with "fakeuser"
      3. Fill input[name="password"] with "wrongpass"
      4. Click button[type="submit"]
      5. Wait for page load (timeout: 10s)
      6. Assert URL still contains "/login" (stayed on login page)
      7. Assert page contains an error message (text containing "incorrect" or "inválido" or "error" — case insensitive)
      8. Take screenshot: login-failure.png
    Expected Result: Stayed on login page, error message visible
    Failure Indicators: Redirected away (unexpected success), no error message, page crash
    Evidence: .sisyphus/evidence/task-11-login-failure.png

  Scenario: Logout redirects to login
    Tool: Playwright
    Preconditions: Already logged in (continue from login success scenario)
    Steps:
      1. Click on logout link/button (look for text "Cerrar sesión", "Salir", "Logout", or link containing "logout")
      2. Wait for navigation (timeout: 10s)
      3. Assert URL contains "/login" or "/accounts/login"
      4. Take screenshot: logout-redirect.png
    Expected Result: Redirected to login page
    Failure Indicators: Still on dashboard, stayed on same page, 404/500 error
    Evidence: .sisyphus/evidence/task-11-logout-redirect.png

  Scenario: Protected route redirects when unauthenticated
    Tool: Playwright
    Preconditions: Logged out (clear cookies)
    Steps:
      1. Clear browser cookies/storage
      2. Navigate to https://kimun.vercel.app/cursos/
      3. Wait for navigation (timeout: 10s)
      4. Assert URL contains "/login" (redirected to login)
      5. Take screenshot: protected-redirect.png
    Expected Result: Redirected to login page
    Failure Indicators: Access granted without login (shows courses page — security vulnerability!)
    Evidence: .sisyphus/evidence/task-11-protected-redirect.png
  ```

  **Evidence to Capture**:
  - [ ] `task-11-login-success.png` — Successful login screenshot
  - [ ] `task-11-login-failure.png` — Failed login screenshot
  - [ ] `task-11-logout-redirect.png` — After logout screenshot
  - [ ] `task-11-protected-redirect.png` — Unauthenticated redirect screenshot

  **Commit**: NO (QA evidence, not code)

- [ ] 12. Playwright QA — Core features

  **What to do**:
  - Use Playwright to verify core functionality on the deployed staging URL
  - Test scenarios:
    1. **Dashboard renders**: After login, verify the dashboard shows role-appropriate content
    2. **Course listing**: Navigate to `/cursos/`, verify course cards/table renders
    3. **Certificate listing**: Navigate to `/certificados/`, verify certificates page loads
    4. **Certificate PDF download**: Navigate to a certificate detail page, trigger PDF download, verify the downloaded file is a valid PDF
    5. **Dark mode toggle**: Click dark mode toggle, verify theme changes
    6. **Navigation**: Click through main nav items, verify no 500 errors
  - Capture screenshots at each key step
  - Report any broken pages (500 errors, missing templates, broken CSS)

  **Must NOT do**:
  - Do NOT test against localhost
  - Do NOT skip the certificate PDF download test — this validates the xhtml2pdf migration

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: Browser automation verifying UI rendering, navigation, and PDF downloads
  - **Skills**: [`playwright`]
    - `playwright`: Browser automation — multi-page navigation, form interaction, screenshot capture
  - **Skills Evaluated but Omitted**:
    - N/A

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 11, 13)
  - **Blocks**: None
  - **Blocked By**: Task 10 (needs deployed URL)

  **References**:
  - `cursos/views.py` — Course views and templates
  - `certificados/views.py` — Certificate views (test xhtml2pdf output)
  - `templates/base.html` — Dark mode implementation (data-theme="dark")
  - `kimun/urls.py` — URL routing structure
  - Deployed staging URL: `https://kimun.vercel.app`

  **Acceptance Criteria**:
  - [ ] Dashboard loads without errors after login
  - [ ] Course listing page loads and displays content
  - [ ] Certificate listing page loads without errors
  - [ ] Certificate PDF download returns a valid PDF file
  - [ ] Dark mode toggle works
  - [ ] All main nav links load without 500 errors

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Dashboard renders after login
    Tool: Playwright
    Preconditions: Authenticated session from Task 11
    Steps:
      1. After login, assert page title contains "Kimün" or "Inicio"
      2. Assert there is visible content (not a blank page)
      3. Check for navigation elements (.sidebar, nav, or header menu)
      4. Take screenshot: dashboard.png
    Expected Result: Dashboard page with content and navigation
    Failure Indicators: Blank page, 500 error, no navigation
    Evidence: .sisyphus/evidence/task-12-dashboard.png

  Scenario: Course listing page loads
    Tool: Playwright
    Preconditions: Authenticated
    Steps:
      1. Navigate to https://kimun.vercel.app/cursos/
      2. Wait for load (timeout: 15s)
      3. Assert HTTP status is 200 (or page doesn't show 500/404 text)
      4. Assert page contains course-related content (table rows, cards, or "curso" text)
      5. Take screenshot: cursos.png
    Expected Result: Courses page with content loaded
    Failure Indicators: 500 error page, 404, blank page
    Evidence: .sisyphus/evidence/task-12-cursos.png

  Scenario: Certificate PDF downloads as valid PDF
    Tool: Playwright
    Preconditions: Authenticated, at least one certificate exists
    Steps:
      1. Navigate to https://kimun.vercel.app/certificados/
      2. Wait for load (timeout: 10s)
      3. If certificate list is empty, skip with note
      4. Find first certificate link/button
      5. Click to trigger PDF download
      6. Wait for download event (timeout: 15s)
      7. Verify downloaded file is a valid PDF (check file starts with %PDF-1.)
      8. Take screenshot: certificados-list.png
    Expected Result: PDF file downloaded and valid
    Failure Indicators: No certificate links, download fails, file is not PDF (HTML error page)
    Evidence: .sisyphus/evidence/task-12-cert-pdf-download.png, task-12-cert-pdf-valid.txt

  Scenario: Dark mode toggle works
    Tool: Playwright
    Preconditions: Page loaded
    Steps:
      1. Find dark mode toggle (button or switch — look for aria-label with "dark" or "theme", or a sun/moon icon)
      2. Check current state: document.documentElement.getAttribute('data-theme')
      3. Click the toggle
      4. Assert data-theme attribute changed (from dark→light or light→dark)
      5. Take screenshot: dark-mode.png
    Expected Result: Theme attribute changes after toggle click
    Failure Indicators: No toggle found, toggle doesn't change theme, CSS not applied
    Evidence: .sisyphus/evidence/task-12-dark-mode.png
  ```

  **Evidence to Capture**:
  - [ ] `task-12-dashboard.png` — Dashboard screenshot
  - [ ] `task-12-cursos.png` — Course listing screenshot
  - [ ] `task-12-cert-pdf-download.png` — Certificate page screenshot
  - [ ] `task-12-cert-pdf-valid.txt` — PDF validity check
  - [ ] `task-12-dark-mode.png` — Dark mode screenshot

  **Commit**: NO (QA evidence only)

- [ ] 13. curl QA — API endpoint verification

  **What to do**:
  - Use curl to verify backend endpoints on the deployed staging URL
  - Test scenarios:
    1. **Login API**: POST to `/usuarios/login/` with valid credentials, verify session cookie is set
    2. **CSRF protection**: Verify CSRF token is present in login form (GET request)
    3. **Static files**: GET common static files (`/static/css/kimun.css`), verify they are served with correct MIME type
    4. **Health check**: GET `/` (root), verify HTTP 200
    5. **Admin panel**: GET `/admin/`, verify it redirects to login (HTTP 302)
    6. **Security headers**: Check for `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options` headers
  - Save response headers and bodies as evidence

  **Must NOT do**:
  - Do NOT test POST endpoints without CSRF token (expected to fail — that's a pass)
  - Do NOT test with wrong credentials expecting success

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: curl commands sending HTTP requests, parsing responses — well-defined, predictable
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 11, 12)
  - **Blocks**: None
  - **Blocked By**: Task 10 (needs deployed URL)

  **References**:
  - `kimun/settings.py:55-64` — MIDDLEWARE (SecurityMiddleware, CsrfViewMiddleware)
  - `kimun/settings.py:128-134` — STATIC_URL and STATIC_ROOT
  - `kimun/urls.py` — URL patterns
  - Deployed staging URL: `https://kimun.vercel.app`

  **Acceptance Criteria**:
  - [ ] Login POST returns HTTP 302 (redirect) with session cookie
  - [ ] Login page GET returns HTTP 200 with CSRF token in form
  - [ ] Static CSS file returns HTTP 200 with `text/css` Content-Type
  - [ ] Root URL returns HTTP 200
  - [ ] /admin/ returns HTTP 302 (redirects to login)
  - [ ] Security headers present (at minimum: X-Content-Type-Options)

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Login endpoint accepts valid credentials
    Tool: Bash (curl)
    Preconditions: Staging URL is live
    Steps:
      1. curl -v -c /tmp/qa-cookies.txt -X POST https://kimun.vercel.app/usuarios/login/ \
           -d "username=admin&password=admin123" \
           -H "Content-Type: application/x-www-form-urlencoded" \
           -o /tmp/login-response.html -w "HTTP %{http_code}" 2>&1 | tee /tmp/login-headers.txt
      2. grep "Set-Cookie" /tmp/login-headers.txt && echo "COOKIE SET" || echo "NO COOKIE"
      3. grep "HTTP 302\|HTTP 301" /tmp/login-headers.txt && echo "REDIRECT" || echo "NO REDIRECT"
    Expected Result: HTTP 302/301 redirect, Set-Cookie header present
    Failure Indicators: HTTP 200 (stayed on page), HTTP 500, no Set-Cookie
    Evidence: .sisyphus/evidence/task-13-login-api.txt

  Scenario: Login page has CSRF token
    Tool: Bash (curl)
    Preconditions: Staging URL is live
    Steps:
      1. curl -s https://kimun.vercel.app/usuarios/login/ | grep -o 'csrfmiddlewaretoken' | head -1
    Expected Result: Output contains "csrfmiddlewaretoken"
    Failure Indicators: Empty output (no CSRF token in form)
    Evidence: .sisyphus/evidence/task-13-csrf-token.txt

  Scenario: Static CSS file is served correctly
    Tool: Bash (curl)
    Preconditions: Staging URL is live
    Steps:
      1. curl -sI https://kimun.vercel.app/static/css/kimun.css 2>&1 | head -15
      2. Check for HTTP 200 and Content-Type: text/css
    Expected Result: HTTP 200, Content-Type contains "text/css"
    Failure Indicators: HTTP 404, HTTP 500, wrong Content-Type
    Evidence: .sisyphus/evidence/task-13-static-css.txt

  Scenario: Security headers are present
    Tool: Bash (curl)
    Preconditions: Staging URL is live
    Steps:
      1. curl -sI https://kimun.vercel.app/ 2>&1 | grep -iE "strict-transport|x-content-type|x-frame|content-security"
      2. echo "---"
      3. curl -sI https://kimun.vercel.app/ 2>&1 | grep -i "x-content-type"
    Expected Result: At minimum, X-Content-Type-Options header present
    Failure Indicators: No security headers at all
    Evidence: .sisyphus/evidence/task-13-security-headers.txt
  ```

  **Evidence to Capture**:
  - [ ] `task-13-login-api.txt` — Login API response
  - [ ] `task-13-csrf-token.txt` — CSRF token check
  - [ ] `task-13-static-css.txt` — Static file serving check
  - [ ] `task-13-security-headers.txt` — Security headers check

  **Commit**: NO (QA evidence only)

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists. For each "Must NOT Have": search codebase for forbidden patterns. Check evidence files exist in `.sisyphus/evidence/`. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `python -m django check --deploy`. Review all changed files for hardcoded secrets, `DEBUG=True`, wildcard hosts. Check AI slop. Verify `requirements.txt` has no WeasyPrint.
  Output: `Django Check [PASS/FAIL] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high` (+ `playwright` skill)
  Start from clean state. Execute EVERY QA scenario from Tasks 11-13. Test cross-feature integration. Test edge cases: invalid login, empty states, certificate generation.
  Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff. Verify 1:1 match. Check "Must NOT do" compliance. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **Wave 1** (all quick tasks): Single commit on `stable` — `chore(vercel): add deployment config and production settings`
- **Wave 2 Task 6**: Separate commit — `refactor(certificados): replace WeasyPrint with xhtml2pdf`
- **Wave 2 Tasks 7-8**: Commit with T6 or separate — `chore: verify tests and update env reference`

---

## Success Criteria

### Verification Commands
```bash
# Verify settings are production-safe
python manage.py check --deploy

# Verify WeasyPrint is not in dependencies
grep -i weasyprint requirements.txt && echo "FAIL" || echo "PASS"

# Verify vercel.json is valid JSON
python -c "import json; json.load(open('vercel.json')); print('PASS')"

# Verify Vercel build succeeds (via Vercel dashboard or CLI)
# Green checkmark = PASS
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] Django check --deploy passes
- [ ] Vercel build succeeds
- [ ] Staging URL loads
- [ ] Certificate PDF generation works via xhtml2pdf
- [ ] All QA scenarios pass
