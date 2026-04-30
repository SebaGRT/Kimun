# Plan: Diagramas de Arquitectura y Modelo de Datos - Kimün LMS

## TL;DR

> **Quick Summary**: Crear dos diagramas en PlantUML: (1) Diagrama de Arquitectura de Software en capas que refleje la estructura real del proyecto Kimün, y (2) Modelo de Base de Datos con notaciones Barker y Chen mostrando entidades principales con atributos clave.
>
> **Deliverables**:
> - `docs/diagrams/diagrama_arquitectura_capas.puml` - Diagrama de Arquitectura en Capas
> - `docs/diagrams/diagrama_modelo_datos_barker.puml` - Modelo Lógico (Notación Barker)
> - `docs/diagrams/diagrama_modelo_datos_chen.puml` - Modelo Conceptual (Notación Chen)
>
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 2 waves
> **Critical Path**: Arquitectura → Modelo de Datos

---

## Context

### Original Request
El usuario necesita: (1) un diagrama de arquitectura de software en capas basado en el PDF de la materia, reflejando la estructura real del proyecto Kimün, y (2) un modelo de base de datos conceptual y lógico con notaciones Barker y Chen.

### Investigation Findings

**Del PDF "ARQUITECTURA DE SOFTWARE"**:
- Estilos cubiertos: Capas, Cliente-Servidor, Monolítica, Microservicios, Event-Driven, MVC
- El ejemplo de ONG (capacitaciones) es directamente relevante a Kimün
- La arquitectura en capas tiene: Presentación → Aplicación/Negocio → Persistencia/Datos
- MVC se describe como: Vista → Modelo → Controlador

**De la estructura real del proyecto Kimün**:
- Django MTZ (Model-Template-View): análogo a MVC
- 7 apps: usuarios, cursos, evaluaciones, certificados, calendario, anuncios, tareas
- 15 modelos con relaciones ForeignKey
- Base de datos: SQLite (desarrollo) / PostgreSQL (producción)
- Frontend: Django Templates + Tailwind CSS + Alpine.js
- Servicios: WeasyPrint (PDF), Chart.js (gráficos)

### Decisions
- **Notación**: Barker (modelo lógico) Y Chen (modelo conceptual) - AMBAS
- **Nivel de detalle**: Entidades principales con atributos clave (PKs, FKs, campos importante)
- **Formato**: PlantUML (.puml) - consistente con diagramas existentes
- **Arquitectura**: En capas (Layered) reflejando la estructura MTZ de Django

---

## Work Objectives

### Core Objective
Crear diagramas profesionales y precisos en PlantUML que documenten la arquitectura y el modelo de datos de Kimün LMS, en español, siguiendo las convenciones del proyecto.

### Concrete Deliverables
- `docs/diagrams/diagrama_arquitectura_capas.puml` - Arquitectura en 4 capas
- `docs/diagrams/diagrama_modelo_datos_barker.puml` - Modelo lógico Barker
- `docs/diagrams/diagrama_modelo_datos_chen.puml` - Modelo conceptual Chen

### Definition of Done
- [x] Diagramas generan sin errores en PlantUML (syntax check exit 0)
- [x] Nombres de entidades/coomponentes coinciden con código real
- [x] Relaciones ForeignKey son correctas en dirección y cardinalidad
- [x] Todo el texto está en español
- [x] Convenciones de colores del proyecto respetadas

### Must Have
- Arquitectura en capas: Presentación → Lógica/Negocio → Acceso a Datos → Base de Datos
- Modelo Barker: entidades con atributos, PKs subrayadas, FKs, cardinalidad crow's foot
- Modelo Chen: entidades (rectángulos), relaciones (rombos), atributos (óvalos), cardinalidad
- 15 entidades del modelo de datos con sus relaciones reales

### Must NOT Have (Guardrails)
- No inventar entidades que no existen en el código
- No usar nombres en inglés (todo en español)
- No copiar diagramas genéricos - deben reflejar Kimün específicamente
- No usar notación UML para arquitectura (usar diagrama de capas)

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** - ALL verification is agent-executed.

### QA Policy
Every task MUST include agent-executed QA scenarios:
- **PlantUML Syntax**: Render diagram with `java -jar plantuml.jar` or verify syntax online
- **Entity Accuracy**: Cross-check every entity name against`models.py` files
- **Relationship Accuracy**: Verify every ForeignKey direction and cardinality against source code

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately - architecture + data model research):
├── Task 1: Create layered architecture diagram [quick]
├── Task 2: Create Chen ER diagram (conceptual) [unspecified-high]
└── Task 3: Create Barker ER diagram (logical) [unspecified-high]

Wave FINAL (After ALL tasks — verify and update docs):
├── Task F1: Verify all PlantUML diagrams render correctly [quick]
└── Task F2: Update docs/diagrams/README.md with new diagrams [quick]
```

---

## TODOs

---

- [x] 1. Diagrama de Arquitectura en Capas

  **What to do**:
  - Create `docs/diagrams/diagrama_arquitectura_capas.puml`
  - Generate a 4-layer architecture diagram reflecting Kimün's actual structure
  - Layer 1 (Presentación): Django Templates, Tailwind CSS, Alpine.js, Chart.js, WeasyPrint templates
  - Layer 2 (Lógica de Negocio / Aplicación): 7 Django apps (usuarios, cursos, evaluaciones, certificados, calendario, anuncios, tareas) with their key views/functionalities
  - Layer 3 (Acceso a Datos): Django ORM, Models, Migrations, SQLite/PostgreSQL
  - Layer 4 (Base de Datos): SQLite (dev), PostgreSQL (prod), File Storage (media)
  - Show cross-cutting concerns: Authentication (LoginRequiredMixin, role decorators), Signals (email notifications), Middleware
  - Use colors from project conventions (LightBlue=presentation, LightGreen=application, LightYellow=framework, LightPink=data)
  - Arrows showing data flow between layers
  - All text in Spanish
  - Include a title and legend

  **Must NOT do**:
  - Do not use UML component diagram syntax (use layered box diagram)
  - Do not use English text anywhere
  - Do not add components that don't exist in the project

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: F1, F2
  - **Blocked By**: None

  **References** (CRITICAL):

  **Pattern References**:
  - `docs/diagrams/diagrama_componentes.puml` - Existing component diagram for style reference
  - `docs/diagrams/README.md` - Color conventions (LightBlue, LightGreen, LightYellow, LightPink, LightCyan)

  **Source Code References**:
  - `usuarios/models.py` - Usuario, AreaCargo, Recordatorio models
  - `cursos/models.py` - Curso, Categoria, Material, InscripcionCurso, Clase, ClaseCompletado models
  - `evaluaciones/models.py` - Evaluacion, Pregunta, Alternativa, IntentoEvaluacion, BancoPreguntas
  - `certificados/models.py` - Certificado model (with estado field: pendiente/aprobado/rechazado)
  - `calendario/models.py` - EventoCalendario, TipoEvento
  - `anuncios/models.py` - Anuncio, LecturaAnuncio
  - `tareas/models.py` - Tarea, EntregaTarea
  - `usuarios/decorators.py` - admin_required, docente_or_admin_required decorators
  - `kimun/settings.py` - Django apps configuration

  **Architecture References** (from PDF content):
  - Layered pattern: Presentación → Lógica → Persistencia
  - MVC equivalent for Django: Templates=View, Views=Controller, Models=Model
  - Cross-cutting: Authentication, Signals, Middleware

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: PlantUML syntax validation
    Tool: Bash
    Preconditions: PlantUML jar available or online validator
    Steps:
      1. Copy diagrama_arquitectura_capas.puml content
      2. Verify no syntax errors (balanced brackets, proper keywords)
      3. Verify all component names match real project entities
    Expected Result: Diagram has zero syntax errors and all entity names are real
    Evidence: .sisyphus/evidence/task-1-arquitectura-syntax.txt
  ```

  **Commit**: YES
  - Message: `docs: add layered architecture diagram`
  - Files: `docs/diagrams/diagrama_arquitectura_capas.puml`

---

- [x] 2. Modelo Conceptual - Notación Chen (ER)

  **What to do**:
  - Create `docs/diagrams/diagrama_modelo_datos_chen.puml`
  - Create a Chen-notation ER diagram showing the conceptual data model
  - Entities (rectángulos): Usuario, AreaCargo, Curso, Categoria, Material, InscripcionCurso, Clase, ClaseCompletado, Evaluacion, BancoPreguntas, Pregunta, Alternativa, IntentoEvaluacion, Certificado, EventoCalendario, Anuncio, LecturaAnuncio, Tarea, EntregaTarea, Recordatorio
  - Relationships (rombos): pertenece_a, inscrito_en, creado_por, contiene, responde_a, aprueba, etc.
  - Key attributes (óvalos): PKs and most important attributes per entity (max 5 per entity)
  - Cardinality labels on relationships (1:1, 1:N, N:M)
  - Inheritance: Usuario extends AbstractUser (show as special relationship)
  - All text in Spanish
  - Title: "Modelo Conceptual de Datos - Kimün LMS (Notación Chen)"

  **Must NOT do**:
  - Do not include ALL attributes per entity (max 5 key attrs including PK)
  - Do not use Barker notation (that's Task 3)
  - Do not use English text

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: F1, F2
  - **Blocked By**: None

  **References** (CRITICAL):

  **Source Code References** (READ ALL - these define the EXACT entities and relationships):
  - `usuarios/models.py:5-13` - AreaCargo entity (nombre)
  - `usuarios/models.py:16-38` - Usuario entity (rut, rol, cargo FK→AreaCargo, extends AbstractUser with username, email, first_name, last_name, password)
  - `usuarios/models.py:41-68` - Recordatorio entity (usuario FK→Usuario, curso FK→Curso, tipo, fecha_envio, unique_together=[usuario,curso,tipo])
  - `cursos/models.py:7-18` - Categoria entity (nombre, color, descripcion)
  - `cursos/models.py:21-50` - Curso entity (titulo, descripcion, categoria FK→Categoria, docente_creador FK→Usuario, estado, fecha_creacion, fecha_limite)
  - `cursos/models.py:53-70` - Material entity (curso FK→Curso, titulo, tipo, archivo, url)
  - `cursos/models.py:73-95` - InscripcionCurso entity (usuario FK→Usuario, curso FK→Curso, estado, fecha_asignacion, unique_together=[usuario,curso])
  - `cursos/models.py:98-123` - Clase entity (curso FK→Curso, titulo, contenido, orden, fecha_creacion, fecha_actualizacion, unique_together=[curso,orden])
  - `cursos/models.py:145-161` - ClaseCompletado entity (usuario FK→Usuario, clase FK→Clase, fecha_completado, unique_together=[usuario,clase])
  - `evaluaciones/models.py:5-18` - BancoPreguntas entity (nombre, descripcion, curso FK→Curso, creado_por FK→Usuario, es_publico, fecha_creacion)
  - `evaluaciones/models.py:21-34` - Evaluacion entity (curso FK→Curso, titulo, porcentaje_aprobacion, max_intentos, duracion_minutos, preguntas_por_intento)
  - `evaluaciones/models.py:37-47` - Pregunta entity (evaluacion FK→Evaluacion, banco FK→BancoPreguntas, texto)
  - `evaluaciones/models.py:50-60` - Alternativa entity (pregunta FK→Pregunta, texto, es_correcta)
  - `evaluaciones/models.py:63-77` - IntentoEvaluacion entity (usuario FK→Usuario, evaluacion FK→Evaluacion, puntaje_obtenido, aprobado, fecha_intento, hora_inicio, respuestas JSON)
  - `certificados/models.py:6-41` - Certificado entity (usuario FK→Usuario, curso FK→Curso, codigo_verificacion UUID, fecha_emision, archivo_pdf, estado [pendiente/aprobado/rechazado], fecha_aprobacion, aprobado_por FK→Usuario)
  - `calendario/models.py:5-30` - EventoCalendario entity (titulo, descripcion, tipo choices, fecha_inicio, fecha_fin, curso FK→Curso, evaluacion FK→Evaluacion, creado_por FK→Usuario, color)
  - `anuncios/models.py:5-29` - Anuncio entity (titulo, contenido, prioridad choices, curso FK→Curso, creado_por FK→Usuario, publicado, fecha_publicacion, fecha_expiracion, fecha_creacion)
  - `anuncios/models.py:32-41` - LecturaAnuncio entity (anuncio FK→Anuncio, usuario FK→Usuario, fecha_lectura, unique_together=[anuncio,usuario])
  - `tareas/models.py:5-20` - Tarea entity (curso FK→Curso, titulo, descripcion, fecha_limite, puntaje_maximo, creado_por FK→Usuario, fecha_creacion)
  - `tareas/models.py:23-46` - EntregaTarea entity (tarea FK→Tarea, estudiante FK→Usuario, archivo, comentario, fecha_entrega, estado choices, puntaje_obtenido, retroalimentacion, calificado_por FK→Usuario, fecha_calificacion, unique_together=[tarea,estudiante])

  **Chen Notation Reference**:
  - Entities: Rectangles with entity name
  - Relationships: Diamonds with relationship name
  - Attributes: Ovals connected to entities
  - PK attributes: Underlined in ovals
  - Cardinality: (1,1), (1,N), (N,M) labels on relationship lines
  - Inheritance: Triangle with "IS-A" label

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Entity count validation
    Tool: Bash
    Preconditions: Diagram file exists
    Steps:
      1. Count entity rectangles in diagram - must be 15-20
      2. Verify every model from models.py files has a corresponding entity
      3. Verify no invented entities exist
    Expected Result: Entity count matches source code models exactly
    Evidence: .sisyphus/evidence/task-2-chen-entities.txt

  Scenario: Relationship direction validation
    Tool: Bash
    Preconditions: Diagram file exists
    Steps:
      1. For each FK relationship, verify the "many" side points to the entity with the FK
      2. Check that FK→Usuario relationships point TO Usuario
      3. Check that FK→Curso relationships point TO Curso
    Expected Result: All relationship directions match source code ForeignKey directions
    Evidence: .sisyphus/evidence/task-2-chen-relationships.txt
  ```

  **Commit**: YES
  - Message: `docs: add Chen ER conceptual data model diagram`
  - Files: `docs/diagrams/diagrama_modelo_datos_chen.puml`

---

- [x] 3. Modelo Lógico - Notación Barker

  **What to do**:
  - Create `docs/diagrams/diagrama_modelo_datos_barker.puml`
  - Create a Barker-notation logical data model diagram
  - Each entity as a box with:
    - Entity name in header (Spanish)
    - Primary key attributes underlined or marked with PK
    - Foreign key attributes marked with FK
    - Other key attributes (max 7 per entity)
    - Data types where relevant (CharField, IntegerField, DateTimeField, etc.)
  - Relationships with crow's foot notation:
    - One-to-one: straight line
    - One-to-many: line with crow's foot on many side
    - Many-to-many: usually through intermediate entity
  - Cardinality labels (1, N, 0..1, 1..*)
  - Normalize: Show all FK relationships explicitly
  - All text in Spanish
  - Title: "Modelo Lógico de Datos - Kimün LMS (Notación Barker)"

  **Must NOT do**:
  - Do not use Chen notation (rombos/óvalos) - this is Barker only
  - Do not include migration details or Django-specific fields (id auto-fields)
  - Do not use English text

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: F1, F2
  - **Blocked By**: None

  **References** (CRITICAL):

  **Use same source code references as Task 2** - all entities and relationships are identical, only the notation changes.

  **Barker Notation Reference**:
  - Entity: Rounded rectangle with name in header, attributes listed below
  - PK: Underlined attribute or marked with # prefix
  - FK: Marked with * or FK suffix
  - Mandatory attribute: Solid line from attribute to entity
  - Optional attribute: Dashed line (or marked with ○)
  - Relationship lines:
    - Solid line = mandatory
    - Dashed line = optional
    - Crow's foot = many
    - Single line = one
    - Bar across line = exactly one
  - Cardinality:
    - ──|── = exactly one (1)
    - ──○── = zero or one (0..1)
    - ──<── = one or many (1..*)
    - ──○<── = zero or many (0..*)

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: FK consistency check
    Tool: Bash
    Preconditions: Both Chen and Barker diagrams exist
    Steps:
      1. Extract all FK relationships from Barker diagram
      2. Compare FK count with source code ForeignKey fields
      3. Verify FK names match source code field names
    Expected Result: FK count and names match source code exactly
    Evidence: .sisyphus/evidence/task-3-barker-fks.txt

  Scenario: Cardinality validation
    Tool: Bash
    Preconditions: Diagram file exists
    Steps:
      1. Verify InscripcionCurso has N:1 with both Usuario and Curso
      2. Verify Certificado has N:1 with both Usuario and Curso
      3. Verify Pregunta has N:1 with Evaluacion and optional N:1 with BancoPreguntas
      4. Verify unique_together constraints are reflected (e.g., InscripcionCurso[usuario,curso])
    Expected Result: All cardinalities match source code relationships
    Evidence: .sisyphus/evidence/task-3-barker-cardinality.txt
  ```

  **Commit**: YES
  - Message: `docs: add Barker logical data model diagram`
  - Files: `docs/diagrams/diagrama_modelo_datos_barker.puml`

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

- [x] F1. **PlantUML Render Verification** — `quick` (ALL 3 PASS exit 0)
  Run PlantUML on all 3 new diagram files. Verify zero syntax errors. Verify all entity/component names match source code. Check Spanish language throughout.

- [x] F2. **Update README** — `quick` (already shows 9 diagrams)
  Update `docs/diagrams/README.md` to include the 3 new diagrams in the file table with descriptions and update the validation checklist.

---

## Commit Strategy

- **1**: `docs: add layered architecture diagram` — `docs/diagrams/diagrama_arquitectura_capas.puml`
- **2**: `docs: add Chen ER conceptual data model diagram` — `docs/diagrams/diagrama_modelo_datos_chen.puml`
- **3**: `docs: add Barker logical data model diagram` — `docs/diagrams/diagrama_modelo_datos_barker.puml`
- **4**: `docs: update diagrams README with new architecture and ER diagrams` — `docs/diagrams/README.md`

---

## Success Criteria

### Verification Commands
```bash
# Verify PlantUML syntax (if plantuml.jar available)
java -jar plantuml.jar -tcurl docs/diagrams/diagrama_arquitectura_capas.puml
java -jar plantuml.jar -tcurl docs/diagrams/diagrama_modelo_datos_chen.puml  
java -jar plantuml.jar -tcurl docs/diagrama_modelo_datos_barker.puml

# Verify all models are represented
grep -c "entity\|Entity\|class" docs/diagrams/diagrama_modelo_datos_chen.puml
grep -c "entity\|Entity\|class" docs/diagrams/diagrama_modelo_datos_barker.puml
```

### Final Checklist
- [x] Architecture diagram has 4 layers (Presentation, Business Logic, Data Access, Database)
- [x] Chen ER has 15-20 entities matching source code models
- [x] Barker diagram has PKs underlined and FKs marked
- [x] All relationship directions match source code ForeignKey fields
- [x] All text in Spanish
- [x] README.md updated with new diagram entries