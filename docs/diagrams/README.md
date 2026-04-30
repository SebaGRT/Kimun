# Guía de Diagramas UML - Kimün LMS

Esta carpeta contiene los archivos fuente (.puml) para generar los 6 diagramas UML requeridos para el proyecto Kimün.

## Archivos Disponibles

| Diagrama | Archivo Fuente | Descripción |
|----------|---------------|-------------|
| Diagrama de Arquitectura en Capas | `diagrama_arquitectura_capas.puml` | Arquitectura 4 capas del sistema |
| Diagrama de Clases | `diagrama_clases.puml` | Modelos Django y sus relaciones |
| Diagrama de Casos de Uso | `diagrama_casos_uso.puml` | Actores y funcionalidades del sistema |
| Diagrama de Actividad | `diagrama_actividad.puml` | Flujo de inscripción y certificación |
| Diagrama de Secuencia | `diagrama_secuencia.puml` | Interacción en el flujo de evaluación |
| Diagrama de Componentes | `diagrama_componentes.puml` | Arquitectura de componentes Django |
| Diagrama de Despliegue | `diagrama_despliegue.puml` | Infraestructura de producción |
| Modelo Conceptual (Chen) | `diagrama_modelo_datos_chen.puml` | Entidades y relaciones - Notación Chen |
| Modelo Lógico (Barker) | `diagrama_modelo_datos_barker.puml` | Atributos y cardinalidad - Notación Barker |

**Total: 9 diagramas**

---

## Cómo Generar los PDFs

### Opción 1: PlantUML Online (Recomendado)

1. Ve a **www.plantuml.com/plantuml**
2. Copia y pega el contenido del archivo `.puml`
3. Click en "Submit"
4. Descarga como PDF o PNG

### Opción 2: Extensión VS Code

1. Instala la extensión **"PlantUML"** de jebbs
2. Abre cualquier archivo `.puml`
3. Presiona `Alt+D` para vista previa
4. Click derecho → "Export Current Diagram" → Selecciona PDF

### Opción 3: Línea de Comandos (Requiere Java)

```bash
# Instalar PlantUML
wget https://github.com/plantuml/plantuml/releases/download/v1.2023.10/plantuml-1.2023.10.jar

# Generar PDF
cd docs/diagrams
java -jar plantuml.jar -tpdf diagrama_arquitectura_capas.puml
java -jar plantuml.jar -tpdf diagrama_clases.puml
java -jar plantuml.jar -tpdf diagrama_casos_uso.puml
java -jar plantuml.jar -tpdf diagrama_actividad.puml
java -jar plantuml.jar -tpdf diagrama_secuencia.puml
java -jar plantuml.jar -tpdf diagrama_componentes.puml
java -jar plantuml.jar -tpdf diagrama_despliegue.puml
java -jar plantuml.jar -tpdf diagrama_modelo_datos_chen.puml
java -jar plantuml.jar -tpdf diagrama_modelo_datos_barker.puml
```

### Opción 4: Docker

```bash
cd docs/diagrams

# Generar todos los PDFs
docker run -v $(pwd):/data plantuml/plantuml -tpdf *.puml

# Los PDFs se guardarán en la misma carpeta
```

---

## Convenciones Utilizadas

### Colores por Capa
- **LightBlue**: Capa de presentación (Templates, Static)
- **LightGreen**: Capa de aplicación (Apps Django)
- **LightYellow**: Capa de framework (Django Core)
- **LightPink**: Capa de datos (Base de datos)
- **LightCyan**: Servicios externos

### Notación
- **Clases**: CamelCase (ej: `InscripcionCurso`)
- **Métodos**: snake_case (ej: `calcular_puntaje()`)
- **Relaciones**: Cardinalidad explícita (1, *, 1..*)
- **Actores**: Representados con `actor` keyword

---

## Estructura de los Diagramas

### 1. Diagrama de Arquitectura en Capas
**Arquitectura:** Sistema en 4 capas (Layered Architecture)
- Capa 4 - Presentación: Django Templates, Tailwind CSS, Alpine.js, Chart.js
- Capa 3 - Lógica de Negocio: 7 apps Django con sus funcionalidades
- Capa 2 - Acceso a Datos: Django ORM, Models, Migrations
- Capa 1 - Base de Datos: SQLite (dev) / PostgreSQL (prod)
- Cross-cutting: Authentication, Signals, Middleware

### 2. Diagrama de Clases
**Muestra:**
- 8 modelos principales (Usuario, Curso, Evaluacion, etc.)
- Relaciones ForeignKey, ManyToMany
- Métodos importantes de cada modelo
- Herencia (Usuario extends AbstractUser)

### 3. Diagrama de Casos de Uso
**Muestra:**
- 4 actores: Administrador, Docente, Colaborador, Sistema
- ~25 casos de uso agrupados por funcionalidad
- Relaciones <<include>> y <<extend>>
- Permisos por rol

### 4. Diagrama de Actividad
**Flujo:** Inscripción → Clases → Evaluación → Certificado
- Decisiones: ¿Aprobado?, ¿Reintentos disponibles?
- Forks paralelos: Email + Notificación + PDF
- Bucle: Completar clases secuencialmente

### 5. Diagrama de Secuencia
**Escenario:** Tomar evaluación
- Participantes: Colaborador, Navegador, Views, Models
- Mensajes: GET evaluación, POST respuestas, Generar certificado
- Alt/Else: Aprobado vs No aprobado

### 6. Diagrama de Componentes
**Arquitectura:**
- Capa de presentación (Templates, Static)
- 7 Apps Django con sus responsabilidades
- Capa de framework (Django Core)

### 7. Diagrama de Despliegue
**Infraestructura:**
- Nginx (reverse proxy)
- Gunicorn (WSGI server)
- Django Application
- PostgreSQL
- WeasyPrint + dependencias del sistema

### 8. Modelo Conceptual (Chen)
**Notación:** Entidad-Relación (Chen)
- Entidades: Rectángulos con nombres
- Relaciones: Diamantes con nombres
- Atributos: Óvalos conectados a entidades
- PKs: Óvalos dobles o subrayados
- Muestra: 15+ entidades con relaciones y cardinalidad

### 9. Modelo Lógico (Barker)
**Notación:** Barker con crow's foot
- Entidades: Cajas con atributos
- PKs: Subrayadas o marcadas con #
- FKs: Marcadas con * o FK
- Cardinalidad: Crow's foot (|, <, O)
- Detalle: Tipos de datos, restricciones UNIQUE
- Servicios externos (PDF, Email)

### 6. Diagrama de Despliegue
**Infraestructura:**
- Nginx (reverse proxy)
- Gunicorn (WSGI server)
- Django Application
- PostgreSQL
- WeasyPrint + dependencias del sistema

---

## Validación

Antes de entregar, verifica:

- [ ] Todos los 6 diagramas generan sin errores
- [ ] Los PDFs son legibles y de buena calidad
- [ ] Los nombres de clases coinciden con el código
- [ ] Las relaciones son correctas (ForeignKey direcciones)
- [ ] Los actores tienen los permisos correctos
- [ ] La secuencia refleja el flujo real del código

---

## Troubleshooting

### Error: "Cannot find Graphviz"
PlantUML requiere Graphviz para algunos diagramas:
```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# Mac
brew install graphviz

# Windows
choco install graphviz
```

### Error: "Syntax error"
- Verificar que no hay espacios en blanco al final de líneas
- Asegurar que las llaves `{}` estén balanceadas
- Verificar keywords válidos de PlantUML

### PDF se ve cortado
- Aumentar el tamaño del canvas: `skinparam maxMessageSize 200`
- Usar dirección `left to right` en lugar de `top to bottom`
- Dividir diagramas muy grandes en varios

---

## Referencias

- **PlantUML Guide**: plantuml.com/guide
- **Diagrama de Clases**: plantuml.com/class-diagram
- **Diagrama de Casos de Uso**: plantuml.com/use-case-diagram
- **Diagrama de Secuencia**: plantuml.com/sequence-diagram
- **Diagrama de Actividad**: plantuml.com/activity-diagram
- **Diagrama de Componentes**: plantuml.com/component-diagram
- **Diagrama de Despliegue**: plantuml.com/deployment-diagram

---

*Generado para el Proyecto Kimün - Abril 2026*