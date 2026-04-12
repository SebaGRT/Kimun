# Kimün UI Redesign — Anti-AI-Slop Makeover

## TL;DR

> **Quick Summary**: Medium visual refresh of the Kimün LMS platform to reduce AI-generated look while preserving the core design system. Add personality through asymmetric layouts, custom SVG illustrations, tasteful animations, and refined component styles.
> 
> **Deliverables**:
> - New `static/css/kimun.css` component stylesheet
> - Global Alpine.js inclusion in `base.html`
> - Redesigned homepage (`inicio.html`) with hero section
> - Redesigned dashboard (`reportes/dashboard.html`)
> - ~25 template modifications for visual refresh
> - 8-10 inline SVG illustrations for empty states
> - Animation pattern library (stagger, float, slide)
> 
> **Estimated Effort**: Medium (1-2 weeks)
> **Parallel Execution**: YES - 5 waves | NO - sequential
> **Critical Path**: Wave 1 (infrastructure) → Wave 2 (homepage) → Wave 3 (dashboard) → Wave 4 (templates) → Wave 5 (polish)

---

## Context

### Original Request
User asked to "plan how the interface could be improved, and use design subagents to get a less AI-generated look to the project, whilst keeping the core design."

### Interview Summary
**Key Discussions**:
- Redesign scope: **Medium refresh** (~25-30 template changes + new CSS)
- Illustrations: **Yes, inline SVGs** for empty states and hero sections (first-aid/medical themed)
- Priority pages: **Dashboard + Home** first
- Animations: **Yes, tasteful** (Alpine.js-based transitions, hover lifts, stagger fades)

**Research Findings**:
- Anti-AI patterns: asymmetric grids, intentional radius variation, organic SVG backgrounds, micro-interactions, spacing rhythm
- Chilean/LatAm design: warm colors (terracotta, sage, amber), community-focused, accessible typography
- Current UI symptoms: symmetric cards everywhere, `rounded-xl` uniformity, no illustrations, utility-class soup

### Metis Review
**Identified Gaps (addressed)**:
- Alpine.js NOT globally available → Decision: load globally in `base.html`
- SVG illustrations are a NEW pattern → Decision: coexist with Bootstrap Icons, illustrated states only
- CSS variables inline in `base.html` → Decision: keep there, add NEW styles to `kimun.css`
- 50 templates use `hybrid-card` → Decision: redesign ~25-30 high-impact, minor tweaks on rest
- Empty states text-only → Decision: add SVG illustrations to 8-10 key templates

---

## Work Objectives

### Core Objective
Reduce AI-generated visual patterns across the Kimün platform by introducing asymmetric layouts, custom SVG illustrations, tasteful micro-interactions, and intentional design variations — while preserving the existing CSS variable system, dark mode support, and component base.

### Concrete Deliverables
- `static/css/kimun.css` — new component stylesheet with refined styles
- Global Alpine.js load in `base.html`
- Redesigned homepage with hero section and SVG illustration
- Redesigned dashboard with asymmetric layout and Chart.js polish
- ~25 template modifications for visual freshness
- 8-10 SVG illustrations for empty states
- Animation pattern library

### Definition of Done
- [ ] Homepage loads with hero section, SVG illustration, and stagger animations
- [ ] Dashboard renders with asymmetric card layout in both light and dark mode
- [ ] All 8-10 SVG illustrations render correctly
- [ ] Dark mode toggle works on all redesigned pages
- [ ] Mobile responsiveness verified at 320px, 375px, 768px widths
- [ ] `prefers-reduced-motion` disables animations
- [ ] `static/css/kimun.css` file size < 30KB
- [ ] No hardcoded color values (all use `var(--color-*)`)
- [ ] 286 existing tests still pass

### Must Have
- Preserve existing `hybrid-card`, `btn-primary`, `btn-outline`, `input-field` classes
- Preserve `data-theme="light|dark"` toggle mechanism
- Preserve all existing CSS variable names
- All text in Spanish
- Tailwind CDN (no build pipeline)
- Accessible: all animations honor `prefers-reduced-motion`

### Must NOT Have (Guardrails)
- NO new JavaScript frameworks (React, Vue, Svelte, etc.)
- NO build pipeline changes (no PostCSS, no npm build step)
- NO backend changes (no view/model/url changes)
- NO new dependencies beyond Alpine.js (already partially used)
- NO removal of existing component classes (`hybrid-card`, etc.)
- NO utility classes that duplicate Tailwind
- NO hardcoded color values (must use `var(--color-*)`)
- NO animations on every element — only "signature moments"
- NO multiple animation timing functions — use `0.2s ease` and `0.3s ease`

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: YES (Django test suite)
- **Automated tests**: NO (visual changes don't break logic)
- **Framework**: N/A
- **Agent-Executed QA**: ALWAYS (Playwright for visual, Django test for non-regression)

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Frontend/UI**: Use Playwright — navigate, screenshot, verify elements exist
- **Dark mode**: Toggle theme, screenshot, verify color vars applied
- **Mobile**: Viewport resize to 375px, screenshot, verify layout collapses
- **Accessibility**: Verify `prefers-reduced-motion` disables animations
- **Non-regression**: Run `python manage.py test` after each wave

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Foundation — MUST complete first):
├── Task 1: Create kimun.css with component styles + animation patterns [quick]
├── Task 2: Add Alpine.js globally to base.html [quick]
└── Task 3: Create SVG illustration library [visual-engineering]

Wave 2 (Homepage — signature moment):
└── Task 4: Redesign inicio.html with hero section and SVG illustration [visual-engineering]

Wave 3 (Dashboard — asymmetric layout):
├── Task 5: Redesign reportes/dashboard.html with asymmetric layout [visual-engineering]
└── Task 6: Refine Chart.js integration and at-risk table [visual-engineering]

Wave 4 (High-Impact Pages — MAX PARALLEL):
├── Task 7: Redesign curso_list.html (course cards with asymmetric layout) [visual-engineering]
├── Task 8: Redesign curso_detail.html (split layout with progress indicators) [visual-engineering]
├── Task 9: Redesign evaluacion_list.html + tomar_evaluacion.html (exam experience) [visual-engineering]
├── Task 10: Redesign tarea_list.html + tarea_detail.html (assignment cards) [visual-engineering]
├── Task 11: Redesign login.html (auth page with illustration) [visual-engineering]
└── Task 12: Redesign calendario.html (calendar visual refresh) [visual-engineering]

Wave 5 (Polish + Empty States):
├── Task 13: Add SVG empty states to all list pages (8-10 templates) [visual-engineering]
├── Task 14: Refine form pages (consistent spacing + visual hierarchy) [visual-engineering]
└── Task 15: Final pass — mobile responsiveness + dark mode parity [visual-engineering]

Wave FINAL (Verification — after ALL implementation):
├── Task F1: Visual regression via Playwright (all redesigned pages) [unspecified-high]
├── Task F2: Dark mode parity check (all redesigned pages) [unspecified-high]
├── Task F3: Accessibility + performance audit [unspecified-high]
└── Task F4: Non-regression test suite (python manage.py test) [quick]
```

### Dependency Matrix

- **1,2,3**: No blockers (Wave 1)
- **4**: Depends on 1,3 (needs CSS + SVG library)
- **5,6**: Depends on 1 (needs CSS)
- **7-12**: Depends on 1,3 (needs CSS + SVG library)
- **13**: Depends on 3 (needs SVG library)
- **14**: Depends on 1 (needs CSS)
- **15**: Depends on 7-14 (needs all pages done)
- **F1-F4**: Depends on ALL tasks

### Agent Dispatch Summary

- **Wave 1**: 2x quick + 1x visual-engineering
- **Wave 2**: 1x visual-engineering
- **Wave 3**: 2x visual-engineering
- **Wave 4**: 6x visual-engineering (parallel)
- **Wave 5**: 3x visual-engineering
- **FINAL**: 3x unspecified-high + 1x quick

---

## TODOs

---

- [x] 1. Create `static/css/kimun.css` — Component Styles + Animation Patterns

  **What to do**:
  - Create `static/css/kimun.css` with the following sections:
  
  **Section 1: CSS Custom Properties (additions only, NOT duplicating base.html)**
  ```css
  /* Spacing scale */
  :root {
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 1.5rem;
    --space-xl: 2rem;
    --space-2xl: 3rem;
    --space-3xl: 4rem;
    
    /* Radius variants */
    --radius-sm: 0.25rem;
    --radius-md: 0.75rem;
    --radius-lg: 1rem;
    --radius-xl: 1.5rem;
    --radius-asymmetric: 1rem 0.25rem 1rem 0.25rem;
    
    /* Shadow depth */
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 40px -10px rgba(0,0,0,0.15);
    
    /* Transition */
    --transition-fast: 0.15s ease;
    --transition-normal: 0.2s ease;
    --transition-slow: 0.3s ease;
  }
  ```
  
  **Section 2: Component Refined Styles**
  ```css
  /* Card variants */
  .hybrid-card-featured {
    border-radius: var(--radius-asymmetric);
    border-left: 4px solid var(--color-primary);
  }
  .hybrid-card-stat {
    border-radius: var(--radius-md);
    text-align: center;
    padding: var(--space-lg) var(--space-xl);
  }
  
  /* Button variants */
  .btn-subtle {
    background: transparent;
    color: var(--color-text-secondary);
    border: 1px solid var(--color-border);
    transition: var(--transition-normal);
  }
  .btn-subtle:hover {
    background: var(--color-card-hover);
    color: var(--color-text);
  }
  
  /* Badge variants */
  .badge { padding: 0.125rem 0.5rem; border-radius: var(--radius-sm); font-size: 0.75rem; font-weight: 600; }
  .badge-success { background: var(--color-success-bg); color: var(--color-success); }
  .badge-warning { background: var(--color-warning-bg); color: var(--color-warning); }
  .badge-info { background: var(--color-info-bg); color: var(--color-info); }
  .badge-purple { background: var(--color-purple-bg); color: var(--color-purple); }
  .badge-pink { background: var(--color-pink-bg); color: var(--color-pink); }
  
  /* Section headers */
  .section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-text);
    margin-bottom: var(--space-lg);
    display: flex;
    align-items: center;
    gap: var(--space-sm);
  }
  .section-title i {
    color: var(--color-primary);
  }
  ```
  
  **Section 3: Animation Patterns**
  ```css
  /* Staggered entrance */
  .stagger-in > * { opacity: 0; animation: fadeInUp 0.5s ease forwards; }
  .stagger-in > *:nth-child(1) { animation-delay: 0.05s; }
  .stagger-in > *:nth-child(2) { animation-delay: 0.1s; }
  .stagger-in > *:nth-child(3) { animation-delay: 0.15s; }
  .stagger-in > *:nth-child(4) { animation-delay: 0.2s; }
  .stagger-in > *:nth-child(5) { animation-delay: 0.25s; }
  .stagger-in > *:nth-child(6) { animation-delay: 0.3s; }
  
  @keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
  }
  .animate-float { animation: float 6s ease-in-out infinite; }
  
  @keyframes pulse-subtle {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.85; }
  }
  .animate-pulse-subtle { animation: pulse-subtle 3s ease-in-out infinite; }
  
  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .stagger-in > *, .animate-float, .animate-pulse-subtle, .fade-in {
      animation: none !important;
      opacity: 1 !important;
    }
    .hybrid-card, .btn-primary, .btn-outline, .btn-subtle {
      transition: none !important;
    }
  }
  ```
  
  **Section 4: Layout Utilities**
  ```css
  /* Asymmetric grid */
  .layout-split { display: grid; grid-template-columns: 1fr; gap: var(--space-lg); }
  @media (min-width: 768px) { .layout-split { grid-template-columns: 7fr 5fr; } }
  
  /* Hero section */
  .hero-section {
    position: relative;
    overflow: hidden;
    padding: var(--space-3xl) 0;
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
    border-radius: var(--radius-xl);
    color: white;
  }
  .hero-section::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 60%;
    height: 200%;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
    transform: rotate(-15deg);
  }
  
  /* Empty state */
  .empty-state {
    text-align: center;
    padding: var(--space-3xl) var(--space-xl);
  }
  .empty-state svg {
    margin: 0 auto var(--space-lg);
    opacity: 0.7;
  }
  ```
  
  - Add `<link rel="stylesheet" href="{% static 'css/kimun.css' %}">` to `base.html` after the `<style>` block
  - Verify `python manage.py collectstatic --noinput` works (or just verify the static file serves in dev)

  **Must NOT do**:
  - Do NOT duplicate CSS variables already in `base.html`
  - Do NOT modify existing `hybrid-card`, `btn-primary`, `btn-outline`, `input-field` base styles
  - Do NOT add hardcoded color values
  - Do NOT create a build pipeline

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES - with Tasks 2 and 3
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Tasks 4-15
  - **Blocked By**: None

  **References**:
  **Pattern References**:
  - `templates/base.html:33-193` — Current CSS variables and component styles (the pattern to extend, not replace)
  - `templates/base.html:167-192` — Existing animation system (fadeIn, stagger-1 through stagger-4)

  **WHY Each Reference Matters**:
  - `base.html` CSS section: Defines all existing variables and components. New styles must extend, not duplicate.

  **Acceptance Criteria**:
  - [ ] `static/css/kimun.css` exists and is < 30KB
  - [ ] File contains: spacing scale, radius variants, shadow depth, transition speeds
  - [ ] File contains: card variants, button variants, badge styles, section headers
  - [ ] File contains: animation patterns (stagger-in, float, pulse-subtle)
  - [ ] File contains: layout utilities (layout-split, hero-section, empty-state)
  - [ ] File contains: `@media (prefers-reduced-motion: reduce)` block that disables ALL animations
  - [ ] `base.html` includes the CSS file link
  - [ ] No hardcoded color values (all use `var(--color-*)`)

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: CSS file loads and applies styles
    Tool: Bash
    Steps:
      1. Run `python manage.py collectstatic --noinput`
      2. Verify `static/css/kimun.css` exists with `ls -la static/css/kimun.css`
      3. Grep for `@media (prefers-reduced-motion` to verify accessibility
      4. Grep for `var(--color-` to verify no hardcoded colors in new styles
      5. Run `python manage.py test` to verify no regressions
    Expected Result: File exists, accessibility media query present, no hardcoded colors, 286 tests pass
    Failure Indicators: File missing, grep fails, tests fail
    Evidence: .sisyphus/evidence/task-1-css-loads.txt
  
  Scenario: Dark mode variables work with new styles
    Tool: Bash
    Steps:
      1. Grep `static/css/kimun.css` for `var(--color-` usage
      2. Verify ALL color references use CSS variables, not hex values
    Expected Result: Zero hardcoded color values outside of existing base.html
    Failure Indicators: Any hex color (#xxx) or rgb() values in kimun.css
    Evidence: .sisyphus/evidence/task-1-dark-mode-vars.txt
  ```

  **Commit**: YES (groups with Task 2)
  - Message: `feat(ui): add kimun.css component stylesheet`
  - Files: `static/css/kimun.css`, `templates/base.html`

---

- [x] 2. Add Alpine.js Globally to base.html

  **What to do**:
  - In `templates/base.html`, add Alpine.js CDN to the `{% block extra_head %}` block (or just before `</head>` if block is empty):
    ```html
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    ```
  - Remove the Alpine.js script tags from `templates/evaluaciones/tomar_evaluacion.html` and `templates/evaluaciones/evaluacion_form.html` (since they're now loaded globally)
  - Verify Alpine.js components still work on the evaluation page

  **Must NOT do**:
  - Do NOT remove any Alpine.js `x-data` or `x-init` attributes from templates
  - Do NOT change any Alpine.js component logic

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES - with Tasks 1 and 3
  - **Parallel Group**: Wave 1
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  **Pattern References**:
  - `templates/evaluaciones/tomar_evaluacion.html:8` — Alpine.js CDN tag (currently page-specific)
  - `templates/evaluaciones/evaluacion_form.html` — May also have Alpine.js tag

  **Acceptance Criteria**:
  - [ ] `base.html` contains Alpine.js CDN script tag
  - [ ] `tomar_evaluacion.html` no longer has page-specific Alpine.js tag
  - [ ] `evaluacion_form.html` no longer has page-specific Alpine.js tag (if it had one)
  - [ ] `python manage.py test` passes

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Alpine.js loads globally
    Tool: Bash
    Steps:
      1. Grep `templates/base.html` for `alpinejs`
      2. Verify exactly ONE Alpine.js script tag in base.html
      3. Grep `templates/evaluaciones/tomar_evaluacion.html` for `alpinejs`
      4. Verify NO Alpine.js script tag in tomar_evaluacion.html
      5. Run `python manage.py test`
    Expected Result: One global Alpine.js tag, zero page-specific tags, tests pass
    Evidence: .sisyphus/evidence/task-2-alpine-global.txt
  ```

  **Commit**: YES (groups with Task 1)
  - Message: `feat(ui): add alpine.js to global layout`
  - Files: `templates/base.html`, `templates/evaluaciones/tomar_evaluacion.html`

---

- [x] 3. Create SVG Illustration Library for Empty States and Hero

  **What to do**:
  - Create directory `static/img/illustrations/`
  - Create 8-10 inline SVG illustrations (first-aid/medical/Latin-American themed):
  
  1. `empty-courses.svg` — No courses available (person looking at empty shelf/bookshelf)
  2. `empty-tasks.svg` — No assignments (person with clipboard, nothing to check off)
  3. `empty-evaluations.svg` — No exams (person at desk, no papers)
  4. `empty-calendar.svg` — No events (calendar with no marks)
  5. `empty-announcements.svg` — No announcements (person reading empty bulletin board)
  6. `empty-certificates.svg` — No certificates (empty frame/award stand)
  7. `empty-students.svg` — No students (empty classroom chairs)
  8. `empty-search.svg` — No search results (magnifying glass with question mark)
  9. `hero-learning.svg` — Hero section illustration (people learning together, books, medical cross)
  10. `hero-dashboard.svg` — Dashboard welcome (person at computer, charts, checklist)
  
  - Each SVG should be:
    - Simple line art style (not photorealistic)
    - Uses `currentColor` for stroke/fill so it adapts to light/dark theme
    - Max 3-4 colors per illustration (primary, accent, secondary, background)
    - Clean, warm, approachable (for elderly care worker audience)
    - 200-300px wide (scalable via viewBox)
    - Medical/first-aid themed with Latin American cultural touches where appropriate
  
  - Create `templates/partials/empty_state.html` as a reusable partial:
    ```html
    {% load static %}
    {% with illustration=illustration|default:"empty-search" title=title|default:"Sin resultados" description=description|default:"No se encontraron resultados." %}
    <div class="empty-state stagger-in">
      {% include "partials/illustrations/"|add:illustration|add:".svg" %}
      <h3 class="text-xl font-semibold mt-4" style="color: var(--color-text);">{{ title }}</h3>
      <p class="mt-2" style="color: var(--color-text-secondary);">{{ description }}</p>
      {% if action_url %}
      <a href="{{ action_url }}" class="btn-primary px-6 py-2 rounded-xl mt-6 inline-block">{{ action_text|default:"Comenzar" }}</a>
      {% endif %}
    </div>
    {% endwith %}
    ```
    
    NOTE: Since Django doesn't have an `add` filter that works this way with includes, use a simpler approach:
    ```html
    <div class="empty-state stagger-in">
      <img src="{% static illustration_path %}" alt="{{ title|default:'Sin resultados' }}" class="w-48 h-48 mx-auto">
      <h3 class="text-xl font-semibold mt-4" style="color: var(--color-text);">{{ title|default:"Sin resultados" }}</h3>
      <p class="mt-2" style="color: var(--color-text-secondary);">{{ description|default:"No se encontraron resultados." }}</p>
      {% if action_url %}
      <a href="{{ action_url }}" class="btn-primary px-6 py-2 rounded-xl mt-6 inline-block">{{ action_text|default:"Comenzar" }}</a>
      {% endif %}
    </div>
    ```

  **Must NOT do**:
  - Do NOT use external SVG libraries (must be custom)
  - Do NOT use raster images (PNG/JPG) - SVGs only
  - Do NOT add JavaScript dependencies
  - Do NOT create photorealistic illustrations

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`

  **Parallelization**:
  - **Can Run In Parallel**: YES - with Tasks 1 and 2
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 4, 13
  - **Blocked By**: None

  **References**:
  **Pattern References**:
  - `static/css/toast.css` — Example of existing custom CSS file (pattern for adding new static assets)
  - `templates/base.html:33-193` — CSS variables as color palette reference for SVGs

  **Acceptance Criteria**:
  - [ ] `static/img/illustrations/` directory exists with 8-10 SVG files
  - [ ] Each SVG uses `currentColor` for theme adaptation
  - [ ] `templates/partials/empty_state.html` reusable partial exists
  - [ ] SVG files are < 5KB each
  - [ ] `python manage.py collectstatic --noinput` succeeds

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: SVG illustrations exist and are valid
    Tool: Bash
    Steps:
      1. List files in `static/img/illustrations/`
      2. Count SVG files (expect 8-10)
      3. For each SVG: check file size < 5KB
      4. For each SVG: grep for `currentColor` to verify theme compatibility
      5. Verify `templates/partials/empty_state.html` exists
    Expected Result: 8-10 SVGs, all < 5KB, all use currentColor, partial exists
    Failure Indicators: Missing SVGs, oversized files, missing currentColor, missing partial
    Evidence: .sisyphus/evidence/task-3-svg-library.txt
  ```

  **Commit**: YES
  - Message: `feat(ui): add SVG illustration library for empty states`
  - Files: `static/img/illustrations/*.svg`, `templates/partials/empty_state.html`

---

- [ ] 4. Redesign Homepage (inicio.html) — Hero Section with SVG

  **What to do**:
  - Redesign `templates/inicio.html` to include:
  
  1. **Hero section** at top: gradient background using `var(--gradient-start)` and `var(--gradient-end)`, with the `hero-learning.svg` illustration on the right side, welcome text on the left, and a "Ver Cursos" CTA button
  
  2. **Stats row** below hero: 4 stat cards in asymmetric layout (2 large + 2 small) showing total cursos, usuarios, inscripciones, evaluaciones
  
  3. **Featured courses section**: 3 course cards in staggered layout (not uniform grid), using `stagger-in` class
  
  4. **Quick actions section**: Role-based action buttons (docente: crear curso, admin: gestionar usuarios, colaborador: mis cursos)
  
  5. **Recent announcements**: 2-3 announcement previews with priority colors
  
  - Use `layout-split` class for asymmetric sections
  - Use `hero-section` class for the hero
  - Use `stagger-in` class for card groups
  - Use `section-title` class for section headers
  - Replace uniform `grid grid-cols-3 gap-6` with asymmetric `layout-split` or mixed-width grids
  - All text in Spanish
  - Preserve existing context variables (cursos, total_usuarios, etc.)

  **Must NOT do**:
  - Do NOT remove existing context variables from the view
  - Do NOT change the URL routes or view logic
  - Do NOT use Bootstrap CSS classes

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`

  **Parallelization**:
  - **Can Run In Parallel**: NO — depends on Tasks 1, 3
  - **Parallel Group**: Wave 2
  - **Blocks**: None
  - **Blocked By**: Tasks 1, 3

  **References**:
  **Pattern References**:
  - `templates/inicio.html` — Current homepage (the page being redesigned)
  - `templates/base.html:33-193` — CSS variables, component classes
  - `static/css/kimun.css` (Task 1) — New component styles (layout-split, hero-section, etc.)
  - `static/img/illustrations/hero-learning.svg` (Task 3) — Hero illustration

  **API/Type References**:
  - `reportes/views.py:dashboard view` — Context variables pattern (total_usuarios, total_cursos, etc.)

  **Acceptance Criteria**:
  - [ ] `templates/inicio.html` has hero section with SVG illustration
  - [ ] Hero uses `var(--gradient-start)` and `var(--gradient-end)` for background
  - [ ] Stats row uses asymmetric layout (not uniform grid)
  - [ ] Course cards use `stagger-in` animation class
  - [ ] Section headers use `section-title` class
  - [ ] Quick actions section is role-based (docente, admin, colaborador)
  - [ ] All text in Spanish
  - [ ] Mobile responsive (collapses to single column)

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Homepage renders with hero section
    Tool: Playwright
    Steps:
      1. Navigate to homepage (/)
      2. Verify hero section exists (has gradient background)
      3. Verify SVG illustration is present in hero
      4. Verify "Ver Cursos" CTA button exists
      5. Verify stat cards render (at least 2 visible)
      6. Verify mobile responsive (resize to 375px, verify single column)
    Expected Result: Hero section renders, SVG visible, stats visible, responsive
    Failure Indicators: Missing hero, missing SVG, broken layout, horizontal scroll on mobile
    Evidence: .sisyphus/evidence/task-4-homepage-hero.png

  Scenario: Dark mode homepage
    Tool: Playwright
    Steps:
      1. Toggle dark mode
      2. Navigate to homepage
      3. Verify hero section uses dark theme colors
      4. Verify SVG illustration adapts (uses currentColor or dark variant)
      5. Screenshot
    Expected Result: Dark mode renders correctly, no white-on-white or black-on-black text
    Evidence: .sisyphus/evidence/task-4-homepage-dark.png
  ```

  **Commit**: YES
  - Message: `feat(ui): redesign homepage with hero section and asymmetric layout`
  - Files: `templates/inicio.html`

---

- [ ] 5. Redesign Dashboard (reportes/dashboard.html) — Asymmetric Layout

  **What to do**:
  - Redesign `templates/reportes/dashboard.html` with:
  
  1. **Welcome header**: "Reportes de Cumplimiento" with role-based subtitle (admin sees "Vista completa", docente sees "Tus cursos")
  2. **Stats row**: 4 stat cards in asymmetric layout using `layout-split` (2 large + 2 small)
  3. **Charts section**: Chart.js canvas elements in a hero-style card with proper titles
  4. **At-risk students table**: Using `section-title` header, proper column headers matching context data (usuario, curso, razón, estado, última_actividad)
  5. **Quick links row**: Links to progreso_heatmap, enviar_anuncios, identificar_riesgo commands
  
  - Fix the data contract mismatch: ensure `estudiantes_en_riesgo` context dictionary keys match template variable names
  - Use `stagger-in` for card entrance animations
  - Use `section-title` for section headers
  - Replace `grid grid-cols-2 md:grid-cols-4 gap-4` with more varied layout

  **Must NOT do**:
  - Do NOT remove Chart.js integration
  - Do NOT remove at-risk students functionality
  - Do NOT change the view context variable names

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`

  **Parallelization**:
  - **Can Run In Parallel**: YES - with Task 6
  - **Parallel Group**: Wave 3
  - **Blocks**: None
  - **Blocked By**: Task 1

  **References**:
  **Pattern References**:
  - `templates/reportes/dashboard.html` — Current dashboard layout (being redesigned)
  - `static/css/kimun.css` (Task 1) — New component styles

  **API/Type References**:
  - `reportes/views.py:get_at_risk_students()` — Returns dict with keys `usuario`, `curso`, `razon`, `estado`, `ultima_actividad`

  **Acceptance Criteria**:
  - [ ] Dashboard uses `layout-split` for charts section
  - [ ] Stats use `hybrid-card-stat` or asymmetric layout
  - [ ] At-risk table column headers match context data keys
  - [ ] Charts render with Chart.js
  - [ ] Quick links section exists
  - [ ] `stagger-in` class used for entrance animations
  - [ ] Mobile responsive

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: Dashboard renders with asymmetric layout
    Tool: Playwright
    Steps:
      1. Login as admin, navigate to /reportes/
      2. Verify stats cards render
      3. Verify chart canvases exist
      4. Verify at-risk table exists with proper headers
      5. Resize to 375px, verify mobile responsive
    Expected Result: Dashboard renders, charts visible, table headers correct
    Evidence: .sisyphus/evidence/task-5-dashboard.png

  Scenario: Data contract alignment
    Tool: Bash
    Steps:
      1. Grep `templates/reportes/dashboard.html` for `estudiante.estado`, `estudiante.ultima_actividad`, `estudiante.riesgo`
      2. Grep `reportes/views.py` for the keys returned by `get_at_risk_students`
      3. Verify template keys match view keys
    Expected Result: Template uses keys that match what the view provides
    Evidence: .sisyphus/evidence/task-5-data-contract.txt
  ```

  **Commit**: YES (groups with Task 6)
  - Message: `feat(ui): redesign dashboard with asymmetric layout and fix data contract`
  - Files: `templates/reportes/dashboard.html`

---

- [ ] 6. Refine Chart.js Integration and At-Risk Table

  **What to do**:
  - In `templates/reportes/dashboard.html`, ensure Chart.js charts use real data from context:
    - Completion donut chart should use `inscripciones_por_estado` or similar context data
    - Pass/Fail bar chart should use actual evaluation results data
  - Add proper chart titles in Spanish
  - Style chart containers with `hybrid-card` and `section-title`
  - Ensure at-risk table renders with correct column order

  **Must NOT do**:
  - Do NOT add new view logic (only template changes)
  - Do NOT change Chart.js CDN source

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `["frontend-ui-ux"]`

  **Parallelization**:
  - **Can Run In Parallel**: YES - with Task 5
  - **Parallel Group**: Wave 3
  - **Blocks**: None
  - **Blocked By**: Task 1

  **References**:
  - `templates/reportes/dashboard.html` — Current chart integration
  - `reportes/views.py:dashboard` — Context data

  **Acceptance Criteria**:
  - [ ] Charts use context data (not hardcoded 0 values)
  - [ ] Chart titles in Spanish
  - [ ] Chart containers use hybrid-card styling

  **QA Scenarios**:
  ```
  Scenario: Charts use real data
    Tool: Bash
    Steps:
      1. Grep dashboard.html for `data-passed`, `data-failed`, `data-completed`
      2. Verify they reference context variables, not hardcoded "0"
    Expected Result: Chart data attributes reference Django template variables
    Evidence: .sisyphus/evidence/task-6-charts-data.txt
  ```

  **Commit**: YES (groups with Task 5)

---

- [ ] 7. Redesign curso_list.html — Asymmetric Course Cards

  **What to do**:
  - Replace uniform `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6` with:
    - Featured/first course card: larger, with image/gradient background
    - Remaining cards: smaller, in 2-3 column grid
    - Stagger entrance animation
  - Add `section-title` header with icon
  - Category filter pills at top
  - Empty state with SVG illustration

  **Must NOT do**: Do NOT change view logic

  **Recommended Agent Profile**: `visual-engineering`

  **Parallelization**: Wave 4 (parallel with 8-12)

---

- [ ] 8. Redesign curso_detail.html — Split Layout with Progress

  **What to do**:
  - Replace uniform card layout with `layout-split` (2/3 + 1/3)
  - Left: course info, description, materials, clases
  - Right: sticky sidebar with progress, quick actions, instructor info
  - Add progress bar for enrolled users
  - Section headers with `section-title`

  **Must NOT do**: Do NOT change view context variables

  **Recommended Agent Profile**: `visual-engineering`

  **Parallelization**: Wave 4 (parallel with 7, 9-12)

---

- [ ] 9. Redesign evaluacion_list.html + tomar_evaluacion.html — Exam Experience

  **What to do**:
  - `evaluacion_list.html`: Cards with attempt badge, progress indicator, due date highlight
  - `tomar_evaluacion.html`: Cleaner question cards, progress bar refinements, timer refinement
  - Use `section-title` for headers, `stagger-in` for card entrance

  **Must NOT do**: Do NOT change evaluation-taking logic

  **Recommended Agent Profile**: `visual-engineering`

  **Parallelization**: Wave 4

---

- [ ] 10. Redesign tarea_list.html + tarea_detail.html — Assignment Cards

  **What to do**:
  - `tarea_list.html`: Cards with status badges (enviado, calificado, pendiente), due date highlighting
  - `tarea_detail.html`: Split layout with assignment info + submission status
  - Empty state SVG illustration

  **Must NOT do**: Do NOT change view logic

  **Recommended Agent Profile**: `visual-engineering`

  **Parallelization**: Wave 4

---

- [ ] 11. Redesign login.html — Auth Page with Illustration

  **What to do**:
  - Add SVG illustration (hero-learning.svg or a login-specific SVG)
  - Use split layout: illustration on left, form on right
  - Rounded input fields with clear labels
  - Error message styling refinements
  - Add "Kimün" branding text next to logo

  **Must NOT do**: Do NOT change auth backend logic

  **Recommended Agent Profile**: `visual-engineering`

  **Parallelization**: Wave 4

---

- [ ] 12. Redesign calendario.html — Calendar Visual Refresh

  **What to do**:
  - Calendar grid with better day styling
  - Event pills with category colors and proper spacing
  - Month navigation with subtle animation
  - Better mobile responsiveness

  **Must NOT do**: Do NOT change calendar view logic or URL routing

  **Recommended Agent Profile**: `visual-engineering`

  **Parallelization**: Wave 4

---

- [ ] 13. Add SVG Empty States to List Pages

  **What to do**:
  - Replace text-only empty states with SVG illustrations in these templates:
    1. `templates/cursos/curso_list.html` → `empty-courses.svg`
    2. `templates/tareas/tarea_list.html` → `empty-tasks.svg`
    3. `templates/evaluaciones/evaluacion_list.html` → `empty-evaluations.svg`
    4. `templates/calendario/calendario.html` → `empty-calendar.svg`
    5. `templates/anuncios/anuncio_list.html` → `empty-announcements.svg`
    6. `templates/certificados/mis_certificados.html` → `empty-certificates.svg`
    7. `templates/usuarios/mis_cursos.html` → `empty-courses.svg`
    8. `templates/reportes/dashboard.html` → (already has content, skip)
  - Use the `templates/partials/empty_state.html` partial for each

  **Must NOT do**: Do NOT add new context variables to views

  **Recommended Agent Profile**: `visual-engineering`

  **Parallelization**: Wave 5

---

- [ ] 14. Refine Form Pages — Consistent Spacing + Visual Hierarchy

  **What to do**:
  - Audit ALL form templates for consistent spacing:
    - `templates/cursos/curso_form.html`
    - `templates/cursos/material_form.html`
    - `templates/cursos/clase_form.html`
    - `templates/cursos/categoria_form.html`
    - `templates/evaluaciones/evaluacion_form.html`
    - `templates/tareas/tarea_form.html`
    - `templates/tareas/entrega_form.html`
    - `templates/anuncios/anuncio_form.html`
    - `templates/calendario/evento_form.html`
  - Add visual hierarchy: section dividers, grouped fields, clear labels
  - Use `section-title` for form sections
  - Ensure all form inputs use `input-field` class consistently

  **Must NOT do**: Do NOT change form validation logic or fields

  **Recommended Agent Profile**: `visual-engineering`

  **Parallelization**: Wave 5

---

- [ ] 15. Final Pass — Mobile Responsiveness + Dark Mode Parity

  **What to do**:
  - Test ALL redesigned templates at 320px, 375px, 768px, 1024px widths
  - Verify all asymmetric layouts collapse to single column on mobile
  - Test dark mode on ALL redesigned pages
  - Verify SVG illustrations adapt with `currentColor`
  - Verify `prefers-reduced-motion` disables animations
  - Fix any visual issues found

  **Must NOT do**: Do NOT add new features

  **Recommended Agent Profile**: `visual-engineering`

  **Parallelization**: Wave 5

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

- [ ] F1. **Visual Regression via Playwright** — `unspecified-high`
  Navigate to all redesigned pages (homepage, dashboard, course list, course detail, evaluation list, task list, login, calendar). Take screenshots. Verify no broken layouts, missing assets, or console errors. Test dark mode toggle on each page. Test mobile viewport (375px).

- [ ] F2. **Dark Mode Parity Check** — `unspecified-high`
  For each redesigned page: toggle dark mode, verify all CSS custom properties resolve correctly, no hardcoded colors visible, SVGs adapt. Screenshot each page.

- [ ] F3. **Accessibility + Performance Audit** — `unspecified-high`
  Run Lighthouse accessibility audit on 3 key pages. Verify `prefers-reduced-motion` disables all animations. Verify CSS file size < 30KB. Verify no layout shifts.

- [ ] F4. **Non-Regression Test Suite** — `quick`
  Run `python manage.py test` and verify 286+ tests still pass.

---

## Commit Strategy

- **Wave 1**: `feat(ui): add kimun.css component stylesheet, alpine.js globally, and SVG illustration library`
- **Wave 2**: `feat(ui): redesign homepage with hero section`
- **Wave 3**: `feat(ui): redesign dashboard with asymmetric layout`
- **Wave 4**: `feat(ui): redesign course, evaluation, task, login, and calendar pages`
- **Wave 5**: `feat(ui): add empty state illustrations and refine form pages`
- **Wave FINAL**: `feat(ui): final polish — mobile, dark mode, and accessibility`

---

## Success Criteria

### Verification Commands
```bash
python manage.py test                    # Expected: 286+ tests pass
ls -la static/css/kimun.css             # Expected: file exists, < 30KB
ls static/img/illustrations/*.svg | wc -l  # Expected: 8-10 files
grep -c 'alpinejs' templates/base.html  # Expected: 1
grep -c 'prefers-reduced-motion' static/css/kimun.css  # Expected: > 0
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] 286+ tests pass
- [ ] Homepage has hero section with SVG
- [ ] Dashboard has asymmetric layout
- [ ] All redesigned pages work in dark mode
- [ ] All redesigned pages are mobile responsive
- [ ] `prefers-reduced-motion` disables animations
- [ ] No hardcoded color values in kimun.css