# Technology Stack

**Analysis Date:** 2026-04-24

## Languages

**Primary:**
- **Python 3.14.3** — Core application language (`venv/pyvenv.cfg`)
  - Virtual environment: `venv/` (isolated, `include-system-site-packages = false`)
- **HTML/CSS/JavaScript** — Frontend templating and interactivity

## Runtime

**Environment:**
- Python 3.14.3 (`/usr/bin/python3.14`)
- Virtual environment managed manually (`venv/`)

**Package Manager:**
- `pip` (bundled with venv)
- No `requirements.txt`, `pyproject.toml`, or `Pipfile` present in repository
- Dependencies must be documented or inferred from `venv/lib/python*/site-packages/`

## Frameworks

**Core:**
- **Django 6.0.3** — Full-stack web framework (`kimun/settings.py` line 4, `venv/lib/.../django-6.0.3.dist-info`)
  - WSGI application: `kimun/wsgi.py`
  - ASGI application: `kimun/asgi.py`
  - Settings: `kimun/settings.py`
  - URL routing: `kimun/urls.py`

**Frontend:**
- **Tailwind CSS 3.x** — Utility-first CSS via CDN (`templates/base.html` line 10)
- **Alpine.js 3.x** — Lightweight reactivity via CDN (`templates/base.html` line 33)
- **Bootstrap Icons 1.11.3** — Icon font via CDN (`templates/base.html` line 12)
- **Google Fonts (Inter)** — Typography via CDN (`templates/base.html` line 17)

**Templating:**
- Django Template Language (DTL) — Server-side rendering
  - Base layout: `templates/base.html`
  - App templates: `templates/<app_name>/`

## Key Dependencies

**Critical:**
- `psycopg2-binary 2.9.11` — PostgreSQL adapter for Django ORM
- `django-ckeditor-5 0.2.20` — Rich text editor integration (`INSTALLED_APPS: 'django_ckeditor_5'`)
- `django-supabase-storage 1.0.1` — Supabase Storage backend for Django file storage (`INSTALLED_APPS: 'django_supabase_storage'`)
- `supabase 2.28.3` — Supabase Python client (auth, realtime, storage, postgrest)

**PDF & Document Generation:**
- `weasyprint 68.1` — HTML-to-PDF rendering for certificate generation (`certificados/views.py`)
- `python-docx 1.2.0` — Microsoft Word document generation

**Image Processing:**
- `pillow 12.1.1` — Image manipulation (used by CKEditor image uploads and general media handling)

**Environment & Configuration:**
- `python-dotenv 1.2.2` — Loads `.env` file into environment variables (`kimun/settings.py` line 14)

**Testing & Automation:**
- `playwright 1.58.0` — Browser automation (used in `test_visuals.py`, `find_widest.py`)

**Infrastructure:**
- `asgiref` — ASGI support for Django
- `sqlparse` — SQL formatting (Django dependency)

## Configuration

**Environment:**
- Loaded via `python-dotenv` from `.env` file at project root
- Example config provided: `.env.example`
- Key variables: `SUPABASE_DB_*`, `DEBUG`, `SECRET_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`

**Build:**
- No build step required for production
- Static files collected via `python manage.py collectstatic`
- Static root: `staticfiles/` (`STATIC_ROOT` in `kimun/settings.py`)
- Media root: `media/` (`MEDIA_ROOT`)

**Django Settings:**
- `LANGUAGE_CODE = 'es-cl'`
- `TIME_ZONE = 'America/Santiago'`
- `AUTH_USER_MODEL = 'usuarios.Usuario'` (custom user model)
- `DEBUG = True` (development default)

## Platform Requirements

**Development:**
- Python 3.10+ (README states), though venv currently uses 3.14.3
- Virtual environment activation: `source venv/bin/activate`
- Database: PostgreSQL (via Supabase connection pooler)

**Production:**
- WSGI server (e.g., Gunicorn) — not yet configured
- PostgreSQL database (Supabase hosted)
- Static/media file serving (Supabase Storage for media, local/whitenoise for static)
- No containerization (Docker) detected

---

*Stack analysis: 2026-04-24*
