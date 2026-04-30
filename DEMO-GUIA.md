# Guía de Demostración — Kimün LMS

> **Rama**: `stable`  
> **Plataforma**: Django 4.2 + Tailwind CSS + Alpine.js + Chart.js + WeasyPrint  
> **Audience**: Stakeholders / Profesores / Evaluadores  
> **Duración estimada**: 25-30 minutos

---

## 1. Preparación Pre-Demo

### 1.1 Arrancar el servidor

```bash
cd /home/sebacc/Documents/UDD/Ingeniería\ de\ Software/Proyecto-Kimün
git checkout stable
source venv/bin/activate
python manage.py runserver
```

Abrir en el navegador: `http://127.0.0.1:8000`

### 1.2 Credenciales de Acceso (Datos Pre-Cargados)

| Usuario | Contraseña | Rol | Cargo |
|--------|-----------|-----|-------|
| admin | admin123 | Administrador | Administración y Apoyo |
| docente | docente123 | Docente | Docente Interno |
| colaborador | colaborador123 | Colaborador | Profesional de Atención Directa |

> **Nota**: Los datos de demo ya están creados. Curso "Cuidados Básicos del Adulto Mayor" con evaluación de 3 preguntas.

---

## 2. Matriz de Cumplimiento (Rúbrica Valentina Garrido)

| Categoría | Peso | Estado | Notas |
|-----------|------|--------|-------|
| **1. Cumplimiento de objetivos** | 30% | ✅ **Cumplido** | Workflow completo certificados, 304 tests, 8 commits |
| **2. Usabilidad y accesibilidad** | 20% | ⚠️ **Parcial** | Navegación clara, falta verificar tipografía adultos mayores |
| **3. Calidad del contenido** | 20% | ✅ **Cumplido** | Diploma profesional gold/navy, sistema evaluaciones funcional |
| **4. Presentación** | 20% | ✅ **Cumplido** | DEMO-GUIA actualizado, demo data lista, flujos documentados |
| **5. Valor percibido** | 10% | ✅ **Cumplido** | MVP funcional end-to-end |

**Nota estimada: 6.0-6.5 / 7.0**

---

## 3. Orden de Demostración (Storytelling)

### 3.1 Página de Inicio — 2 minutos

**Navegar a**: `http://127.0.0.1:8000/`

**Qué decir**:
> "Esta es Kimün, la plataforma de capacitación de la ONG ALUMCO. Está diseñada específicamente para formar a cuidadores de adultos mayores en residencias ELEAM de Chile. El nombre 'Kimün' proviene del mapudungun y está alineado con nuestra misión de capacitación."

**Elementos a señalar**:
- Hero section con gradiente y estadísticas de cursos/estudiantes
- Cards de cursos destacados con diseño asimétrico
- Navegación con dropdown "Más" para secciones secundarias

---

### 3.2 Login y Cambio de Rol — 2 minutos

**Acción**: Entrar como `colaborador`/`colaborador123`

**Qué decir**:
> "Tenemos 3 roles diferenciados. El Colaborador es el participante que toma los cursos. El Docente gestiona sus propios cursos y evaluaciones. El Administrador tiene acceso completo al sistema. Cada rol tiene cargos específicos asignados automáticamente."

**Navegar**: `http://127.0.0.1:8000/accounts/login/`

---

### 3.3 Vista del Colaborador y Restricción de Cursos — 2 minutos

**Como colaborador**, intentar navegar a `/cursos/`.

**Qué decir**:
> "Noten que si un colaborador intenta acceder a la lista general de cursos, es redirigido automáticamente a 'Mis Cursos'. Esto garantiza que solo vean los cursos en los que están inscritos, asignados por un administrador."

**Elementos a señalar**:
- Redirección automática de `/cursos/` a `/mis-cursos/`
- Link "Cursos" oculto en navegación para colaboradores
- Estados de inscripción (Asignado / En Progreso / Completado)

---

### 3.4 Volver como Administrador y Dashboard — 3 minutos

**Logout y login como** `admin`/`admin123`

**Navegar a**: `http://127.0.0.1:8000/reportes/dashboard/`

**Qué decir**:
> "El dashboard del administrador muestra métricas clave: estudiantes en riesgo de abandono, tasa de aprobación por curso, y actividad reciente del sistema."

**Elementos a señalar**:
- Gráfico de líneas (Chart.js) con datos dinámicos
- Cards de estadísticas con números destacados
- Indicador de estudiantes en riesgo
- Sección de actividad reciente

---

### 3.5 Gestión de Usuarios y Cargos — 2 minutos

**Navegar a**: `http://127.0.0.1:8000/usuarios/`

**Qué decir**:
> "Desde aquí gestionamos todos los usuarios del sistema. Como administradores, podemos crear, editar y asignar roles."

**Acción**: Mostrar los cargos asignados a cada usuario.

**Qué señalar**:
> "Noten que al seleccionar el Rol, el campo Cargo se filtra automáticamente según el rol elegido: Administradores tienen 'Administración y Apoyo' o 'Directivos'; Docentes tienen 'Docente Interno' o 'Docente Externo'; Colaboradores tienen 5 opciones incluyendo 'Profesional de Atención Directa', 'Técnico de Atención Directa', etc."

**Elementos a señalar**:
- Lista con avatar, nombre, rol y cargo
- Filtro de búsqueda por nombre
- Botón para crear usuario nuevo

---

### 3.6 Gestión de Cursos — 3 minutos

**Navegar a**: `http://127.0.0.1:8000/cursos/`

**Qué decir**:
> "Cada curso tiene materiales descargables, evaluaciones, y participantes inscritos. Todo el contenido está organizado por categorías."

**Acción**: Entrar al detalle del curso "Cuidados Básicos del Adulto Mayor".

**Elementos a señalar**:
- Diseño split: información a la izquierda, contenido a la derecha
- Lista de materiales (PDFs)
- Inscripción de participantes
- Estado del curso
- Docente asignado (María García)

---

### 3.7 Flujo de Evaluación y Aprobación — 4 minutos

**Como colaborador**, tomar la evaluación del curso.

**Navegar a**: `http://127.0.0.1:8000/evaluaciones/`

**Qué decir**:
> "Las evaluaciones son auto-corrigidas. Configuramos el tiempo límite, cantidad de intentos permitidos, y el porcentaje mínimo para aprobar. Esta evaluación tiene 3 preguntas y requiere 60% para aprobar."

**Acción**: Tomar la evaluación respondiendo correctamente.

**Elementos a señalar**:
- Timer visible en la parte superior
- Navegación entre preguntas (anterior/siguiente)
- Indicador de preguntas respondidas
- Al terminar: pantalla de resultado con detalle pregunta por pregunta

**Resultado esperado**: 3/3 respuestas correctas = 100% aprobado.

---

### 3.8 Workflow de Certificados con Aprobación — 5 minutos

**Paso 1 - Ver certificado pendiente (como colaborador)**

**Navegar a**: `http://127.0.0.1:8000/certificados/mis-certificados/`

**Qué decir**:
> "Al aprobar todas las evaluaciones, el sistema crea automáticamente un certificado en estado 'PENDIENTE'. El colaborador puede ver que completó el curso, pero NO puede descargar el certificado todavía."

**Elementos a señalar**:
- Badge amarillo "Pendiente de aprobación"
- No hay botón de descarga
- Mensaje indicando que debe esperar aprobación

---

**Paso 2 - Aprobar certificado (como administrador)**

**Cambiar a usuario admin**, navegar a: `http://127.0.0.1:8000/certificados/pendientes/`

**Qué decir**:
> "El docente o administrador debe revisar y aprobar el certificado. Este flujo de aprobación es crítico para garantizar que solo se entreguen certificados validados. Los docentes solo ven certificados de sus cursos; los administradores ven todos."

**Acción**: Aprobar el certificado de "Juan Pérez".

**Elementos a señalar**:
- Lista de certificados pendientes
- Información del colaborador y curso
- Botones "Aprobar" (verde) y "Rechazar" (rojo)
- Opción de resetear si se rechaza por error

---

**Paso 3 - Descargar certificado (como colaborador)**

**Volver a colaborador**, refrescar página de certificados.

**Qué decir**:
> "Una vez aprobado, el colaborador ve el certificado en estado 'APROBADO' y puede descargar el PDF. El diseño es profesional con tema dorado/azul marino, bordes ornamentales, y código de verificación único."

**Acción**: Descargar el certificado PDF.

**Elementos a señalar**:
- Badge verde "Aprobado"
- Botón "Descargar PDF" habilitado
- Diseño profesional del PDF (orientación landscape A4)
- Código de verificación único
- Firma de la Dirección de Capacitación

---

### 3.9 Filtro de Cursos para Docentes — 2 minutos

**Login como docente** (`docente`/`docente123`)

**Navegar a**: `http://127.0.0.1:8000/mis-cursos/`

**Qué decir**:
> "Los docentes solo ven en 'Mis Cursos' los cursos donde están asignados como docentes. No ven cursos de otros docentes ni todos los cursos del sistema."

**Elementos a señalar**:
- Lista filtrada solo a cursos del docente actual
- Acceso a gestionar evaluaciones y materiales de sus cursos

---

### 3.10 Calendario de Eventos — 2 minutos

**Navegar a**: `http://127.0.0.1:8000/calendario/`

**Qué decir**:
> "El calendario muestra todos los eventos importantes: fechas de inicio y fin de cursos, plazos de tareas, y fechas de evaluaciones. Cada tipo de evento tiene un color diferente."

**Elementos a señalar**:
- Vista mensual con navegación
- Eventos codificados por color según tipo
- Tooltip con detalles al pasar el cursor

---

### 3.11 Modo Oscuro — 1 minuto

**Qué decir**:
> "La plataforma tiene modo oscuro integrado. El toggle está en la barra de navegación y el cambio es instantáneo sin recargar la página."

**Acción**: Click en el icono de sol/luna en el navbar.

---

## 4. Features Clave Implementadas

| Feature | Tecnología | Estado en Demo |
|---------|-----------|----------------|
| Dashboard con gráficos | Chart.js | ✅ Funcional |
| Evaluación con timer | Alpine.js | ✅ Funcional |
| **Certificados con aprobación** | WeasyPrint + Django | ✅ **NUEVO - Flujo completo** |
| Redirección colaboradores | Django Views | ✅ **NUEVO** |
| Filtro cursos por docente | Django ORM | ✅ **NUEVO** |
| Modo oscuro | CSS + Tailwind | ✅ Funcional |
| Calendario visual | Custom | ✅ Funcional |
| Filtro de cargos por rol | JavaScript | ✅ Funcional |

---

## 5. Mejoras Futuras (Mencionar al final)

> "Estamos trabajando en: notificaciones email para aprobación de certificados, firma digital en PDFs, optimización móvil completa, y accesibilidad WCAG AA para adultos mayores."

---

## 6. Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| No cargan los estilos | `python manage.py collectstatic` |
| Error de base de datos | `rm db.sqlite3 && python manage.py migrate && python manage.py shell < demo_data.py` |
| Timer no funciona | Verificar que Alpine.js carga correctamente |
| PDF no se genera | Instalar dependencias: `sudo apt install libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0` |
| Certificado aparece como 404 | Limpiar caché: `python manage.py shell -c "from certificados.models import Certificado; Certificado.objects.filter(archivo_pdf__isnull=False).update(archivo_pdf=None)"` |

---

## 7. Checklist Pre-Demo (Automatizado)

- [x] Rama `stable` actualizada
- [x] 3 usuarios creados con cargos asignados
- [x] 1 curso con evaluación de 3 preguntas
- [x] Inscripción creada
- [x] Base de datos migrada
- [x] Tests pasando (304 tests)
- [x] Servidor funcionando

**Comando de verificación rápida:**
```bash
cd /home/sebacc/Documents/UDD/Ingeniería\ de\ Software/Proyecto-Kimün
git checkout stable
source venv/bin/activate
python manage.py test --verbosity=0 && echo "✅ Tests OK" || echo "❌ Tests fallando"
python manage.py runserver
```

---

*Documento actualizado para demo del Proyecto Kimün — Abril 2026*  
*Incluye: Certificate Approval Workflow, Role-based Access Control*
