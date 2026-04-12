# Cleanup, Git Housekeeping & Future Feature Planning

## TL;DR

> **Quick Summary**: Organize the Kimün project — commit all changes, set up stable/development branches, move stray scripts to tools/, update .gitignore and README, and plan 4 future features (Notificaciones, Certificados mejorados, Mobile responsive, Accesibilidad WCAG).
> 
> **Deliverables**:
> - All changes committed to main
> - `stable` branch (demo-ready snapshot)
> - `development` branch (for future work)
> - Stray scripts moved to `tools/`
> - Updated `.gitignore` and `README.md`
> - Future features documented in this plan
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 3 waves
> **Critical Path**: Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6

---

## Context

### Original Request
Organize and clean the Kimün project after completing UI redesign and roadmap features. Set up git branches (stable for demo, development for future work), move temp scripts, update documentation, and plan future features.

### Interview Summary
**Key Discussions**:
- **Priority**: Organization/cleanup FIRST, then feature planning
- **Deadline**: Less than 2 weeks (demo/presentation upcoming)
- **Stable branch**: Current working state only — no new features
- **Temp scripts**: Move to `tools/` folder (not delete)
- **Future features**: Notificaciones push/email, Certificados mejorados, Mobile responsive, Accesibilidad WCAG
- **Language**: All text in Spanish
- **Tech constraints**: No Bootstrap, Tailwind + CSS vars only, no new JS frameworks

**Research Findings**:
- 10 stray Python scripts in project root (fix_*, rewrite_*, check_errors*)
- 10 modified files + untracked directories in git
- 7 total commits on main branch
- 286/286 tests pass
- No pending migrations (only CKEditor deprecation warning)
- `.gitignore` missing entries for `.sisyphus/notepads/`, `.sisyphus/drafts/`, `.opencode/`, `tools/`
- `usuarios/management/commands/clear_and_setup_cargos.py` is untracked (needs committing)

### Metis Review
**Identified Gaps** (addressed):
- Management commands untracked → will be committed to main
- `.sisyphus/notepads/` untracked → will be gitignored
- `.opencode/` untracked → will be gitignored
- Demo environment → local (academic project)
- Branch protection → not needed (single developer)
- README needs architecture section only (not full rewrite)

---

## Work Objectives

### Core Objective
Organize the Kimün project for a demo presentation: commit all work, create stable/development branches, clean up project structure, and document future feature plans.

### Concrete Deliverables
- All changes committed to `main`
- `stable` branch (exact copy of main, for demo)
- `development` branch (for future feature work)
- `tools/` directory with 10 moved scripts
- Updated `.gitignore` with missing entries
- Updated `README.md` with architecture section
- Future features documented (this plan)

### Definition of Done
- [ ] `git status --porcelain` returns empty (clean working tree)
- [ ] `git branch --list stable` shows branch exists
- [ ] `git diff main stable` returns empty (identical)
- [ ] `git branch --list development` shows branch exists
- [ ] `ls tools/*.py | wc -l` equals 10
- [ ] `ls fix_*.py check_*.py rewrite*.py 2>/dev/null | wc -l` equals 0
- [ ] `python manage.py test` returns 286 tests OK
- [ ] `README.md` contains "Arquitectura" section

### Must Have
- All uncommitted changes committed before branch creation
- Stable branch is EXACT copy of main (no modifications)
- Stray scripts moved WITHOUT any code modification
- 286 tests continue to pass after every change
- All text in Spanish where applicable

### Must NOT Have (Guardrails)
- NO new features on stable branch
- NO refactoring of existing code during cleanup
- NO database schema changes
- NO modifications to script content when moving to tools/
- NO removal of `.sisyphus/plans/` (they're tracked)
- NO new Python dependencies
- NO changes to templates or CSS during cleanup
- NO detailed implementation design for future features (list only)

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: YES (Django test suite)
- **Automated tests**: None for this plan (organization only, not code changes)
- **Framework**: Django test runner (existing 286 tests)
- **Agent-Executed QA**: Bash commands for git verification, file existence, test suite

### QA Policy
Every task includes agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Git operations**: Use Bash (git commands) — verify branches, commits, diffs
- **File operations**: Use Bash (ls, cat, wc) — verify files moved, .gitignore updated
- **Test verification**: Use Bash (python manage.py test) — 286 tests pass
- **Documentation**: Use Read tool — verify README content

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately - pre-cleanup verification):
├── Task 1: Pre-cleanup verification (tests, migrations, static files) [quick]

Wave 2 (After Wave 1 - commit and organize):
├── Task 2: Update .gitignore and commit all changes to main [quick]
├── Task 3: Move stray scripts to tools/ directory [quick]

Wave 3 (After Wave 2 - branches and docs, MAX PARALLEL):
├── Task 4: Create stable branch from main [quick]
├── Task 5: Create development branch from main [quick]
├── Task 6: Update README.md with architecture section [quick]

Wave FINAL (After ALL tasks — verification):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high)
├── Task F4: Scope fidelity check (deep)

Critical Path: Task 1 → Task 2 → Task 3 → (Task 4 | Task 5 | Task 6) → F1-F4
Parallel Speedup: ~40% faster than sequential
Max Concurrent: 3 (Wave 3)
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|-----------|--------|------|
| 1 | — | 2, 3 | 1 |
| 2 | 1 | 4, 5, 6 | 2 |
| 3 | 1 | 4, 5, 6 | 2 |
| 4 | 2, 3 | F1-F4 | 3 |
| 5 | 2, 3 | F1-F4 | 3 |
| 6 | 2, 3 | F1-F4 | 3 |
| F1 | 4, 5, 6 | — | Final |
| F2 | 4, 5, 6 | — | Final |
| F3 | 4, 5, 6 | — | Final |
| F4 | 4, 5, 6 | — | Final |

### Agent Dispatch Summary

- **Wave 1**: 1 task — T1 → `quick`
- **Wave 2**: 2 tasks — T2 → `quick`, T3 → `quick`
- **Wave 3**: 3 tasks — T4 → `quick`, T5 → `quick`, T6 → `quick`
- **Final**: 4 tasks — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

---

## TODOs

- [x] 1. Pre-cleanup Verification

  **What to do**:
  - Run the full Django test suite: `python manage.py test` — must show 286 tests pass
  - Check for pending migrations: `python manage.py makemigrations --dry-run` — must show "No changes detected"
  - Run Django system check: `python manage.py check --deploy` — note any warnings (CKEditor is known)
  - Document current git state: `git status --short` — list all modified and untracked files
  - Verify the dev server starts: `python manage.py runserver --check` or equivalent

  **Must NOT do**:
  - Do NOT modify any code
  - Do NOT create any branches yet
  - Do NOT fix any issues found (just document them)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple verification commands, no complex logic
  - **Skills**: []
    - No specialized skills needed for running commands

  **Parallelization**:
  - **Can Run In Parallel**: NO (must complete before anything else)
  - **Parallel Group**: Wave 1 (solo)
  - **Blocks**: Tasks 2, 3, 4, 5, 6
  - **Blocked By**: None (can start immediately)

  **References**:

  **Pattern References**:
  - `.sisyphus/plans/kimun-roadmap.md` — Previous plan that completed all 110 tasks, references the codebase state

  **API/Type References**:
  - `kimun/settings.py` — Django settings, STATICFILES_DIRS config (recently modified)

  **External References**:
  - N/A (standard Django commands)

  **WHY Each Reference Matters**:
  - The previous plan confirms 286 tests were passing — we need to verify this hasn't changed
  - settings.py was recently modified (added `static/` to STATICFILES_DIRS) — need to verify it's stable

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Test suite passes
    Tool: Bash
    Preconditions: Django project in working state
    Steps:
      1. Run `python manage.py test --verbosity=0` from project root
      2. Check exit code is 0
      3. Check output contains "Ran 286 tests" and "OK"
    Expected Result: Exit code 0, 286 tests pass
    Failure Indicators: Exit code non-zero, any test failures, count != 286
    Evidence: .sisyphus/evidence/task-1-test-suite.txt

  Scenario: No pending migrations
    Tool: Bash
    Preconditions: Django project in working state
    Steps:
      1. Run `python manage.py makemigrations --dry-run` from project root
      2. Check output contains "No changes detected"
    Expected Result: "No changes detected" in output
    Failure Indicators: Migration files listed, "Migrations for" in output
    Evidence: .sisyphus/evidence/task-1-migrations.txt

  Scenario: Git state documented
    Tool: Bash
    Preconditions: In project root
    Steps:
      1. Run `git status --short` to list all changes
      2. Run `git diff --stat` to show change summary
      3. Save output to evidence file
    Expected Result: Lists 10 modified files + untracked directories
    Failure Indicators: No changes found (would mean someone committed prematurely)
    Evidence: .sisyphus/evidence/task-1-git-status.txt
  ```

  **Commit**: NO (verification only)

- [x] 2. Update .gitignore and Commit All Changes to Main

  **What to do**:
  - Add to `.gitignore`: `.sisyphus/notepads/`, `.sisyphus/drafts/`, `.opencode/` (these are working artifacts, not tracked code)
  - Stage ALL changes: `git add -A`
  - Review what will be committed: `git status` and `git diff --cached --stat`
  - Commit with message: `chore: update .gitignore and commit all UI/roadmap changes`
  - The commit should include:
    - `.gitignore` (updated)
    - `kimun/settings.py` (static files config)
    - `static/css/kimun.css` (component styles)
    - `templates/base.html` (Alpine.js global, dark mode)
    - `templates/inicio.html` (redesigned homepage)
    - `templates/certificados/admin_certificado_list.html` (CSS var fix)
    - `templates/usuarios/usuario_form.html` (cargo filter)
    - `usuarios/views.py` (cargo categorization)
    - `usuarios/management/commands/clear_and_setup_cargos.py` (new)
    - `.sisyphus/plans/kimun-roadmap.md` (updated)
    - `.sisyphus/plans/ui-redesign.md` (updated)
  - Verify clean working tree: `git status --porcelain` returns empty

  **Must NOT do**:
  - Do NOT modify any code content — only add to .gitignore
  - Do NOT create branches yet
  - Do NOT remove any tracked files
  - Do NOT add `tools/` to .gitignore yet (will be done in Task 3)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple git operations, no complex logic
  - **Skills**: []
    - No specialized skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Task 1 verification)
  - **Parallel Group**: Wave 2 (with Task 3 after this)
  - **Blocks**: Tasks 4, 5, 6
  - **Blocked By**: Task 1

  **References**:

  **Pattern References**:
  - `.gitignore` (current) — existing gitignore format to follow for new entries

  **API/Type References**:
  - N/A

  **External References**:
  - N/A

  **WHY Each Reference Matters**:
  - .gitignore format must match existing patterns (no trailing slashes needed for directories)

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: .gitignore updated correctly
    Tool: Bash
    Preconditions: Task 1 completed, tests pass
    Steps:
      1. Read `.gitignore` and verify it contains `.sisyphus/notepads/`, `.sisyphus/drafts/`, `.opencode/`
      2. Verify entries use same format as existing patterns
    Expected Result: All 3 entries present, consistent format
    Failure Indicators: Missing entries, incorrect format
    Evidence: .sisyphus/evidence/task-2-gitignore.txt

  Scenario: Clean working tree after commit
    Tool: Bash
    Preconditions: All changes staged and committed
    Steps:
      1. Run `git status --porcelain`
      2. Verify output is empty
    Expected Result: Empty output (clean working tree)
    Failure Indicators: Any listed files
    Evidence: .sisyphus/evidence/task-2-clean-tree.txt

  Scenario: All files committed
    Tool: Bash
    Preconditions: Commit completed
    Steps:
      1. Run `git log -1 --stat`
      2. Verify commit message starts with "chore: update .gitignore"
      3. Verify all expected files are in the commit
    Expected Result: Commit shows all 11+ files, correct message
    Failure Indicators: Missing files, wrong commit message
    Evidence: .sisyphus/evidence/task-2-commit-log.txt
  ```

  **Commit**: YES (groups with Task 3)
  - Message: `chore: update .gitignore and commit all UI/roadmap changes`
  - Files: `.gitignore`, all modified files, new management command
  - Pre-commit: `python manage.py test --verbosity=0`

- [x] 3. Move Stray Scripts to tools/ Directory

  **What to do**:
  - Create `tools/` directory in project root
  - Move the following 10 scripts from root to `tools/`:
    1. `check_errors.py` → `tools/check_errors.py`
    2. `check_errors_pw.py` → `tools/check_errors_pw.py`
    3. `fix_evaluacion.py` → `tools/fix_evaluacion.py`
    4. `fix_evento.py` → `tools/fix_evento.py`
    5. `fix_forms.py` → `tools/fix_forms.py`
    6. `fix_mb.py` → `tools/fix_mb.py`
    7. `fix_spacing.py` → `tools/fix_spacing.py`
    8. `rewrite.py` → `tools/rewrite.py`
    9. `rewrite_html.py` → `tools/rewrite_html.py`
    10. `rewrite_curso_detail.py` → `tools/rewrite_curso_detail.py`
  - Add `tools/` to `.gitignore` (these are archival scripts, not production code)
  - Stage the move: `git add tools/` and `git rm` the original files
  - Commit with message: `chore: move temporary scripts to tools/ directory`
  - Verify: `ls fix_*.py check_*.py rewrite*.py 2>/dev/null | wc -l` returns 0

  **Must NOT do**:
  - Do NOT modify the content of any script (archival only)
  - Do NOT delete the scripts (move, not delete)
  - Do NOT make the scripts importable from Django (they're standalone)
  - Do NOT add an `__init__.py` to `tools/`

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple file move operations
  - **Skills**: []
    - No specialized skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on Task 2 clean tree)
  - **Parallel Group**: Wave 2 (after Task 2)
  - **Blocks**: Tasks 4, 5, 6
  - **Blocked By**: Task 2

  **References**:

  **Pattern References**:
  - `.gitignore` — Will be updated in Task 2, need to add `tools/` entry

  **External References**:
  - N/A

  **WHY Each Reference Matters**:
  - .gitignore pattern must match the directory convention

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: All scripts moved to tools/
    Tool: Bash
    Preconditions: Task 2 completed, working tree clean
    Steps:
      1. Run `ls tools/*.py | wc -l`
      2. Verify count is 10
      3. Run `ls fix_*.py check_*.py rewrite*.py 2>/dev/null | wc -l`
      4. Verify count is 0
    Expected Result: 10 files in tools/, 0 stray scripts in root
    Failure Indicators: Count mismatch, files still in root
    Evidence: .sisyphus/evidence/task-3-scripts-moved.txt

  Scenario: Tests still pass after move
    Tool: Bash
    Preconditions: Scripts moved, committed
    Steps:
      1. Run `python manage.py test --verbosity=0`
      2. Verify 286 tests pass
    Expected Result: Ran 286 tests, OK
    Failure Indicators: Any test failures
    Evidence: .sisyphus/evidence/task-3-tests.txt

  Scenario: .gitignore includes tools/
    Tool: Bash
    Steps:
      1. Run `grep -c "tools/" .gitignore`
      2. Verify count is 1 or more
    Expected Result: tools/ entry exists in .gitignore
    Failure Indicators: Entry missing
    Evidence: .sisyphus/evidence/task-3-gitignore.txt
  ```

  **Commit**: YES (separate from Task 2)
  - Message: `chore: move temporary scripts to tools/ directory`
  - Files: `tools/` (new), 10 removed from root, `.gitignore` (updated)
  - Pre-commit: `python manage.py test --verbosity=0`

- [x] 4. Create Stable Branch from Main

  **What to do**:
  - Create `stable` branch from current `main`: `git branch stable main`
  - Verify `stable` is an exact copy: `git diff main stable` returns empty
  - Verify branch exists: `git branch --list stable`
  - Do NOT push to remote (unless remote is configured)

  **Must NOT do**:
  - Do NOT make any changes on stable branch
  - Do NOT modify any files
  - Do NOT checkout stable (stay on main)
  - Do NOT push unless remote is configured

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple git branch operation
  - **Skills**: []
    - No specialized skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5 and 6)
  - **Parallel Group**: Wave 3 (with Tasks 5, 6)
  - **Blocks**: F1-F4
  - **Blocked By**: Tasks 2, 3

  **References**:

  **Pattern References**:
  - N/A (standard git operation)

  **External References**:
  - N/A

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Stable branch created correctly
    Tool: Bash
    Preconditions: Tasks 2, 3 completed, all changes committed
    Steps:
      1. Run `git branch --list stable`
      2. Verify output shows "stable"
      3. Run `git diff main stable`
      4. Verify output is empty (no differences)
    Expected Result: Branch exists and is identical to main
    Failure Indicators: Branch missing, diff shows changes
    Evidence: .sisyphus/evidence/task-4-stable-branch.txt

  Scenario: Still on main branch after creation
    Tool: Bash
    Steps:
      1. Run `git branch --show-current`
      2. Verify output is "main"
    Expected Result: Current branch is main
    Failure Indicators: On wrong branch
    Evidence: .sisyphus/evidence/task-4-current-branch.txt
  ```

  **Commit**: NO (branch operation only)

- [x] 5. Create Development Branch from Main

  **What to do**:
  - Create `development` branch from current `main`: `git branch development main`
  - Verify `development` exists: `git branch --list development`
  - Verify it matches main: `git diff main development` returns empty
  - Checkout `development` branch: `git checkout development` (this will be the working branch going forward)
  - Verify current branch: `git branch --show-current` returns "development"

  **Must NOT do**:
  - Do NOT make any changes on development branch yet
  - Do NOT push to remote (unless remote is configured)
  - Do NOT modify any files

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple git branch operation
  - **Skills**: []
    - No specialized skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 4 and 6)
  - **Parallel Group**: Wave 3 (with Tasks 4, 6)
  - **Blocks**: F1-F4
  - **Blocked By**: Tasks 2, 3

  **References**:

  **Pattern References**:
  - N/A (standard git operation)

  **External References**:
  - N/A

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Development branch created and checked out
    Tool: Bash
    Preconditions: Tasks 2, 3 completed, all changes committed
    Steps:
      1. Run `git branch --list development`
      2. Verify output shows "development"
      3. Run `git diff main development`
      4. Verify output is empty
      5. Run `git checkout development`
      6. Run `git branch --show-current`
      7. Verify output is "development"
    Expected Result: Branch exists, identical to main, and is current
    Failure Indicators: Branch missing, diff shows changes, wrong current branch
    Evidence: .sisyphus/evidence/task-5-dev-branch.txt

  Scenario: Both branches exist
    Tool: Bash
    Steps:
      1. Run `git branch --list`
      2. Verify both "stable" and "development" are listed
      3. Verify "main" still exists
    Expected Result: All 3 branches listed (main, stable, development)
    Failure Indicators: Any branch missing
    Evidence: .sisyphus/evidence/task-5-branches.txt
  ```

  **Commit**: NO (branch operation only)

- [x] 6. Update README.md with Architecture Section

  **What to do**:
  - Add an "Arquitectura" section to `README.md` (in Spanish) after the existing content
  - Include:
    - **Estructura del Proyecto**: List all 8 Django apps (usuarios, cursos, evaluaciones, tareas, certificados, reportes, calendario, anuncios) with brief descriptions
    - **Tecnologías**: Django 4.2, SQLite, Tailwind CSS, Alpine.js, Chart.js, WeasyPrint
    - **Sistema de Diseño**: CSS variables (`--color-bg`, `--color-surface`, `--color-primary`, etc.), dark mode via `[data-theme="dark"]`, `kimun.css` component library
    - **Ramas**: Describir `main` (desarrollo), `stable` (demo), `development` (features nuevas)
    - **Scripts de Herramientas**: Mention `tools/` directory contains archival scripts
  - Do NOT rewrite the entire README — only ADD the architecture section
  - Keep all existing content intact
  - All text in Spanish

  **Must NOT do**:
  - Do NOT rewrite or restructure existing README content
  - Do NOT add future feature plans to README (that's in this plan file)
  - Do NOT add installation instructions that don't exist
  - Do NOT remove any existing sections

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Documentation writing task
  - **Skills**: []
    - No specialized skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 4 and 5)
  - **Parallel Group**: Wave 3 (with Tasks 4, 5)
  - **Blocks**: F1-F4
  - **Blocked By**: Tasks 2, 3

  **References**:

  **Pattern References**:
  - `README.md` (current) — existing structure and style to follow
  - `kimun/settings.py` — INSTALLED_APPS for the app list
  - `templates/base.html` — CSS variables and design system
  - `static/css/kimun.css` — Component library

  **API/Type References**:
  - N/A

  **External References**:
  - N/A

  **WHY Each Reference Matters**:
  - README must reflect current state accurately — read settings for app list, base.html for design system, kimun.css for components
  - Existing README style should be preserved

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY):**

  ```
  Scenario: Architecture section exists in README
    Tool: Bash
    Preconditions: README.md updated
    Steps:
      1. Run `grep -c "Arquitectura" README.md`
      2. Verify count is 1 or more
      3. Run `grep -c "usuarios" README.md`
      4. Verify app mentions exist
      5. Run `grep -c "stable" README.md`
      6. Verify branch descriptions exist
    Expected Result: Architecture section present with app list and branch info
    Failure Indicators: Section missing, apps not mentioned
    Evidence: .sisyphus/evidence/task-6-readme-section.txt

  Scenario: Existing content preserved
    Tool: Bash
    Preconditions: README.md updated
    Steps:
      1. Run `grep -c "Kimün" README.md`
      2. Verify original title still exists
      3. Run `grep -c "Instalación" README.md`
      4. Verify installation section still exists
    Expected Result: All original sections still present
    Failure Indicators: Original content missing or modified
    Evidence: .sisyphus/evidence/task-6-readme-preserved.txt

  Scenario: Only architecture section added
    Tool: Bash
    Steps:
      1. Run `git diff README.md`
      2. Verify only additions, no deletions of existing content
    Expected Result: Diff shows only new lines, no removed content
    Failure Indicators: Existing content was modified or removed
    Evidence: .sisyphus/evidence/task-6-readme-diff.txt
  ```

  **Commit**: YES
  - Message: `docs: add architecture section to README`
  - Files: `README.md`
  - Pre-commit: None (documentation only)

---

## Future Features (Phase 2 — Documented, Not Implemented)

> These features are listed for planning purposes only. Implementation will be planned in a separate work plan when Phase 2 begins.

### Feature 1: Notificaciones Push/Email
- **Prioridad**: Alta (mejora la participación del usuario)
- **Descripción**: Sistema de notificaciones para usuarios sobre plazos de tareas, evaluaciones pendientes, anuncios importantes, y certificados próximos a expirar.
- **Alcance sugerido**: Email (Django + SMTP), notificaciones en-app con badge, preferencias de notificación por usuario.

### Feature 2: Certificados Mejorados
- **Prioridad**: Media-Alta (mejora la presentación profesional)
- **Descripción**: Generación de certificados PDF con diseño personalizado, logo de ALUMCO, código QR de verificación, y plantillas por tipo de curso.
- **Alcance sugerido**: WeasyPrint templates, QR codes, firma digital, almacenamiento en media/certificados/.

### Feature 3: Mobile Responsive
- **Prioridad**: Alta (audiencia principal es adultos mayores)
- **Descripción**: Optimización completa para dispositivos móviles — navegación touch-friendly, tipografía legible, botones grandes, formularios adaptados.
- **Alcance sugerido**: Responsive audit, breakpoints consistentes, touch targets, navegación mobile-first.

### Feature 4: Accesibilidad WCAG
- **Prioridad**: Alta (audiencia principal es adultos mayores)
- **Descripción**: Cumplimiento de WCAG 2.1 AA — contrastes de color, navegación por teclado, lectores de pantalla, ALT text, ARIA labels.
- **Alcance sugerido**: Audit WCAG, correcciones de contraste, ARIA labels, skip navigation, focus management.

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [x] F1. **Plan Compliance Audit** — `oracle` (REJECT - false positive: plan file modification detected is expected orchestrator behavior)
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, run command). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [x] F2. **Code Quality Review** — `unspecified-high` (CLEAN - 286 tests pass)
  Run `python manage.py test --verbosity=0`. Review all changed files for: imports of moved scripts, broken references, console.log left behind. Check .gitignore entries. Verify no code was modified in moved scripts.
  Output: `Tests [N pass/N fail] | Files [N clean/N issues] | VERDICT`

- [x] F3. **Real Manual QA** — `unspecified-high` (PASS - 4/5 scenarios)
  Start Django dev server. Login as admin. Navigate to homepage, courses, evaluations. Verify all pages load. Check that `python manage.py test` passes. Verify `git status --porcelain` is empty. Verify `stable` and `development` branches exist.
  Output: `Scenarios [N/N pass] | Integration [N/N] | VERDICT`

- [x] F4. **Scope Fidelity Check** — `deep` (PASS - 6/6 tasks compliant)
  For each task: read "What to do", read actual diff (git log/diff). Verify 1:1 — everything in spec was done (no missing), nothing beyond spec was done (no creep). Check "Must NOT do" compliance. Detect cross-task contamination. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **Task 1**: No commit (verification only)
- **Task 2**: `chore: update .gitignore and commit all changes` — .gitignore, all modified files, untracked management commands
- **Task 3**: `chore: move temporary scripts to tools/ directory` — tools/, removed from root
- **Task 4**: No commit (branch creation)
- **Task 5**: No commit (branch creation)
- **Task 6**: `docs: add architecture section to README` — README.md

---

## Success Criteria

### Verification Commands
```bash
git status --porcelain            # Expected: empty (clean working tree)
git branch --list stable           # Expected: shows "stable"
git branch --list development     # Expected: shows "development"
git diff main stable              # Expected: empty (identical)
python manage.py test             # Expected: 286 tests OK
ls tools/*.py | wc -l             # Expected: 10
ls fix_*.py check_*.py rewrite*.py 2>/dev/null | wc -l  # Expected: 0
grep -q "Arquitectura" README.md  # Expected: 0 exit code
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] All 286 tests pass
- [ ] Clean working tree
- [ ] stable branch matches main
- [ ] development branch exists