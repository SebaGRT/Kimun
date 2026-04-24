# External Integrations

**Analysis Date:** 2026-04-24

## APIs & External Services

**Supabase:**
- **Purpose:** Primary external backend — database hosting and file storage
- **SDK/Client:** `supabase` Python package (v2.28.3), `django-supabase-storage` (v1.0.1)
- **Auth:** Service-level — uses project URL + anon/service key
- **Environment Variables:**
  - `SUPABASE_URL` — Project API URL
  - `SUPABASE_KEY` — Anonymous or service role key

**CKEditor 5 (via django-ckeditor-5):**
- **Purpose:** Rich text WYSIWYG editor for course content, announcements, and materials
- **SDK:** `django-ckeditor-5` (v0.2.20)
- **Features configured:** Heading, bold, italic, underline, strikethrough, links, lists, blockquotes, image upload, undo/redo
- **Image upload:** Authenticated users only (`CKEDITOR_5_FILE_UPLOAD_PERMISSION = 'authenticated'`)
- **Max file size:** 5 MB (`CKEDITOR_5_MAX_FILE_SIZE = 5`)
- **Custom upload view:** `cursos.views.ckeditor5_upload_restricted` (`kimun/urls.py` line 19)

## Data Storage

**Databases:**
- **PostgreSQL (Supabase hosted)**
  - Connection: Via Supabase connection pooler (`aws-1-us-east-2.pooler.supabase.com`)
  - Driver: `psycopg2-binary` 2.9.11
  - SSL: Required (`sslmode: 'require'`)
  - Database name: `postgres` (default)
  - Configuration in `kimun/settings.py` lines 87–99
  - Environment variables:
    - `SUPABASE_DB_NAME`
    - `SUPABASE_DB_USER`
    - `SUPABASE_DB_PASSWORD`
    - `SUPABASE_DB_HOST`
    - `SUPABASE_DB_PORT` (default 5432)

**File Storage:**
- **Supabase Storage** — Default Django storage backend for user-uploaded media files
  - Backend class: `django_supabase_storage.SupabaseMediaStorage`
  - Configured in `kimun/settings.py` lines 148–155 (`STORAGES['default']`)
  - Used for: CKEditor image uploads, course materials, user avatars, certificates
- **Local filesystem** — Static files (CSS, JS, images)
  - Backend: `django.contrib.staticfiles.storage.StaticFilesStorage`
  - Collected to: `staticfiles/`

**Caching:**
- Not detected — no Redis, Memcached, or database caching configured

## Authentication & Identity

**Auth Provider:**
- **Django built-in authentication** (custom user model)
  - Custom user model: `usuarios.Usuario` (`AUTH_USER_MODEL` in `kimun/settings.py` line 126)
  - Extends `AbstractUser`
  - Roles: `admin`, `docente`, `colaborador`
  - No OAuth, SSO, or external identity provider integration detected

**Session Management:**
- Django session middleware (`django.contrib.sessions`)
- CSRF protection enabled (`django.middleware.csrf.CsrfViewMiddleware`)

## Monitoring & Observability

**Error Tracking:**
- Not configured — no Sentry, Rollbar, or similar service detected

**Logs:**
- Django console logging (default)
- Custom audit middleware: `usuarios.middleware.AuditoriaMiddleware` (`kimun/settings.py` line 64)

## CI/CD & Deployment

**Hosting:**
- Not configured — development server only (`python manage.py runserver`)

**CI Pipeline:**
- Not detected — no GitHub Actions, GitLab CI, or similar configuration files

## Environment Configuration

**Required env vars:**
| Variable | Purpose | Required By |
|----------|---------|-------------|
| `SUPABASE_DB_USER` | Database username | `kimun/settings.py` |
| `SUPABASE_DB_PASSWORD` | Database password | `kimun/settings.py` |
| `SUPABASE_DB_HOST` | Database host | `kimun/settings.py` |
| `SUPABASE_DB_PORT` | Database port (default: 5432) | `kimun/settings.py` |
| `SUPABASE_DB_NAME` | Database name (default: postgres) | `kimun/settings.py` |
| `DEBUG` | Django debug mode | `kimun/settings.py` |
| `SECRET_KEY` | Django cryptographic signing | `kimun/settings.py` |
| `SUPABASE_URL` | Supabase project URL | `kimun/settings.py` (storage) |
| `SUPABASE_KEY` | Supabase API key | `kimun/settings.py` (storage) |

**Secrets location:**
- `.env` file at project root (loaded via `python-dotenv`)
- `.env.example` provides template (no real values committed)
- **CRITICAL:** `SECRET_KEY` is hardcoded in `kimun/settings.py` line 23 — must be moved to environment variable for production

## Email Backend

**Current Configuration:**
- Backend: `django.core.mail.backends.console.EmailBackend`
- All emails printed to console (development only)

**Email Use Cases:**
- Course enrollment notifications (`usuarios/utils.py:notificar_inscripcion`)
- Certificate award notifications (`usuarios/utils.py:notificar_certificado`)
- Announcement broadcasts (`anuncios/management/commands/enviar_anuncios.py`)
- Reminder emails (`usuarios/utils.py`)

**Production Migration Path:**
- Switch to `django.core.mail.backends.smtp.EmailBackend`
- Recommended provider: Gmail SMTP (documented in `README.md` lines 122–131)
- Required vars: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`

## Webhooks & Callbacks

**Incoming:**
- None detected

**Outgoing:**
- None detected — no third-party webhooks or callback URLs configured

## File Storage Setup Details

**Supabase Storage Configuration:**
```python
# kimun/settings.py
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

STORAGES = {
    'default': {
        'BACKEND': 'django_supabase_storage.SupabaseMediaStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}
```

**Media Handling:**
- `MEDIA_URL = 'media/'`
- `MEDIA_ROOT = BASE_DIR / 'media'` (fallback for local dev)
- In debug mode, Django serves media files directly (`kimun/urls.py` lines 23–25)

---

*Integration audit: 2026-04-24*
