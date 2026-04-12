# Guía para Replicar Diagramas UML con IA

> **Proyecto**: Kimün LMS - Plataforma de Capacitación para ONG ALUMCO  
> **Stack**: Django 4.2 + Tailwind CSS  
> **Objetivo**: Generar 6 diagramas UML en formato PDF  
> **Fecha**: Abril 2026

---

## Resumen para el Agente IA

Esta guía permite a cualquier agente de IA generar los 6 diagramas UML del proyecto Kimün. El agente debe:

1. Leer el código fuente del proyecto (models.py, views.py, urls.py)
2. Generar archivos PlantUML (.puml) con la sintaxis correcta
3. Exportar a PDF con nombres específicos
4. Validar que los diagramas reflejan el código real

---

## Contexto del Proyecto

**Kimün** es un LMS (Learning Management System) desarrollado en Django para capacitación de cuidadores de adultos mayores. La ONG ALUMCO trabaja con residencias ELEAM en Chile.

### Stack Tecnológico
- **Backend**: Django 4.2, Python 3.10+
- **Base de datos**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Tailwind CSS, Alpine.js, Chart.js
- **PDFs**: WeasyPrint
- **Editor**: CKEditor 4

### Estructura de Apps
```
kimun/
├── usuarios/      # Gestión de usuarios, roles, autenticación
├── cursos/        # Cursos, clases, materiales, inscripciones
├── evaluaciones/  # Evaluaciones, preguntas, intentos, calificación
├── certificados/  # Generación de certificados PDF con QR
├── calendario/    # Eventos, recordatorios, fechas importantes
├── anuncios/      # Sistema de anuncios y notificaciones
├── reportes/      # Dashboard con estadísticas y gráficos
└── kimun/         # Configuración principal de Django
```

### Roles del Sistema
1. **Administrador**: Acceso total, gestiona usuarios y cursos
2. **Docente**: Crea cursos propios, evaluaciones, ve reportes
3. **Colaborador**: Toma cursos, evaluaciones, descarga certificados

---

## Los 6 Diagramas Requeridos

### 1. Diagrama de Clases (Class Diagram)
**Archivo de salida**: `Diagrama de clases.pdf`

**Qué debe mostrar**:
- Todos los modelos de las 6 apps Django
- Relaciones ForeignKey, ManyToMany, OneToOne
- Herencia (Usuario extiende AbstractUser)
- Métodos importantes de cada modelo
- Cardinalidad de relaciones (1, *, 1..*)

**Modelos principales**:
```python
# usuarios/models.py
Usuario (extends AbstractUser)
├── rut: CharField(unique)
├── rol: CharField(admin/docente/colaborador)
├── cargo: ForeignKey(AreaCargo)
└── telefono: CharField

AreaCargo
├── nombre: CharField
├── descripcion: TextField
└── categoria: CharField

# cursos/models.py
Curso
├── titulo: CharField
├── descripcion: TextField
├── categoria: ForeignKey(Categoria)
├── docente_creador: ForeignKey(Usuario)
├── estado: CharField(borrador/publicado)
├── fecha_inicio: DateTimeField
├── fecha_fin: DateTimeField
└── porcentaje_aprobacion: IntegerField

Categoria
├── nombre: CharField
├── descripcion: TextField
└── color: CharField

Clase
├── curso: ForeignKey(Curso)
├── titulo: CharField
├── contenido: RichTextField(ckeditor)
└── orden: PositiveIntegerField

Material
├── curso: ForeignKey(Curso)
├── titulo: CharField
├── archivo: FileField(PDF)
├── url_video: URLField
└── orden: PositiveIntegerField

InscripcionCurso
├── usuario: ForeignKey(Usuario)
├── curso: ForeignKey(Curso)
├── estado: CharField(asignado/en_progreso/completado)
├── fecha_inscripcion: DateTimeField
└── fecha_completado: DateTimeField

ClaseCompletado
├── usuario: ForeignKey(Usuario)
├── clase: ForeignKey(Clase)
└── fecha_completado: DateTimeField

# evaluaciones/models.py
Evaluacion
├── curso: ForeignKey(Curso)
├── titulo: CharField
├── descripcion: TextField
├── tiempo_limite: IntegerField(minutos)
├── intentos_permitidos: IntegerField
├── porcentaje_aprobacion: IntegerField
├── fecha_apertura: DateTimeField
└── fecha_cierre: DateTimeField

Pregunta
├── evaluacion: ForeignKey(Evaluacion)
├── texto: TextField
├── puntaje: DecimalField
└── orden: PositiveIntegerField

Alternativa
├── pregunta: ForeignKey(Pregunta)
├── texto: CharField
└── es_correcta: BooleanField

IntentoEvaluacion
├── usuario: ForeignKey(Usuario)
├── evaluacion: ForeignKey(Evaluacion)
├── fecha_inicio: DateTimeField
├── fecha_fin: DateTimeField
├── puntaje_obtenido: DecimalField
├── porcentaje: DecimalField
├── aprobado: BooleanField
└── respuestas: JSONField

# certificados/models.py
Certificado
├── usuario: ForeignKey(Usuario)
├── curso: ForeignKey(Curso)
├── codigo_verificacion: UUIDField(unique)
├── fecha_emision: DateTimeField
├── fecha_expiracion: DateTimeField
└── pdf: FileField

# calendario/models.py
EventoCalendario
├── titulo: CharField
├── descripcion: TextField
├── tipo: CharField(clase_deadline/evaluacion_deadline/curso_start/curso_end/evento_general)
├── curso: ForeignKey(Curso, null=True)
├── fecha_inicio: DateTimeField
├── fecha_fin: DateTimeField
└── usuarios_asignados: ManyToManyField(Usuario)
```

**Instrucciones para el agente**:
1. Lee todos los archivos models.py
2. Crea un diagrama de clases en PlantUML
3. Agrupa las clases por app (package)
4. Muestra todas las relaciones con cardinalidad
5. Incluye métodos importantes (save, clean, custom methods)
6. Usa colores diferentes para cada app

---

### 2. Diagrama de Casos de Uso (Use Case Diagram)
**Archivo de salida**: `Diagrama de caso de uso.pdf`

**Actores**:
1. **Administrador**: Acceso total
2. **Docente**: Gestiona cursos propios
3. **Colaborador**: Participante
4. **Sistema**: Procesos automáticos

**Casos de uso por actor**:

**Administrador** (~12 casos):
- CRUD Usuarios (crear, editar, eliminar)
- Asignar cargos a usuarios
- Importar usuarios vía CSV
- CRUD Categorías de cursos
- CRUD Todos los cursos
- Inscribir usuarios a cursos
- Cancelar inscripciones
- Generar certificados manualmente
- Ver dashboard con estadísticas
- Generar reportes
- Crear anuncios
- Gestión de calendario

**Docente** (~10 casos):
- Crear curso
- Editar curso propio
- Publicar/borrador curso
- Crear clases
- Editar clases
- Subir materiales (PDF, video)
- Ordenar clases
- Crear evaluación
- Editar evaluación
- Ver reportes de cursos propios
- Inscribir usuarios a cursos propios

**Colaborador** (~8 casos):
- Ver cursos asignados
- Ver materiales del curso
- Completar clase (secuencial)
- Ver progreso del curso
- Tomar evaluación
- Ver resultado de evaluación
- Descargar certificado
- Ver calendario de eventos

**Sistema** (~4 casos):
- Enviar recordatorios automáticos
- Calificar evaluaciones automáticamente
- Generar certificados al aprobar
- Crear eventos de calendario automáticamente

**Relaciones a incluir**:
- `<<include>>`: Cuando un caso de uso SIEMPRE requiere otro
  - Ej: "Tomar evaluación" include "Verificar tiempo límite"
- `<<extend>>`: Cuando un caso de uso extiende otro bajo condición
  - Ej: "Generar certificado" extend "Tomar evaluación" (si aprueba)

**Instrucciones para el agente**:
1. Agrupa casos de uso por funcionalidad (packages)
2. Usa relaciones <<include>> para dependencias obligatorias
3. Usa relaciones <<extend>> para funcionalidades opcionales/condicionales
4. Asigna cada caso de uso al actor correcto

---

### 3. Diagrama de Actividad (Activity Diagram)
**Archivo de salida**: `DIAGRAMA DE ACTIVIDAD.pdf`

**Flujo a modelar**: Proceso completo desde inscripción hasta certificación

**Pasos**:

1. **Nodo Inicial** (círculo negro)

2. **Actividad**: "Colaborador solicita inscripción a curso"

3. **Decisión** (rombo): "¿Inscripción aprobada?"
   - [No] → "Notificar rechazo" → **Nodo Final**
   - [Sí] → Continuar

4. **Actividad**: "Sistema crea InscripcionCurso"

5. **Actividad**: "Asignar clases secuenciales"

6. **Bucle** (while): "¿Todas las clases completadas?"
   - [No] → Actividades:
     - "Mostrar clase N"
     - "Colaborador estudia contenido"
     - "Marcar clase N como completada"
     - "Desbloquear clase N+1"
     - Volver al bucle
   - [Sí] → Salir del bucle

7. **Actividad**: "Todas las clases completadas"

8. **Fork** (paralelo):
   - Rama 1: "Mostrar evaluación disponible"
   - Rama 2: "Notificar docente progreso completado"

9. **Actividad**: "Colaborador toma evaluación"

10. **Actividad**: "Sistema califica automáticamente"

11. **Actividad**: "Mostrar resultado"

12. **Decisión**: "¿Aprobó evaluación?"
    - [Sí] → Continuar a certificado
    - [No] → "Mostrar errores pregunta por pregunta" → Decisión: "¿Reintentos disponibles?"
      - [Sí] → "Permitir nuevo intento" → Volver a paso 9
      - [No] → "Notificar docente para revisión" → **Nodo Final**

13. **Actividad** (si aprobó): "Generar certificado automáticamente"

14. **Fork** (paralelo):
    - Rama 1: "Guardar PDF en servidor"
    - Rama 2: "Enviar email con certificado"
    - Rama 3: "Notificar en dashboard"

15. **Join**: Todas las ramas convergen

16. **Actividad**: "Curso completado exitosamente"

17. **Nodo Final** (círculo negro con borde)

**Instrucciones para el agente**:
1. Usa símbolos estándar UML para actividad
2. Incluye decisiones (rombos) con guardias [Sí]/[No]
3. Usa fork/join para actividades paralelas
4. Incluye un bucle while para completar clases secuencialmente
5. Usa swimlanes opcionalmente (Colaborador | Sistema | Docente)

---

### 4. Diagrama de Secuencia (Sequence Diagram)
**Archivo de salida**: `DIAGRAMA DE SECUENCIA.pdf`

**Escenario**: Flujo de evaluación completo

**Participantes** (de izquierda a derecha):
1. `Col` - Colaborador (actor)
2. `Web` - Navegador/Web App
3. `View` - Django View
4. `Eval` - Evaluacion Model
5. `Intento` - IntentoEvaluacion Model
6. `Cert` - Certificado Model

**Secuencia de mensajes**:

```
# Inicio de Evaluación
1. Col → Web: GET /evaluaciones/1/
2. Web → View: request
3. View → Eval: get(pk=1)
4. Eval --> View: evaluacion
5. View → Intento: get_or_create(usuario, evaluacion)
6. Intento --> View: intento
7. View --> Web: render(template)
8. Web --> Col: Mostrar evaluación con timer

# Colaborador Responde
9. Col → Web: POST respuestas
10. Web → View: POST request
11. View → Eval: calcular_puntaje(respuestas)
12. Eval --> View: puntaje, porcentaje
13. View → Intento: save(puntaje, porcentaje, aprobado)
14. Intento --> View: intento guardado

# Decisión: ¿Aprobó?
alt Aprobó (porcentaje >= minimo)
    15. View → Cert: create(usuario, curso, codigo)
    16. Cert --> View: certificado creado
    17. Cert → Cert: generar_pdf()
    18. Cert --> Cert: pdf guardado
    19. View → View: enviar_email_notificacion()
    20. View --> Web: redirect resultado (aprobado)
    21. Web --> Col: Mostrar resultado + descargar certificado
else No aprobó
    22. View --> Web: redirect resultado (no aprobado)
    23. Web --> Col: Mostrar resultado + preguntas incorrectas + intentos restantes
end
```

**Instrucciones para el agente**:
1. Muestra el flujo completo desde que el colaborador entra hasta que recibe resultado
2. Incluye un bloque `alt`/`else` para las dos ramas (aprobado/no aprobado)
3. Muestra activación de objetos (líneas de vida activas)
4. Incluye auto-mensajes (ej: Cert → Cert: generar_pdf())
5. Numera los mensajes para claridad

---

### 5. Diagrama de Componentes (Component Diagram)
**Archivo de salida**: `DIAGRAMA DE COMPONENTES.pdf`

**Nivel**: Arquitectura de alto nivel

**Capas a mostrar**:

**Capa de Presentación**:
- Componente: `Django Templates`
  - Base templates
  - Course templates
  - User templates
  - Evaluation templates
  - Certificate templates
- Componente: `Static Assets`
  - CSS (Tailwind)
  - JavaScript (Alpine.js, HTMX)
  - Bootstrap Icons

**Capa de Aplicación** (7 componentes):
- `cursos App`: Models (Curso, Clase, Material), Views, Templates
- `usuarios App`: Models (Usuario, AreaCargo), Views, Templates
- `evaluaciones App`: Models (Evaluacion, Pregunta, Intento), Views, Templates
- `certificados App`: Models (Certificado), Views, Templates
- `calendario App`: Models (EventoCalendario), Views, Templates
- `anuncios App`: Models (Anuncio), Views, Templates
- `reportes App`: Views (Dashboard), Templates

**Capa de Framework**:
- Componente: `Django Core`
  - Settings
  - URL Routing
  - Middleware
  - Authentication
- Componente: `Django ORM`
- Componente: `Django Admin`

**Capa de Datos**:
- Componente: `SQLite (Desarrollo)`
- Componente: `PostgreSQL (Producción)`

**Servicios Externos**:
- Componente: `WeasyPrint` (PDF generation)
- Componente: `Email Backend`
- Componente: `File Storage`

**Dependencias** (conectores):
- `<<use>>`: Cuando una app usa modelos de otra
  - evaluaciones → cursos (usa Curso)
  - certificados → cursos (usa Curso)
  - certificados → evaluaciones (usa IntentoEvaluacion)
  - calendario → cursos (usa Curso)
  - reportes → cursos, usuarios, evaluaciones
- `<<import>>`: Importación de Django
- Todas las apps → Django Core

**Instrucciones para el agente**:
1. Agrupa componentes por capa (colores diferentes)
2. Muestra interfaces explícitas (lollipops/cups opcional)
3. Usa conectores <<use>> para dependencias
4. Incluye notas con responsabilidades de cada app

---

### 6. Diagrama de Despliegue (Deployment Diagram)
**Archivo de salida**: `diagrama de despliegue.pdf`

**Entornos a mostrar**:

#### Entorno de Desarrollo (izquierda)
```
Node: Laptop del Desarrollador
├── Python 3.10+
├── Django 4.2
├── SQLite
└── Virtualenv

Node: Django Dev Server
    ├── cursos App
    ├── usuarios App
    ├── evaluaciones App
    ├── certificados App
    ├── calendario App
    ├── anuncios App
    └── reportes App
```

#### Entorno de Producción (derecha)
```
Node: Servidor Web (Ubuntu 22.04)
├── Nginx (Reverse Proxy, puertos 80/443)
│   └── proxy_pass a Gunicorn
├── Gunicorn (WSGI Server, puerto 8000)
│   └── Unix socket o puerto
│   └── Node: Django Application
│       ├── cursos App
│       ├── usuarios App
│       ├── evaluaciones App
│       ├── certificados App
│       ├── calendario App
│       ├── anuncios App
│       └── reportes App
├── PostgreSQL 14 (puerto 5432)
├── WeasyPrint + dependencias del sistema
│   ├── libcairo2
│   ├── libpango-1.0-0
│   └── libgobject-2.0-0
├── Media Storage (/var/www/kimun/media/)
├── Static Files (/var/www/kimun/static/)
└── Logs (/var/log/kimun/)
```

**Conexiones**:
```
Cliente Web --HTTPS--> Nginx --HTTP--> Gunicorn --WSGI--> Django App
                                              |
                                              v
                                        PostgreSQL
```

**Configuración de Nginx** (mostrar como nota o artifact):
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

**Instrucciones para el agente**:
1. Muestra dos nodos principales: Desarrollo y Producción
2. En producción, separa claramente: Nginx, Gunicorn, PostgreSQL
3. Incluye puertos y protocolos en las conexiones
4. Muestra artefactos: archivos de configuración
5. Incluye dependencias del sistema para WeasyPrint

---

## Validación Final

Antes de entregar, verificar:

### Diagrama de Clases
- [ ] Todos los modelos de las 6 apps están incluidos
- [ ] ForeignKeys tienen cardinalidad correcta
- [ ] Herencia de AbstractUser está marcada
- [ ] Cada clase tiene sus atributos principales

### Diagrama de Casos de Uso
- [ ] Los 3 roles humanos están como actores
- [ ] Sistema es actor para procesos automáticos
- [ ] Casos de uso agrupados por funcionalidad
- [ ] Relaciones <<include>> y <<extend>> correctas

### Diagrama de Actividad
- [ ] Flujo completo desde inscripción hasta certificado
- [ ] Decisiones (rombos) con guardias [Sí]/[No]
- [ ] Bucle para completar clases secuenciales
- [ ] Fork/join para actividades paralelas

### Diagrama de Secuencia
- [ ] 6+ participantes definidos
- [ ] Mensajes numerados cronológicamente
- [ ] Bloque alt/else para aprobado/no aprobado
- [ ] Auto-mensajes para operaciones internas

### Diagrama de Componentes
- [ ] 7 apps Django como componentes separados
- [ ] Capas claramente separadas (Presentación, Aplicación, Framework, Datos)
- [ ] Dependencias <<use>> entre apps
- [ ] Servicios externos incluidos

### Diagrama de Despliegue
- [ ] Nodos: Desarrollo y Producción
- [ ] En producción: Nginx, Gunicorn, PostgreSQL
- [ ] Conexiones con puertos y protocolos
- [ ] Artefactos de configuración
- [ ] Dependencias del sistema (WeasyPrint)

---

## Formato de Entrega

**Archivos requeridos**:
```
diagramas/
├── Diagrama de caso de uso.pdf
├── Diagrama de clases.pdf
├── DIAGRAMA DE ACTIVIDAD.pdf
├── DIAGRAMA DE SECUENCIA.pdf
├── DIAGRAMA DE COMPONENTES.pdf
└── diagrama de despliegue.pdf
```

**Formato**: PDF de alta calidad (vectorial preferido)

**Idioma**: Español (todos los nombres, etiquetas, notas)

---

## Ejemplo de Prompt para el Agente IA

```
Genera 6 diagramas UML para un proyecto Django LMS llamado Kimün.

CONTEXTO:
- Proyecto: Kimün - Plataforma de capacitación para ONG ALUMCO
- Stack: Django 4.2, Python 3.10+, SQLite/PostgreSQL
- Apps: usuarios, cursos, evaluaciones, certificados, calendario, anuncios, reportes
- Roles: Administrador, Docente, Colaborador

DIAGRAMAS A GENERAR:

1. DIAGRAMA DE CLASES (Diagrama de clases.pdf)
   - Lee todos los models.py
   - Muestra: Usuario, Curso, Clase, Material, Evaluacion, Pregunta, Alternativa, IntentoEvaluacion, Certificado, EventoCalendario
   - Relaciones ForeignKey con cardinalidad
   - Usuario extiende AbstractUser
   - Agrupa por app (package en PlantUML)

2. DIAGRAMA DE CASOS DE USO (Diagrama de caso de uso.pdf)
   - Actores: Administrador, Docente, Colaborador, Sistema
   - ~30 casos de uso agrupados por funcionalidad
   - Relaciones <<include>> y <<extend>>

3. DIAGRAMA DE ACTIVIDAD (DIAGRAMA DE ACTIVIDAD.pdf)
   - Flujo: Inscripción → Clases secuenciales → Evaluación → Certificado
   - Decisiones, bucles, forks paralelos

4. DIAGRAMA DE SECUENCIA (DIAGRAMA DE SECUENCIA.pdf)
   - Participantes: Colaborador, Web, View, Evaluacion, IntentoEvaluacion, Certificado
   - Flujo de tomar evaluación y generar certificado
   - Bloque alt/else para aprobado/no aprobado

5. DIAGRAMA DE COMPONENTES (DIAGRAMA DE COMPONENTES.pdf)
   - 7 apps Django
   - Capas: Presentación, Aplicación, Framework, Datos
   - Dependencias entre apps

6. DIAGRAMA DE DESPLIEGUE (diagrama de despliegue.pdf)
   - Nodos: Desarrollo y Producción
   - Producción: Nginx, Gunicorn, PostgreSQL
   - Puertos, protocolos, configuración

FORMATO: PlantUML (.puml) exportado a PDF
IDIOMA: Español
ENTREGA: 6 archivos PDF con nombres exactos
```

---

## Recursos Adicionales

### Referencias de PlantUML
- Guía oficial: plantuml.com/guide
- Diagrama de Clases: plantuml.com/class-diagram
- Diagrama de Casos de Uso: plantuml.com/use-case-diagram
- Diagrama de Secuencia: plantuml.com/sequence-diagram
- Diagrama de Actividad: plantuml.com/activity-diagram
- Diagrama de Componentes: plantuml.com/component-diagram
- Diagrama de Despliegue: plantuml.com/deployment-diagram

### Herramientas
- **Online**: plantuml.com/plantuml
- **VS Code**: Extensión "PlantUML" de jebbs
- **Docker**: `docker run plantuml/plantuml -tpdf *.puml`

---

*Documento generado para replicar diagramas UML del Proyecto Kimün*
*Fecha: Abril 2026*
