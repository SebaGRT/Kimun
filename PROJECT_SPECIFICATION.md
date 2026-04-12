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

## Guía de Diagramas UML

### Instrucciones Generales

**Herramientas Recomendadas:**
- **Visual Paradigm** - Profesional, completo
- **Lucidchart** - Online, colaborativo
- **draw.io (diagrams.net)** - Gratuito, versátil
- **PlantUML** - Texto a diagramas

**Convenciones:**
- Usar español en todos los diagramas
- Incluir leyenda en cada diagrama
- Numerar los diagramas secuencia de actividad
- Guardar en formato PDF y PNG

---

### 1. Diagrama de Casos de Uso (Use Case Diagram)

**Archivo:** `Diagrama de caso de uso.pdf`

**Actores:**
1. **Administrador** - Acceso total al sistema
2. **Docente** - Crea y gestiona cursos propios
3. **Colaborador** - Participante que toma cursos
4. **Sistema** - Procesos automáticos

**Casos de Uso por Actor:**

**Administrador:**
- CRUD Usuarios (crear, leer, actualizar, eliminar)
- CRUD Categorías
- CRUD Cursos (todos)
- Inscribir usuarios a cursos
- Generar certificados manualmente
- Ver dashboard con estadísticas
- Gestión de anuncios
- Generar reportes

**Docente:**
- CRUD Cursos propios
- CRUD Materiales (PDFs, videos)
- CRUD Evaluaciones
- Inscribir usuarios a cursos propios
- Ver reportes de cursos propios
- Ver certificados emitidos

**Colaborador:**
- Ver cursos asignados
- Ver materiales del curso
- Completar clases (secuencial)
- Tomar evaluaciones
- Ver resultados de evaluaciones
- Descargar certificados
- Ver progreso personal

**Sistema:**
- Enviar recordatorios automáticos
- Calificar evaluaciones automáticamente
- Generar certificados al aprobar
- Crear eventos de calendario

**Relaciones a mostrar:**
- `<<include>>` - Cuando un caso de uso siempre requiere otro
  - Ejemplo: "Tomar evaluación" include "Verificar inscripción"
- `<<extend>>` - Cuando un caso de uso extiende otro bajo condición
  - Ejemplo: "Enviar recordatorio" extends "Crear curso" (si hay fecha límite)

**Ejemplo de Estructura:**
```
[Administrador] -----> (Gestionar Usuarios)
                  -----> (Gestionar Categorías)
                  -----> (Gestionar Todos los Cursos)
                  -----> (Ver Dashboard)
                  -----> (Generar Reportes)

[Docente] ----------> (Crear Curso) <<include>> (Definir Categoría)
                  ----------> (Gestionar Materiales)
                  ----------> (Crear Evaluación)
                  ----------> (Ver Reporte de Curso)

[Colaborador] ------> (Ver Cursos Asignados)
                  ------> (Completar Clase)
                  ------> (Tomar Evaluación) <<include>> (Verificar Tiempo)
                  ------> (Descargar Certificado)

(Sistema) --------> (Enviar Recordatorios) <<extend>> (Crear Curso con Fecha)
```

---

### 2. Diagrama de Clases (Class Diagram)

**Archivo:** `Diagrama de clases.pdf`

**Clases Principales:**

**usuarios App:**
```python
class Usuario (extends AbstractUser)
  - rut: CharField(unique)
  - rol: CharField(choices: admin/docente/colaborador)
  - cargo: ForeignKey(AreaCargo)
  - telefono: CharField
  - methods: clean(), save()

class AreaCargo
  - nombre: CharField
  - descripcion: TextField
  - categoria: CharField(colaborador/admin/docente)
```

**cursos App:**
```python
class Categoria
  - nombre: CharField
  - descripcion: TextField
  - color: CharField(hex)

class Curso
  - titulo: CharField
  - descripcion: TextField
  - categoria: ForeignKey(Categoria)
  - docente_creador: ForeignKey(Usuario)
  - estado: CharField(borrador/publicado)
  - fecha_inicio: DateTimeField
  - fecha_fin: DateTimeField
  - porcentaje_aprobacion: IntegerField
  - methods: clean(), save(), es_completado_por(usuario)

class Material
  - curso: ForeignKey(Curso)
  - titulo: CharField
  - archivo: FileField(PDF)
  - url_video: URLField
  - orden: PositiveIntegerField

class Clase
  - curso: ForeignKey(Curso)
  - titulo: CharField
  - contenido: RichTextField(ckeditor)
  - orden: PositiveIntegerField
  - methods: es_accesible_para(usuario)

class InscripcionCurso
  - usuario: ForeignKey(Usuario)
  - curso: ForeignKey(Curso)
  - estado: CharField(asignado/en_progreso/completado)
  - fecha_inscripcion: DateTimeField
  - fecha_completado: DateTimeField

class ClaseCompletado
  - usuario: ForeignKey(Usuario)
  - clase: ForeignKey(Clase)
  - fecha_completado: DateTimeField
```

**evaluaciones App:**
```python
class Evaluacion
  - curso: ForeignKey(Curso)
  - titulo: CharField
  - descripcion: TextField
  - tiempo_limite: IntegerField(minutes)
  - intentos_permitidos: IntegerField
  - porcentaje_aprobacion: IntegerField
  - fecha_apertura: DateTimeField
  - fecha_cierre: DateTimeField

class Pregunta
  - evaluacion: ForeignKey(Evaluacion)
  - texto: TextField
  - puntaje: DecimalField
  - orden: PositiveIntegerField

class Alternativa
  - pregunta: ForeignKey(Pregunta)
  - texto: CharField
  - es_correcta: BooleanField

class IntentoEvaluacion
  - usuario: ForeignKey(Usuario)
  - evaluacion: ForeignKey(Evaluacion)
  - fecha_inicio: DateTimeField
  - fecha_fin: DateTimeField
  - puntaje_obtenido: DecimalField
  - porcentaje: DecimalField
  - aprobado: BooleanField
  - respuestas: JSONField  # {pregunta_id: alternativa_id}
```

**certificados App:**
```python
class Certificado
  - usuario: ForeignKey(Usuario)
  - curso: ForeignKey(Curso)
  - codigo_verificacion: UUIDField(unique)
  - fecha_emision: DateTimeField
  - fecha_expiracion: DateTimeField
  - pdf: FileField
  - methods: generar_pdf(), verificar()
```

**calendario App:**
```python
class EventoCalendario
  - titulo: CharField
  - descripcion: TextField
  - tipo: CharField(clase_deadline/evaluacion_deadline/curso_start/curso_end/evento_general)
  - curso: ForeignKey(Curso, null=True)
  - fecha_inicio: DateTimeField
  - fecha_fin: DateTimeField
  - usuarios_asignados: ManyToManyField(Usuario)
```

**Relaciones a mostrar:**
- Asociación (línea simple): cuando una clase usa otra
- Agregación (rombo vacío): "tiene" pero puede existir sin el padre
- Composición (rombo lleno): "contiene" y no puede existir sin el padre
- Herencia (flecha vacía): "extends" o "is a"

**Multiplicidades:**
- `1` - Exactamente uno
- `0..1` - Cero o uno
- `*` - Cero o muchos
- `1..*` - Uno o muchos

---

### 3. Diagrama de Actividad (Activity Diagram)

**Archivo:** `DIAGRAMA DE ACTIVIDAD.pdf`

**Flujo recomendado:** Proceso de inscripción y certificación

**Pasos a mostrar:**

1. **Nodo Inicial** (círculo negro)

2. **Actividad**: "Colaborador solicita inscripción"

3. **Decisión** (rombo): "¿Está aprobada la solicitud?"
   - [Sí] → Siguiente actividad
   - [No] → "Notificar rechazo" → Nodo Final

4. **Actividad**: "Inscribir en curso" (Sistema crea InscripcionCurso)

5. **Actividad**: "Asignar clases secuenciales"

6. **Bucle/Actividad**: "Completar clases" (flecha de retorno hasta completar todas)
   - "Ver clase N"
   - "Marcar clase N como completada"
   - "Desbloquear clase N+1"

7. **Decisión**: "¿Todas las clases completadas?"
   - [No] → Regresar al bucle
   - [Sí] → Continuar

8. **Actividad**: "Tomar evaluación final"

9. **Decisión**: "¿Aprobó evaluación?"
   - [No] → "Mostrar resultado" → "Permitir reintento" → Regresar a 8
   - [Sí] → Continuar

10. **Actividad**: "Generar certificado automáticamente"

11. **Actividad**: "Notificar al colaborador"

12. **Nodo Final** (círculo negro con borde)

**Ramas paralelas (Fork/Join):**
- Mostrar en paralelo: "Enviar email" + "Crear notificación en-app" + "Actualizar dashboard"

**Swimlanes (Canales):**
- Canal 1: Colaborador
- Canal 2: Sistema
- Canal 3: Docente/Admin

---

### 4. Diagrama de Secuencia (Sequence Diagram)

**Archivo:** `DIAGRAMA DE SECUENCIA.pdf`

**Escenarios recomendados:**

#### Escenario 1: Flujo de Evaluación (recomendado)

**Participantes:**
- `Col` - Colaborador (actor)
- `Web` - Navegador/Web App
- `View` - Django View
- `Eval` - Evaluacion Model
- `Intento` - IntentoEvaluacion Model
- `Cert` - Certificado Model

**Secuencia:**

```
1.  Col → Web: GET /evaluaciones/1/
2.  Web → View: request
3.  View → Eval: get(pk=1)
4.  View → Intento: get_or_create(usuario, evaluacion)
5.  View → Web: render(template con evaluación)
6.  Web → Col: Mostrar evaluación con timer

7.  Col → Web: POST respuestas
8.  Web → View: POST request
9.  View → Eval: calcular_puntaje(respuestas)
10. View → Intento: save(puntaje, aprobado)
11. View → Cert: create(usuario, curso) [si aprobó]
12. View → Web: redirect a resultado
13. Web → Col: Mostrar resultado con detalle
```

**Notas:**
- Incluir alt/else para "Si aprobó" vs "Si no aprobó"
- Incluir loop para "Para cada pregunta"
- Mostrar tiempo de vida de objetos (líneas punteadas)

#### Escenario 2: Generación de Certificado

**Participantes:**
- `Sys` - Sistema (señal Django)
- `View` - Resultado view
- `Intento` - IntentoEvaluacion
- `Cert` - Certificado Model
- `PDF` - WeasyPrint/ReportLab
- `Email` - Email backend

**Secuencia:**

```
1. Sys → View: signal(intento_completado)
2. View → Intento: check(aprobado=True)
3. View → Cert: create(usuario, curso)
4. Cert → PDF: generar(certificado_data)
5. PDF → Cert: pdf_file
6. Cert → Email: send_email(usuario, certificado)
7. Email → Usuario: Notificación
```

---

### 5. Diagrama de Componentes (Component Diagram)

**Archivo:** `DIAGRAMA DE COMPONENTES.pdf`

**Nivel:** Vista de alto nivel de la arquitectura Django

**Componentes a mostrar:**

**Capa de Presentación:**
```
[<<component>> Django Templates]
  - Base templates
  - Course templates
  - User templates
  - Evaluation templates
  - Certificate templates

[<<component>> Static Assets]
  - CSS (Tailwind)
  - JavaScript (Alpine.js, HTMX)
  - Images
```

**Capa de Aplicación:**
```
[<<component>> cursos App]
  - Models: Curso, Clase, Material
  - Views: Course CRUD, Enrollment
  - Templates: course_list, course_detail

[<<component>> usuarios App]
  - Models: Usuario, AreaCargo
  - Views: Auth, Profile
  - Templates: login, profile

[<<component>> evaluaciones App]
  - Models: Evaluacion, Pregunta, Intento
  - Views: Take evaluation, Results
  - Templates: evaluacion_form, resultado

[<<component>> certificados App]
  - Models: Certificado
  - Views: Generate, Verify, Download
  - Templates: certificado_list

[<<component>> calendario App]
  - Models: EventoCalendario
  - Views: Calendar view
  - Templates: calendario

[<<component>> anuncios App]
  - Models: Anuncio
  - Views: Announcement CRUD
  - Templates: anuncio_list

[<<component>> reportes App]
  - Views: Dashboard, Reports
  - Templates: dashboard
```

**Capa de Infraestructura:**
```
[<<component>> Django Core]
  - Settings
  - URLs
  - Middleware
  - Authentication

[<<component>> Database]
  - SQLite (dev)
  - PostgreSQL (prod)

[<<component>> External Services]
  - Email Backend
  - PDF Generation (WeasyPrint)
  - File Storage
```

**Conectores (interfaces):**
- `<<import>>` - Una app usa modelos de otra
- `<<use>>` - Un componente usa otro

**Ejemplo de conexiones:**
```
[evaluaciones] --<<use>>--> [cursos] (usa Curso)
[evaluaciones] --<<use>>--> [usuarios] (usa Usuario)
[certificados] --<<use>>--> [evaluaciones] (usa IntentoEvaluacion)
[calendario] --<<use>>--> [cursos] (usa Curso)
[reportes] --<<use>>--> [cursos, usuarios, evaluaciones]
```

---

### 6. Diagrama de Despliegue (Deployment Diagram)

**Archivo:** `diagrama de despliegue.pdf`

**Entornos a mostrar:**

#### Entorno de Desarrollo (Local)

```
<<device>> Laptop del Desarrollador
  |__ <<artifact>> Python 3.10+
  |__ <<artifact>> Django 4.2
  |__ <<artifact>> SQLite
  |__ <<artifact>> venv/
  
  <<execution environment>> Django Dev Server
    |__ [cursos App]
    |__ [usuarios App]
    |__ [evaluaciones App]
    |__ [certificados App]
    |__ [calendario App]
    |__ [anuncios App]
    |__ [reportes App]
```

#### Entorno de Producción (Servidor)

```
<<device>> Servidor Web (Ubuntu 22.04)
  |__ <<artifact>> Nginx (Reverse Proxy)
  |__ <<artifact>> Gunicorn (WSGI)
  |__ <<artifact>> PostgreSQL 14
  |__ <<artifact>> Python 3.10
  |__ <<artifact>> WeasyPrint + dependencias
  
  <<execution environment>> Django Application
    |__ <<deploy>> kimun/
        |__ <<artifact>> settings.py (prod)
        |__ <<artifact>> wsgi.py
        |__ [cursos/]
        |__ [usuarios/]
        |__ [evaluaciones/]
        |__ [certificados/]
        |__ [calendario/]
        |__ [anuncios/]
        |__ [reportes/]
  
  <<artifact>> Media Storage (/var/www/kimun/media/)
  <<artifact>> Static Files (/var/www/kimun/static/)
```

**Nodos de comunicación:**
```
[Cliente Web] --HTTPS--> [Nginx] --HTTP--> [Gunicorn] --WSGI--> [Django]
                                              |
                                              v
                                        [PostgreSQL]
```

**Configuración recomendada:**

```
<<device>> Servidor Producción
  OS: Ubuntu 22.04 LTS
  
  Servicios:
    - Nginx (puerto 80/443)
    - Gunicorn (puerto 8000, unix socket)
    - PostgreSQL (puerto 5432, localhost)
    - Redis (opcional, para caché)
  
  Aplicación:
    - Código en: /var/www/kimun/
    - Virtualenv en: /var/www/kimun/venv/
    - Media en: /var/www/kimun/media/
    - Static en: /var/www/kimun/static/
    - Logs en: /var/log/kimun/
  
  Usuarios:
    - www-data: usuario del servidor web
    - kimun: usuario de la aplicación
```

**Configuración de Nginx:**
```nginx
server {
    listen 80;
    server_name kimun.alumco.org;
    
    location /static/ {
        alias /var/www/kimun/static/;
    }
    
    location /media/ {
        alias /var/www/kimun/media/;
    }
    
    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Entregables

### Lista de Archivos

| Diagrama | Archivo | Estado |
|----------|---------|--------|
| Casos de Uso | `Diagrama de caso de uso.pdf` | ⬜ Pendiente |
| Clases | `Diagrama de clases.pdf` | ⬜ Pendiente |
| Actividad | `DIAGRAMA DE ACTIVIDAD.pdf` | ⬜ Pendiente |
| Secuencia | `DIAGRAMA DE SECUENCIA.pdf` | ⬜ Pendiente |
| Componentes | `DIAGRAMA DE COMPONENTES.pdf` | ⬜ Pendiente |
| Despliegue | `diagrama de despliegue.pdf` | ⬜ Pendiente |

### Notas Finales

1. **Consistencia**: Mantener los mismos nombres de clases/métodos en todos los diagramas
2. **Versionado**: Incluir versión del documento y fecha en cada diagrama
3. **Revisión**: Validar que los diagramas reflejen el código actual (models.py, views.py)
4. **Formato**: Exportar en PDF de alta calidad para impresión y PNG para presentaciones

---

*Document Version: 1.1*
*Last Updated: 2026-04-12*
*Project: Kimün - Plataforma de Capacitación en Primeros Auxilios*