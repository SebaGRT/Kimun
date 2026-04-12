# Guía de Demostración — Kimün LMS

> **Rama**: `stable`  
> **Plataforma**: Django 4.2 + Tailwind CSS + Alpine.js + Chart.js + WeasyPrint  
> **Audience**: Stakeholders / Profesores / Evaluadores  
> **Duración estimada**: 20-25 minutos

---

## 1. Preparación Pre-Demo

### 1.1 Arrancar el servidor

```bash
cd /home/sebacc/Documents/UDD/UDD/Ingeniería\ de\ Software/Proyecto-Kimün
git checkout stable
source venv/bin/activate
python manage.py runserver
```

Abrir en el navegador: `http://127.0.0.1:8000`

### 1.2 Credenciales de Acceso

| Usuario | Contraseña | Rol |
|--------|-----------|-----|
| admin | admin123 | Administrador |
| docente | docente123 | Docente |
| colaborador | colaborador123 | Colaborador |

> **Tip**: Crea las contraseñas ejecutando el comando `python manage.py shell` y cambiando con `user.set_password('nueva')` y `user.save()`.

---

## 2. Datos de Prueba a Crear

### 2.1 Como Administrador, crear:

**Cursos:**
1. "Cuidados Básicos del Adulto Mayor" — categoría: "Salud"
2. "Comunicación Efectiva con Personas Mayores" — categoría: "Habilidades Blandas"

**Usuarios:**
1. María García — Rol: Docente
2. Juan Pérez — Rol: Colaborador

**Evaluaciones (como Docente):**
1. "Evaluación Final — Cuidados Básicos" (3 preguntas, 15 min)
2. "Evaluación de Comunicación" (3 preguntas, 10 min)

**Eventos del Calendario:**
1. "Inicio: Cuidados Básicos" — fecha: mañana
2. "Evaluación Final" — fecha: en 3 días
3. "Plazo de Tarea" — fecha: en 5 días
4. "Fin de Curso" — fecha: en 2 semanas

**Anuncio:**
1. "Bienvenida al Programa de Capacitación 2026" — dirigido a todos los cursos

**Inscripciones:**
1. Inscribir a Juan Pérez en "Cuidados Básicos del Adulto Mayor"
2. Inscribir a Juan Pérez en "Comunicación Efectiva con Personas Mayores"

---

## 3. Orden de Demostración (Storytelling)

### 3.1 Página de Inicio — 2 minutos

**Navegar a**: `http://127.0.0.1:8000/`

**Qué decir**:
> "Esta es Kimün, la plataforma de capacitación de la ONG ALUMCO. Está diseñada específicamente para formar a cuidadores de adultos mayores en residencias ELEAM de Chile."

**Elementos a señalar**:
- Hero section con gradiente y estadísticas de cursos/estudiantes
- Cards de cursos destacados con diseño asimétrico
- Navegación con dropdown "Más" para secciones secundarias

---

### 3.2 Login y Cambio de Rol — 2 minutos

**Acción**: Cerrar sesión y entrar como `colaborador`/`colaborador123`

**Qué decir**:
> "Tenemos 3 roles diferenciados. El Colaborador es el participante que toma los cursos. El Docente gestiona sus propios cursos y evaluaciones. El Administrador tiene acceso completo al sistema."

**Navegar**: `http://127.0.0.1:8000/accounts/login/`

---

### 3.3 Vista del Colaborador — 2 minutos

**Como colaborador**, navegar a Mis Cursos.

**Qué decir**:
> "El colaborador ve solo los cursos en los que está inscrito. Puede ver sus materiales, tomar evaluaciones, descargar certificados y ver su progreso."

**Elementos a señalar**:
- Estados de inscripción (Asignado / En Progreso / Completado)
- Botón para tomar evaluaciones
- Acceso a certificados descargables

---

### 3.4 Volver como Administrador y Dashboard — 3 minutos

**Logout y login como** `admin`/`admin123`

**Navegar a**: `http://127.0.0.1:8000/reportes/dashboard/`

**Qué decir**:
> "El dashboard del administrador muestra métricas clave: estudiantes en riesgo de abandono, tasa de aprobación por curso, y actividad reciente del sistema."

**Elementos a señalar**:
- Gráfico de líneas (Chart.js) con datos dinámicos
- Cards de estadísticas con números destacados
- Indicador de estudiantes en riesgo (si hay datos)
- Sección de actividad reciente

---

### 3.5 Gestión de Usuarios — 2 minutos

**Navegar a**: `http://127.0.0.1:8000/usuarios/`

**Qué decir**:
> "Desde aquí gestionamos todos los usuarios del sistema. Como administradores, podemos crear, editar y asignar roles."

**Acción**: Crear un usuario nuevo.

**Qué señalar**:
> "Noten que al seleccionar el Rol, el campo Cargo se filtra automáticamente según el rol elegido. Esto reduce errores al asignar posiciones."

**Elementos a señalar**:
- Lista con avatar, nombre, rol y cargo
- Filtro de búsqueda por nombre
- Botón para crear usuario nuevo

---

### 3.6 Gestión de Cursos — 3 minutos

**Navegar a**: `http://127.0.0.1:8000/cursos/`

**Qué decir**:
> "Cada curso tiene materiales descargables, evaluaciones, y participantes inscritos. Todo el contenido está organizado por categorías."

**Acción**: Entrar al detalle de un curso.

**Elementos a señalar**:
- Diseño split: información a la izquierda, contenido a la derecha
- Lista de materiales (PDFs)
- Inscripción de participantes
- Estado del curso

---

### 3.7 Flujo de Evaluación Completo — 4 minutos

**Como administrador**, crear una evaluación rápida con 3 preguntas de alternativas.

**Navegar a**: `http://127.0.0.1:8000/evaluaciones/`

**Qué decir**:
> "Las evaluaciones son auto-corrigidas. Configuramos el tiempo límite, количество de intentos permitidos, y el porcentaje mínimo para aprobar."

**Acción**: Entrar a la evaluación como si fuera el colaborador.

**Elementos a señalar**:
- Timer visible en la parte superior
- Navegación entre preguntas (anterior/siguiente)
- Indicador de preguntas respondidas
- Al terminar: pantalla de resultado con detalle pregunta por pregunta (qué acertó, qué no)

**URL de ejemplo**: `http://127.0.0.1:8000/evaluaciones/tomar/1/`

---

### 3.8 Certificados PDF — 2 minutos

**Navegar a**: `http://127.0.0.1:8000/certificados/`

**Qué decir**:
> "Al aprobar todas las evaluaciones de un curso, el sistema genera automáticamente un certificado en PDF con código QR único de verificación."

**Acción**: Ver/Descargar un certificado existente.

**Elementos a señalar**:
- Tabla con historial de certificados
- Columna de verificación (código único)
- Botón de descarga PDF
- Diseño profesional del PDF (WeasyPrint)

---

### 3.9 Calendario de Eventos — 2 minutos

**Navegar a**: `http://127.0.0.1:8000/calendario/`

**Qué decir**:
> "El calendario muestra todos los eventos importantes: fechas de inicio y fin de cursos, plazos de tareas, y fechas de evaluaciones. Cada tipo de evento tiene un color diferente."

**Elementos a señalar**:
- Vista mensual con navegación
- Eventos codificados por color según tipo
- Tooltip con detalles al pasar el cursor

---

### 3.10 Sistema de Anuncios — 2 minutos

**Navegar a**: `http://127.0.0.1:8000/anuncios/`

**Qué decir**:
> "Podemos enviar anuncios a participantes específicos o a todos los cursos. El sistema tiene un comando de gestión que envía notificaciones por email automáticamente."

**Acción**: Crear un anuncio de prueba.

---

### 3.11 Modo Oscuro — 1 minuto

**Qué decir**:
> "La plataforma tiene modo oscuro integrado. EI toggle está en la barra de navegación y el cambio es instantáneo sin recargar la página."

**Acción**: Click en el icono de sol/luna en el navbar.

---

## 4. Resumen de Features Clave

| Feature | Tecnología | Impresión |
|---------|-----------|----------|
| Dashboard con gráficos | Chart.js | ⭐⭐⭐ |
| Evaluación con timer | Alpine.js | ⭐⭐⭐ |
| Certificados PDF con QR | WeasyPrint | ⭐⭐⭐ |
| Modo oscuro | CSS + Tailwind | ⭐⭐ |
| Calendario visual | FullCalendar / Custom | ⭐⭐ |
| Anuncios con email | Django signals | ⭐⭐ |
| Filtro de cargos por rol | JavaScript | ⭐⭐ |

---

## 5. Features Futuras (Phase 2)

Al final de la demo, mencionar:

> "Estamos trabajando en la próxima versión con: notificaciones push en tiempo real, certificados mejorados con firma digital, optimización completa para móviles, y accesibilidad WCAG para adultos mayores."

---

## 6. Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| No cargan los estilos | `python manage.py collectstatic` |
| Error de base de datos | `rm db.sqlite3 && python manage.py migrate` |
| Timer no funciona | Verificar que Alpine.js carga correctamente |
| PDF no se genera | Instalar dependencias: `sudo apt install libcairo2 libpango-1.0-0` |

---

## 7. Checklist Pre-Demo

- [ ] Servidor arrancado en `stable`
- [ ] 3 usuarios creados (admin, docente, colaborador)
- [ ] 2 cursos con materiales
- [ ] 2 evaluaciones con preguntas
- [ ] 3-5 eventos en el calendario
- [ ] 1 anuncio creado
- [ ] 2 inscripciones hechas
- [ ] Navegador abierto en `http://127.0.0.1:8000`
- [ ] Dark mode funciona
- [ ] Tests pasan: `python manage.py test`

---

*Documento generado para la demo del Proyecto Kimün — Abril 2026*
