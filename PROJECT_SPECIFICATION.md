# Kimün Training Platform - Technical Specification

## Project Overview

**Kimün** is a Django-based Learning Management System (LMS) designed for first aid training (Primeros Auxilios) for an NGO. The platform manages courses, users, evaluations, certificates, and progress tracking.

**Tech Stack:**
- **Framework:** Django 6.0.3
- **Database:** SQLite (development), PostgreSQL (production-ready)
- **Frontend:** Django Templates + TailwindCSS
- **Rich Text:** django-ckeditor (CKEditor 4)
- **Authentication:** Custom User model with role-based access

---

## Architecture

### Project Structure
```
kimun/
├── kimun/                 # Project settings & URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── cursos/               # Courses, classes, materials
├── usuarios/             # Users, authentication, roles
├── evaluaciones/         # Quizzes, questions, attempts
├── certificados/         # Certificate generation
├── reportes/             # Dashboard & reporting
├── templates/            # Shared templates
├── static/               # CSS, JS, images
└── manage.py
```

### Django Apps

#### 1. `cursos` - Course Management
**Models:**
- `Categoria` - Course categories with colors
- `Curso` - Courses with published/draft status, deadlines
- `Material` - PDF files and video URLs
- `InscripcionCurso` - User enrollments with status tracking
- `Clase` - Ordered lessons with rich text content (CKEditor)
- `ClaseCompletado` - User completion records per class

**Key Features:**
- Sequential class unlock (must complete N-1 before N)
- Progress tracking per user
- Bulk enrollment via CSV
- Course categories with filtering

#### 2. `usuarios` - User Management
**Models:**
- `Usuario` (extends AbstractUser) - Custom user with RUT, roles
- `AreaCargo` - Job positions/departments
- `Recordatorio` - Course deadline reminders

**Roles:**
- `admin` - Full system access
- `docente` - Can create/manage own courses
- `colaborador` - Can enroll and complete courses

**Key Features:**
- RUT (Chilean ID) validation
- Password change workflows
- User profile with activity timeline
- Bulk user enrollment

#### 3. `evaluaciones` - Assessment System
**Models:**
- `Evaluacion` - Course evaluations with passing percentage
- `Pregunta` - Questions linked to evaluations
- `Alternativa` - Multiple choice answers
- `IntentoEvaluacion` - User attempt records with scoring

**Key Features:**
- Automatic scoring
- HTMX-powered correctness checking
- Evaluation required for course completion
- Pass/fail status tracking

#### 4. `certificados` - Certificate Management
**Models:**
- `Certificado` - Certificates with UUID verification codes

**Key Features:**
- PDF generation (ReportLab)
- UUID-based verification
- Download functionality
- Admin and personal certificate lists

#### 5. `reportes` - Reporting & Analytics
**Views:**
- Dashboard with statistics
- Course-level reports (enrollments, completions)
- User-level reports (progress, certificates)

---

## Data Models (Simplified)

### Core Relationships

```
Usuario (1) ───< (N) InscripcionCurso >─── (1) Curso
                          │
                          ├──< (N) ClaseCompletado >─── (N) Clase
                          │                              │
                          │                              └──< (N) Material
                          │
                          ├──< (N) IntentoEvaluacion >─── (N) Evaluacion
                          │                                 │
                          │                                 └──< (N) Pregunta >───< (N) Alternativa
                          │
                          └──< (N) Certificado

Curso (1) ───< (N) Categoria
```

### Key Constraints
- `InscripcionCurso`: unique_together [usuario, curso]
- `Clase`: unique_together [curso, orden] + check orden >= 1
- `ClaseCompletado`: unique_together [usuario, clase]
- `Certificado`: UUID unique verification code

---

## Current Features

### Implemented ✅

**Course Management:**
- [x] Course CRUD (create, read, update, delete)
- [x] Published/Draft status
- [x] Course categories with colors
- [x] Course deadlines with reminders
- [x] PDF and video materials
- [x] Sequential class completion (unlock N after N-1)
- [x] Progress tracking dashboard
- [x] Bulk enrollment via CSV

**User Management:**
- [x] Custom authentication (RUT-based)
- [x] Role-based access (admin, docente, colaborador)
- [x] User profiles with activity timeline
- [x] Password management
- [x] Bulk user creation

**Learning Content:**
- [x] Rich text classes (CKEditor)
- [x] Ordered lesson sequencing
- [x] Class completion tracking
- [x] Material downloads

**Assessments:**
- [x] Evaluation CRUD
- [x] Multiple choice questions
- [x] Automatic scoring
- [x] Pass/fail determination
- [x] HTMX correctness feedback
- [x] Evaluation required for completion

**Certificates:**
- [x] PDF certificate generation
- [x] UUID verification codes
- [x] Certificate verification page
- [x] Download functionality

**Reporting:**
- [x] Admin dashboard
- [x] Course statistics
- [x] User progress reports

---

## Technical Debt & Gaps

### Architecture Issues
1. **Duplicated Permission Checks** - 62 inline `request.user.rol` checks across views
2. **Raw POST Handling** - 30+ views use raw `request.POST.get()` instead of ModelForms
3. **No Test Coverage** - All `tests.py` files are empty
4. **Scattered Progress Logic** - Progress computed inline in views (N+1 queries)

### Missing Features
1. **Evaluation Enhancements** - No attempt limits, timers, or question randomization
2. **Automatic Certificates** - Manual generation only (no auto-issuance on completion)
3. **Audit Logging** - No tracking of who did what
4. **API Layer** - No REST API for mobile/frontend apps

---

## URL Structure

### Main Routes
```
/                           # Home page
/admin/                     # Django Admin

/cursos/                    # Course list
/cursos/<pk>/               # Course detail
/cursos/<pk>/clases/        # Class list
/cursos/clases/<pk>/        # Class detail
/cursos/<pk>/inscribir/     # Enroll users

/usuarios/                  # User management
/usuarios/perfil/           # User profile
/usuarios/login/            # Authentication
/usuarios/logout/           # Logout

/evaluaciones/              # Evaluation list
/evaluaciones/<pk>/         # Take evaluation
/evaluaciones/<pk>/resultado/  # Results

/certificados/              # My certificates
/certificados/verificar/    # Verification page

/reportes/                  # Dashboard
```

---

## Security Model

### Role Permissions

| Feature | Admin | Docente | Colaborador |
|---------|-------|---------|-------------|
| Create courses | ✅ | ✅ (own only) | ❌ |
| Edit courses | ✅ | ✅ (own only) | ❌ |
| Delete courses | ✅ | ✅ (own only) | ❌ |
| Enroll users | ✅ | ✅ (own courses) | ❌ |
| View courses | ✅ | ✅ | ✅ (enrolled) |
| Complete classes | ❌ | ❌ | ✅ |
| Take evaluations | ❌ | ❌ | ✅ |
| View certificates | ✅ | ✅ | ✅ (own) |

### Current Implementation
- Manual checks in each view: `if request.user.rol not in ['admin', 'docente']`
- No centralized permission system
- Course ownership checked via `curso.docente_creador == request.user`

---

## Key Technologies

### Django Packages
- `django-ckeditor` - Rich text editing
- `django-crispy-forms` - Form rendering (partially used)
- `reportlab` - PDF generation
- `openpyxl` - Excel export for reports

### Frontend
- TailwindCSS (via CDN)
- Bootstrap Icons
- HTMX for dynamic interactions
- Vanilla JavaScript

### External Services
- None currently (email via Django console backend)

---

## File Inventory

### Models (4 files)
- `cursos/models.py` - 161 lines, 6 models
- `usuarios/models.py` - 68 lines, 3 models
- `evaluaciones/models.py` - 55 lines, 4 models
- `certificados/models.py` - 22 lines, 1 model

### Views (5 files)
- `cursos/views.py` - ~530 lines
- `usuarios/views.py` - ~400 lines
- `evaluaciones/views.py` - ~300 lines
- `certificados/views.py` - ~200 lines
- `reportes/views.py` - ~150 lines

### Templates (~25 files)
- Base templates: `base.html`, `base_admin.html`
- Course templates: 7 files
- User templates: 5 files
- Evaluation templates: 4 files
- Certificate templates: 3 files
- Report templates: 2 files

---

## Development Roadmap

### Priority 1: RBAC Decorators 🔐
Extract 62 permission checks into reusable decorators

### Priority 2: ModelForm Validation 📝
Replace raw POST with proper ModelForms

### Priority 3: Test Suite 🧪
Build comprehensive test coverage

### Priority 4: Evaluation Engine ⏱️
Add timers, attempt limits, randomization

### Priority 5: Auto Certificates 📜
Auto-issue on course completion

### Priority 6: Progress Model 📊
Unified progress tracking

### Priority 7: Audit Logging 🔍
Track all significant actions

---

## Database Schema Notes

### Key Tables
- `cursos_curso` - Courses
- `cursos_clase` - Classes (lessons)
- `cursos_inscripcioncurso` - Enrollments
- `cursos_clasecompletado` - Class completions
- `usuarios_usuario` - Users (custom auth)
- `evaluaciones_evaluacion` - Evaluations
- `evaluaciones_intentoevaluacion` - Attempts
- `certificados_certificado` - Certificates

### Indexes
- All ForeignKeys have automatic indexes
- `Clase`: unique index on (curso_id, orden)
- `InscripcionCurso`: unique index on (usuario_id, curso_id)

---

## For UML Diagrams

### Recommended Diagrams

1. **Class Diagram** - All models with relationships
2. **Use Case Diagram** - Actors (Admin, Docente, Colaborador) and actions
3. **Sequence Diagram** - Course enrollment to certificate flow
4. **Activity Diagram** - Sequential class completion logic
5. **Entity Relationship Diagram** - Database schema

### Key Actors
- **Administrador** - Full system access
- **Docente** - Course creator/manager
- **Colaborador** - Student/learner
- **Sistema** - Automated processes

### Key Workflows
1. Course Creation → Publication → Enrollment
2. Class Completion (sequential unlock)
3. Evaluation → Scoring → Certificate Generation
4. Bulk User Enrollment (CSV)
5. Progress Tracking & Reporting

---

*Document Version: 1.0*
*Last Updated: 2026-04-12*
*Project: Kimün - Plataforma de Capacitación en Primeros Auxilios*
