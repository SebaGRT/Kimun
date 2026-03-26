# Especificación de Proyecto: Kimün - Plataforma de Capacitación ONG ALUMCO

## 1. DIRECTIVA PRINCIPAL DE IDIOMA
**IMPORTANTE:** Este es un proyecto dirigido a una audiencia hispanohablante en Chile. 
* Toda la interfaz de usuario (UI), textos, alertas, correos electrónicos y certificados generados deben estar estrictamente en **Español**.
* Los nombres de los modelos de base de datos, variables principales y comentarios en el código deben mantenerse preferentemente en español o en un formato bilingüe claro para facilitar el mantenimiento por parte del equipo universitario local.

## 2. Resumen del Proyecto
* **Nombre del Sistema:** Kimün.
* [cite_start]**Cliente:** ONG ALUMCO (Organización que trabaja con Adultos Mayores en residencias ELEAM) [cite: 1-4, 8].
* [cite_start]**Objetivo:** Diseño e Implementación de una Aplicación de Capacitación Interna para la Gestión del Aprendizaje Organizacional [cite: 5-7]. [cite_start]El sistema busca centralizar, organizar y optimizar los procesos formativos del personal [cite: 11][cite_start], reduciendo costos [cite: 38] [cite_start]y permitiendo la trazabilidad para auditorías[cite: 36].

## 3. Stack Tecnológico Definido
* **Backend:** Python con el framework Django.
* **Frontend:** Django Templates (Server-Side Rendering).
* **Estilos:** Bootstrap 5 o Tailwind CSS (Enfoque estricto en Web-Responsive y Accesibilidad para adultos mayores/presbicia).
* **Interactividad (Frontend ligero):** HTMX y/o Alpine.js (para evitar recargas de página en cuestionarios sin necesidad de usar React/Vue).
* **Base de Datos:** SQLite (Desarrollo local) / PostgreSQL (Producción).
* **Generación de PDFs:** WeasyPrint (o similar) para la emisión de certificados HTML a PDF.
* **Despliegue planeado:** Render o Railway.

## 4. Perfiles de Usuario
[cite_start]La aplicación contará con tres perfiles principales[cite: 12]:
1. [cite_start]**Perfil Administrador (Empleadora):** Encargado de gestionar usuarios, asignar capacitaciones por cargo, emitir certificados, monitorear avances y generar reportes de cumplimiento [cite: 13-21].
2. **Perfil Docente (Área Académica):** Encargado de crear los módulos de los cursos, subir material formativo (manuales, videos, normativas) y estructurar las evaluaciones.
3. [cite_start]**Perfil Usuario (Colaborador/a):** Accede a las capacitaciones asignadas, descarga/visualiza material, realiza evaluaciones en línea y obtiene certificados digitales al aprobar [cite: 22-25].

## 5. Requerimientos Funcionales Core
* Autenticación segura de usuarios (Login/Logout).
* CRUD de Cursos y Módulos de Material (soporte para enlaces de video y subida de archivos PDF).
* Motor de Evaluaciones: Creación de test de alternativas con corrección automática.
* [cite_start]Lógica de Aprobación: Si el usuario supera el % de corte en la evaluación, el curso se marca como aprobado [cite: 24-25].
* [cite_start]Generador de Certificados: Creación automática de un diploma en PDF al aprobar, con código de verificación [cite: 43-44].
* [cite_start]Panel de Reportes: Vista para exportar el nivel de cumplimiento normativo del personal[cite: 36].

## 6. Arquitectura de Base de Datos Propuesta (Modelos Django)

Se sugiere dividir el proyecto en las siguientes apps de Django: `usuarios`, `cursos`, `evaluaciones` y `certificados`.

### App: Usuarios
* **Area_Cargo:** `id`, `nombre`
* **Usuario (Extiende AbstractUser):** `rut` (unique), `rol` (Admin, Docente, Colaborador), `cargo` (FK a Area_Cargo).

### App: Cursos
* **Curso:** `id`, `titulo`, `descripcion`, `docente_creador` (FK), `estado` (Borrador/Publicado), `fecha_creacion`.
* **Material:** `id`, `curso` (FK), `titulo`, `tipo` (PDF, Video_URL), `archivo`, `url`.
* **Inscripcion_Curso:** `usuario` (FK), `curso` (FK), `estado` (Asignado, En Progreso, Completado), `fecha_asignacion`.

### App: Evaluaciones
* **Evaluacion:** `id`, `curso` (FK), `titulo`, `porcentaje_aprobacion` (Integer, ej: 70).
* **Pregunta:** `id`, `evaluacion` (FK), `texto`.
* **Alternativa:** `id`, `pregunta` (FK), `texto`, `es_correcta` (Booleano).
* **Intento_Evaluacion:** `usuario` (FK), `evaluacion` (FK), `puntaje_obtenido`, `aprobado` (Booleano), `fecha_intento`.

### App: Certificados
* **Certificado:** `id`, `usuario` (FK), `curso` (FK), `codigo_verificacion` (UUID), `fecha_emision`, `archivo_pdf`.

## 7. Notas Adicionales para el Asistente de Código
* **Accesibilidad:** Mantener un contraste alto y tamaños de fuente legibles (mínimo 16px base) en el frontend.
* **Escalabilidad:** Separar la lógica pesada (como la generación del PDF del certificado) en funciones independientes o utilidades para no bloquear las vistas principales.
* **Estandarización:** Utilizar el sistema de permisos y grupos integrado de Django (`django.contrib.auth`) para manejar la lógica de los Perfiles (Admin, Docente, Usuario).
