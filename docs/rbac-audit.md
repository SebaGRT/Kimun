# RBAC Inline Role Check Audit

Scope: all `views.py` files across `usuarios`, `cursos`, `evaluaciones`, `certificados`, `reportes`, `calendario`, `anuncios`, `tareas`.

## Summary
- Total inline `request.user.rol` occurrences: **63**
- Files with matches: **7**
- Files with no matches: `reportes/views.py`

### Decorators/mixins referenced
- Decorators: `role_required`, `admin_required`, `docente_or_admin_required`, `course_owner_or_admin`
- Mixins: `RoleRequiredMixin`, `AdminRequiredMixin`, `DocenteOrAdminRequiredMixin`, `CourseOwnerOrAdminMixin`

### Risk guide
- **low**: feature gating / queryset filtering / display logic
- **medium**: object-specific gate with limited blast radius
- **high**: direct access-control gate on sensitive actions or ownership checks

---

## /home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/usuarios/views.py
Occurrences: **5**

- **L67** `if request.user.rol == 'admin':` — **c** — keep inline (dashboard aggregation for admins only) — **low**
- **L84** `elif request.user.rol == 'docente':` — **c** — keep inline (dashboard aggregation for docentes) — **low**
- **L89** `if request.user.rol in ['colaborador', 'docente']:` — **c** — keep inline (personal dashboard data block) — **low**
- **L124** `if request.user.rol == 'admin':` — **c** — keep inline (role-based course listing) — **low**
- **L132** `elif request.user.rol == 'docente':` — **c** — keep inline (role-based course listing) — **low**

## /home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/cursos/views.py
Occurrences: **26**

- **L16** `if request.user.rol == 'colaborador':` — **c** — keep inline (redirect/UX gating) — **low**
- **L22** `if request.user.rol in ['admin', 'docente']:` — **c** — keep inline (queryset selection) — **low**
- **L45** `'is_docente': request.user.rol in ['admin', 'docente'],` — **c** — keep inline (template context flag) — **low**
- **L61** `if request.user.rol == 'docente':` — **c** — keep inline (default creator assignment) — **low**
- **L109** `if request.user.rol not in ['admin', 'docente']:` — **d** — keep inline (draft-course access depends on role + enrollment) — **high**
- **L111** `if request.user.rol == 'docente' and curso.docente_creador != request.user:` — **d** — keep inline (draft-course access depends on creator ownership) — **high**
- **L121** `if request.user.rol == 'colaborador':` — **c** — keep inline (per-user progress state) — **low**
- **L137** `if request.user.rol == 'colaborador':` — **c** — keep inline (course progress calculation) — **low**
- **L152** `puede_editar = request.user.rol == 'admin' or (` — **c** — keep inline (template permission flag) — **low**
- **L153** `request.user.rol == 'docente' and curso.docente_creador == request.user` — **c** — keep inline (template permission flag) — **low**
- **L214** `if request.user.rol == 'docente' and curso.docente_creador != request.user:` — **b** — needs new decorator (`material_course_owner_or_admin`; current `course_owner_or_admin` cannot target `material.pk`) — **high**
- **L292** `if request.user.rol not in ['admin', 'docente']:` — **d** — keep inline (draft-course access depends on role + enrollment) — **high**
- **L294** `if request.user.rol == 'docente' and curso.docente_creador != request.user:` — **d** — keep inline (draft-course access depends on creator ownership) — **high**
- **L297** `if request.user.rol == 'colaborador':` — **c** — keep inline (enrollment gate) — **low**
- **L303** `puede_editar = request.user.rol == 'admin' or (` — **c** — keep inline (template permission flag) — **low**
- **L304** `request.user.rol == 'docente' and curso.docente_creador == request.user` — **c** — keep inline (template permission flag) — **low**
- **L310** `if request.user.rol == 'colaborador':` — **c** — keep inline (completion state for collaborators) — **low**
- **L361** `if request.user.rol not in ['admin', 'docente']:` — **d** — keep inline (draft-course access depends on role + enrollment) — **high**
- **L363** `if request.user.rol == 'docente' and curso.docente_creador != request.user:` — **d** — keep inline (draft-course access depends on creator ownership) — **high**
- **L366** `if request.user.rol == 'colaborador':` — **c** — keep inline (enrollment gate) — **low**
- **L370** `puede_editar = request.user.rol == 'admin' or (` — **c** — keep inline (template permission flag) — **low**
- **L371** `request.user.rol == 'docente' and curso.docente_creador == request.user` — **c** — keep inline (template permission flag) — **low**
- **L379** `if request.user.rol == 'colaborador':` — **c** — keep inline (completion state for collaborators) — **low**
- **L407** `if request.user.rol == 'docente' and curso.docente_creador != request.user:` — **b** — needs new decorator (`class_course_owner_or_admin`; current `course_owner_or_admin` cannot target `clase.pk`) — **high**
- **L436** `if request.user.rol == 'docente' and curso.docente_creador != request.user:` — **b** — needs new decorator (`class_course_owner_or_admin`; current `course_owner_or_admin` cannot target `clase.pk`) — **high**
- **L458** `if request.user.rol != 'colaborador':` — **a** — replaceable with existing `@role_required('colaborador')` — **medium**

## /home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/evaluaciones/views.py
Occurrences: **8**

- **L60** `if request.user.rol == 'docente' and curso.docente_creador != request.user:` — **a** — replaceable with existing `@course_owner_or_admin` (has `curso_pk`) — **high**
- **L121** `if request.user.rol == 'docente' and curso.docente_creador != request.user:` — **b** — needs new decorator (`evaluation_course_owner_or_admin`; current `course_owner_or_admin` cannot target `evaluacion.pk`) — **high**
- **L191** `if request.user.rol == 'docente' and curso.docente_creador != request.user:` — **b** — needs new decorator (`evaluation_course_owner_or_admin`; current `course_owner_or_admin` cannot target `evaluacion.pk`) — **high**
- **L360** `if request.user.rol == 'admin':` — **c** — keep inline (admin-only queryset expansion) — **low**
- **L394** `if request.user.rol == 'docente' and banco.creado_por != request.user:` — **b** — needs new decorator (`banco_owner_or_admin`) — **high**
- **L415** `if request.user.rol == 'docente' and banco.creado_por != request.user:` — **b** — needs new decorator (`banco_owner_or_admin`) — **high**
- **L432** `if request.user.rol == 'docente' and banco.creado_por != request.user and not banco.es_publico:` — **d** — keep inline (ownership + public-visibility rule) — **high**
- **L446** `if request.user.rol == 'docente' and banco.creado_por != request.user:` — **b** — needs new decorator (`banco_owner_or_admin`) — **high**

## /home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/certificados/views.py
Occurrences: **8**

- **L29** `if request.user.rol == 'admin':` — **c** — keep inline (admin redirect) — **low**
- **L62** `if request.user.rol == 'docente' and curso.docente_creador != request.user:` — **a** — replaceable with existing `@course_owner_or_admin` (has `curso_pk`) — **high**
- **L102** `if request.user.rol == 'admin':` — **c** — keep inline (admin redirect) — **low**
- **L111** `if request.user != certificado.usuario and request.user.rol != 'admin':` — **b** — needs new decorator (`certificate_owner_or_admin`) — **high**
- **L172** `if request.user.rol == 'admin':` — **c** — keep inline (admin gets broader queryset) — **low**
- **L194** `if request.user.rol == 'docente' and certificado.curso.docente_creador != request.user:` — **b** — needs new decorator (`certificate_course_owner_or_admin`) — **high**
- **L215** `if request.user.rol == 'docente' and certificado.curso.docente_creador != request.user:` — **b** — needs new decorator (`certificate_course_owner_or_admin`) — **high**
- **L233** `if request.user.rol == 'docente' and certificado.curso.docente_creador != request.user:` — **b** — needs new decorator (`certificate_course_owner_or_admin`) — **high**

## /home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/calendario/views.py
Occurrences: **5**

- **L48** `if request.user.rol in ['admin', 'docente']:` — **c** — keep inline (calendar queryset split) — **low**
- **L109** `if request.user.rol in ['admin', 'docente']:` — **c** — keep inline (events API split) — **low**
- **L150** `if request.user.rol != 'admin' and evento.creado_por != request.user:` — **b** — needs new decorator (`event_owner_or_admin`) — **high**
- **L173** `if request.user.rol != 'admin' and evento.creado_por != request.user:` — **b** — needs new decorator (`event_owner_or_admin`) — **high**
- **L191** `if request.user.rol in ['admin', 'docente']:` — **c** — keep inline (iCal export split) — **low**

## /home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/anuncios/views.py
Occurrences: **4**

- **L15** `if request.user.rol not in ('admin', 'docente'):` — **c** — keep inline (publicado filter; data visibility, not access control) — **low**
- **L29** `if request.user.rol not in ('admin', 'docente') and not anuncio.publicado:` — **d** — keep inline (visibility gate combines role + publication state) — **high**
- **L59** `if request.user.rol == 'docente' and anuncio.creado_por != request.user:` — **b** — needs new decorator (`anuncio_owner_or_admin`) — **high**
- **L91** `if request.user.rol not in ('admin', 'docente') and not anuncio.publicado:` — **d** — keep inline (visibility gate combines role + publication state) — **high**

## /home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/tareas/views.py
Occurrences: **7**

- **L17** `if request.user.rol == 'colaborador':` — **c** — keep inline (enrollment check for collaborators) — **low**
- **L36** `if request.user.rol == 'colaborador':` — **c** — keep inline (enrollment check for collaborators) — **low**
- **L45** `if request.user.rol == 'colaborador':` — **c** — keep inline (loading collaborator-specific delivery state) — **low**
- **L62** `if request.user.rol == 'docente' and curso.docente_creador != request.user:` — **a** — replaceable with existing `@course_owner_or_admin` (has `curso_pk`) — **high**
- **L89** `if request.user.rol == 'docente' and tarea.creado_por != request.user:` — **b** — needs new decorator (`tarea_owner_or_admin`) — **high**
- **L113** `if request.user.rol == 'docente' and tarea.creado_por != request.user:` — **b** — needs new decorator (`tarea_owner_or_admin`) — **high**
- **L168** `if request.user.rol == 'docente' and entrega.tarea.creado_por != request.user:` — **b** — needs new decorator (`entrega_task_owner_or_admin`) — **high**

## /home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/reportes/views.py
Occurrences: **0**

- No inline `request.user.rol` checks found.

## Recommended follow-up
- Convert the repeated ownership checks into object-specific decorators where possible (`*_owner_or_admin`).
- Leave role-based queryset/display gating inline when it is only shaping visibility or dashboard content.
- Consider CBV mixins (`AdminRequiredMixin`, `DocenteOrAdminRequiredMixin`, `CourseOwnerOrAdminMixin`) only if these views are refactored from FBV to CBV.
