## Arquitectura

### Estructura del Proyecto
El sistema se organiza en 8 aplicaciones Django principales:
- `usuarios` — Gestión de usuarios, perfiles y autenticación (3 roles).
- `cursos` — Gestión de cursos, categorías y materiales de estudio.
- `evaluaciones` — Sistema de evaluaciones con corrección automática.
- `tareas` — Gestión de entregas y retroalimentación de tareas.
- `certificados` — Generación dinámica de certificados en formato PDF.
- `reportes` — Dashboard de estadísticas y reportes de cumplimiento.
- `calendario` — Sistema de calendario para eventos y fechas límite.
- `anuncios` — Sistema de anuncios globales y notificaciones.

### Tecnologías
- **Core**: Django 4.2+, Python 3.10+
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: Tailwind CSS, Alpine.js, Bootstrap Icons
- **Visualización**: Chart.js (en reportes)
- **PDF**: WeasyPrint

### Sistema de Diseño
El proyecto utiliza un sistema de diseño basado en variables CSS centralizadas en `base.html`, soportando modo oscuro nativo mediante el atributo `data-theme="dark"`.

Variables principales:
- `--color-bg`: Color de fondo principal.
- `--color-surface`: Fondo de tarjetas y elementos de superficie.
- `--color-primary`: Color de marca principal.
- `--color-secondary`: Color secundario.
- `--color-accent`: Color de acento (naranjo).
- `--color-success`, `--color-warning`, `--color-danger`: Colores semánticos.
- `--color-text`, `--color-text-muted`: Colores para tipografía.

Adicionalmente, se cuenta con una librería de componentes en `static/css/kimun.css`.

### Ramas (Git Flow)
- `main`: Rama de producción y despliegue final.
- `stable`: Rama utilizada para demostraciones y QA.
- `development`: Rama principal de integración para nuevas características.

### Scripts de Herramientas
El directorio `tools/` contiene scripts temporales de debugging y utilidades de desarrollo que no deben utilizarse en entornos de producción.

