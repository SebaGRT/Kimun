# Kimün - Plataforma de Capacitación ALUMCO

Plataforma de capacitación interna para la ONG ALUMCO, dedicada a trabajar con adultos mayores en residencias ELEAM.

## Características

- **Gestión de usuarios** con 3 roles: Administrador, Docente, Colaborador
- **Gestión de cursos** con materiales (PDF) y videos
- **Evaluaciones** con corrección automática
- **Certificados** en PDF con código de verificación
- **Categorías** para organizar cursos
- **Fechas límite** con recordatorios automáticos
- **Diseño responsivo** compatible con móviles
- **Modo oscuro** integrado

## Requisitos

- Python 3.10+
- Django 4.2+
- Node.js (opcional, para compilar Tailwind CSS)

## Instalación Rápida

### 1. Clonar y Entrar al proyecto
```bash
cd /home/sebacc/Documents/UDD/Ingeniería\ de\ Software/Proyecto-Kimün
```

### 2. Activar entorno virtual
```bash
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install django weasyprint pillow
```

### 4. Configurar base de datos
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Ejecutar
```bash
python manage.py runserver
```

### 6. Acceder
Abre tu navegador en: `http://127.0.0.1:8000`

## Credenciales de Acceso

| Usuario | Contraseña | Rol |
|--------|-----------|-----|
| admin | admin123 | Administrador |
| (crear nuevo) | - | Docente / Colaborador |

## Roles de Usuario

### Administrador
- Gestionar usuarios (crear, editar, eliminar)
- Gestionar categorías de cursos
- Inscribir usuarios a cursos
- Emitir certificados
- Ver reportes de cumplimiento
- Acceso completo a todas las funciones

### Docente
- Crear y editar cursos propios
- Agregar materiales (PDF, videos)
- Crear evaluaciones
- Ver características de sus cursos
- No puede gestionar usuarios ni ver reportes

### Colaborador
- Ver cursos asignados
- Completar materiales
- Tomar evaluaciones
- Obtener certificados al aprobar
- Descargar certificados
- Ver progreso personal

## Estructura del Proyecto

```
kimun/
├── cursos/           # Gestión de cursos y categorías
├── usuarios/         # Usuarios y autenticación
├── evaluaciones/     # Evaluaciones y preguntas
├── certificados/     # Generación de certificados PDF
├── reportes/        # Reportes y estadísticas
├── templates/        # Plantillas HTML
├── static/          # CSS, JS, imágenes
└── kimun/           # Configuración Django
```

## Modelos Principales

| Modelo | Descripción |
|--------|-------------|
| Usuario | Usuarios del sistema (extiende AbstractUser) |
| Curso | Cursos de capacitación |
| Material | Archivos PDF o videos por curso |
| Evaluacion | Pruebas con preguntas y alternativas |
| InscripcionCurso | Relación usuario-curso con estado |
| Certificado | Certificados generados con código único |
| Categoria | Categorías para organizar cursos |
| Recordatorio | Control de recordatorios enviados |

## Estados de Inscripción

- **Asignado**: Usuario recibió el curso
- **En Progreso**: Usuario comenzó el curso
- **Completado**: Usuario apruebó todas las evaluaciones

## Configuración de Correo

Por defecto, los correos se muestran en la consola. Para configurar SMTP:

```python
# kimun/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

## Solución de Problemas

### No aparecen los estilos
```bash
# Verificar que Tailwind esté compilado
ls static/css/
```

### Error de base de datos
```bash
# Recrear base de datos
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Error al generar PDF (WeasyPrint)
```bash
# Instalar dependencias del sistema
# Ubuntu/Debian:
sudo apt-get install libcairo2 libpango-1.0-0 libgobject-2.0-0

# Mac:
brew install cairo pango libgobject
```

## Tecnologías Usadas

- **Backend**: Django 4.2+
- **Frontend**: Django Templates + Tailwind CSS
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **PDFs**: WeasyPrint + Pillow
- **Icons**: Bootstrap Icons

## Licencia

MIT License - Proyecto desarrollado para ONG ALUMCO

## Equipo

Desarrollado por equipo universitario para el ramo Ingeniería de Software

---

¿Necesitas ayuda? Revisa el código o contacta al equipo de desarrollo.
