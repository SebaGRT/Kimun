# Testing Patterns

**Analysis Date:** 2026-04-24

## Test Framework

**Runner:** Django's built-in `TestCase` (unittest-based)
**Config:** No custom test runner configuration detected in `settings.py`
**Assertion Library:** Python unittest assertions

**Run Commands:**
```bash
python manage.py test                    # Run all tests
python manage.py test app_name           # Run tests for specific app
python manage.py test app_name.tests.TestClassName  # Run specific test class
```

## Test File Inventory

| App | File | Lines | Coverage Level |
|-----|------|-------|----------------|
| `anuncios` | `anuncios/tests.py` | 49 | Model tests only |
| `calendario` | `calendario/tests.py` | 457 | Models, forms, views, signals |
| `certificados` | `certificados/tests.py` | 599 | Models, views, services, signals |
| `cursos` | `cursos/tests.py` | 928 | Models, forms, views, utilities |
| `evaluaciones` | `evaluaciones/tests.py` | 853 | Models, forms, views, timer, randomization, scoring |
| `reportes` | `reportes/tests.py` | 172 | Views, RBAC |
| `tareas` | `tareas/tests.py` | 661 | Models, forms, views, signals |
| `usuarios` | `usuarios/tests.py` | 743 | Models, forms, views, decorators |

**Total test lines:** ~4,462 lines across 8 apps
**Total production Python lines:** ~12,130 lines (excluding migrations, tools, venv)
**Test-to-code ratio:** ~0.37 (37%)

**Visual regression test:** `test_visuals.py` (87 lines) - Playwright-based responsive layout and dark mode testing

## Test Organization

**Location:** Co-located as `tests.py` in each Django app
**Naming:** `class *Tests(TestCase)` for each test category
**Structure per app:**
```python
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

Usuario = get_user_model()

class ModelNameTests(TestCase):
    def setUp(self):
        # Create test users with explicit roles and RUT
        self.docente = Usuario.objects.create_user(
            username='docente', password='testpass', rol='docente', rut='11111111-1'
        )
        self.colaborador = Usuario.objects.create_user(
            username='colaborador', password='testpass', rol='colaborador', rut='22222222-2'
        )
```

## Test Patterns

### Model Tests
**Standard assertions observed:**
- Creation tests: verify field values after `objects.create()`
- `__str__` method tests
- Choice field validation
- Default value tests
- Unique constraint tests (using `with self.assertRaises(Exception):`)
- Related name traversal (e.g., `self.curso.materiales.count()`)
- `Meta` option tests (`verbose_name`, `ordering`)

**Example from `cursos/tests.py`:**
```python
def test_curso_estado_choices(self):
    choices = dict(Curso.ESTADO_CHOICES)
    self.assertIn('borrador', choices)
    self.assertIn('publicado', choices)
    self.assertEqual(choices['borrador'], 'Borrador')
```

### View Tests
**Pattern:** `Client`-based integration tests
- Login with `self.client.login(username='...', password='...')`
- Status code assertions (`302` for redirect, `200` for success, `403` for forbidden)
- Template used assertions: `self.assertTemplateUsed(response, 'template.html')`
- Context variable checks: `self.assertIn('key', response.context)`
- Message verification via `get_messages(response.wsgi_request)`
- Redirect target checks: `self.assertRedirects(response, reverse('...'))`

**Example from `reportes/tests.py`:**
```python
def test_dashboard_reportes_accessible_by_admin(self):
    self.client.login(username='admin', password='testpass')
    response = self.client.get(reverse('reportes:dashboard_reportes'))
    self.assertEqual(response.status_code, 200)
    self.assertIn('total_usuarios', response.context)
```

### Form Tests
**Pattern:** Instantiation with data dict, validity checks
- Valid data tests
- Required field omission tests
- Boundary value tests (min/max values)
- Cross-field validation tests (e.g., `__all__` errors)
- File upload tests using `SimpleUploadedFile`

**Example from `tareas/tests.py`:**
```python
def test_tarea_form_fecha_limite_past(self):
    data = self.valid_data.copy()
    data['fecha_limite'] = (timezone.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
    form = TareaForm(data=data)
    self.assertFalse(form.is_valid())
    self.assertIn('__all__', form.errors)
    self.assertIn('La fecha límite no puede estar en el pasado.', form.errors['__all__'])
```

### RBAC / Permission Tests
**Pattern:** Matrix testing across all three roles
- Admin: access to everything
- Docente: access to own content, blocked from others
- Colaborador: access to enrolled content, blocked from admin/docente areas

**Example from `usuarios/tests.py`:**
```python
def test_docente_cannot_access_admin_view(self):
    request = self.factory.get('/test/')
    request.user = self.docente
    decorated_view = role_required('admin')(dummy_view)
    response = decorated_view(request)
    self.assertEqual(response.status_code, 403)
```

### Decorator Tests
**Pattern:** `RequestFactory` + dummy view function
```python
def dummy_view(request, **kwargs):
    return HttpResponse('OK')

class RoleRequiredDecoratorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
```

### Signal Tests
**Pattern:** Disconnect signals in `setUp`, reconnect in `tearDown` when testing service logic independently
- Use `transaction.atomic()` blocks for signal isolation
- Manually trigger signals with `post_save.send()` when disconnected

**Example from `certificados/tests.py`:**
```python
def setUp(self):
    post_save.disconnect(intento_post_save, sender=IntentoEvaluacion)
    post_save.disconnect(clase_completado_post_save, sender=ClaseCompletado)

def tearDown(self):
    post_save.connect(intento_post_save, sender=IntentoEvaluacion)
    post_save.connect(clase_completado_post_save, sender=ClaseCompletado)
```

### Service/Utility Tests
**Pattern:** Direct function/method calls with prepared fixtures
- `CertificateEligibilityService.check_eligibility()` has 12 test cases
- `obtener_o_calcular_progreso()` tested in `cursos/tests.py`

## Test Data Strategy

**No external fixtures or factories** - all test data created inline in `setUp()`
**Standard user creation pattern:**
```python
self.admin = Usuario.objects.create_user(
    username='admin', password='testpass', rol='admin', rut='11111111-1'
)
self.docente = Usuario.objects.create_user(
    username='docente', password='testpass', rol='docente', rut='22222222-2'
)
self.colaborador = Usuario.objects.create_user(
    username='colaborador', password='testpass', rol='colaborador', rut='33333333-3'
)
```

**RUT values:** Hardcoded format `XXXXXXXX-X`, unique per user

## Mocking

**Framework:** Python `unittest.mock` (minimal usage)
**Observed usage:**
- `patch('tareas.views.render', return_value=HttpResponse('ok', status=200))` for view tests that render complex templates

**No mocking of:**
- Database queries
- External services (Supabase storage not mocked in tests)
- Email backend

## Coverage Analysis

### Well-Tested Areas
- **Models:** All major models have dedicated test classes
- **Views:** All core CRUD views have status code and permission tests
- **Forms:** Form validation logic thoroughly tested
- **Decorators:** All custom decorators have unit tests
- **Business logic:** Certificate eligibility service, evaluation scoring, timer logic, question randomization

### Test Coverage Gaps

**Critical untested areas:**

1. **Management commands** (`management/commands/`)
   - Files: `anuncios/management/commands/enviar_anuncios.py`, `calendario/management/commands/generar_eventos_calendario.py`, `certificados/management/commands/actualizar_venimientos.py`, `reportes/management/commands/identificar_riesgo.py`, `usuarios/management/commands/clear_and_setup_cargos.py`
   - Risk: Background/scheduled job logic not verified

2. **Services module** (`certificados/services.py`)
   - Only `CertificateEligibilityService` is tested
   - Other service functions may exist untested

3. **Utility modules**
   - `usuarios/utils.py` (137 lines) - notification and reminder logic mostly untested
   - `cursos/utils.py` - progress calculation utility tested, but edge cases may be missing

4. **Middleware**
   - `usuarios/middleware.py` (`AuditoriaMiddleware`) - no tests found
   - Risk: Request logging and audit trail not verified

5. **Template tags/filters**
   - `calendario/templatetags/calendario_filters.py`
   - `evaluaciones/templatetags/evaluaciones_filters.py`
   - No template tag tests detected

6. **Signals integration**
   - Signal handlers are tested in isolation within apps
   - Cross-app signal interactions not comprehensively tested

7. **File upload handling**
   - Only basic `SimpleUploadedFile` tests in forms
   - Actual storage backend (Supabase) not tested
   - File type validation tested, but file size limits not tested

8. **Error boundaries**
   - 404 handling not systematically tested
   - `get_object_or_404` edge cases rarely tested

9. **Anuncios app**
   - Only 49 lines of tests (smallest test file)
   - Missing view and form tests

10. **Playwright visual tests**
    - Only runs responsive layout checks
    - No functional flow testing (e.g., complete course enrollment → evaluation → certificate)

## Test Execution Time Concerns

**Potential slow tests:**
- Signal integration tests create many database records
- No `@skip` or `@tag` decorators used for slow tests
- No parallel test execution configured

## Recommendations

### High Priority
1. **Add tests for management commands** - These handle critical background processes
2. **Test middleware** - Audit logging is important for compliance
3. **Add template tag tests** - Use `django.template.Context` and `Template` for unit testing filters

### Medium Priority
4. **Create test factories** - Consider `factory_boy` to reduce `setUp` boilerplate across 8 apps
5. **Add integration tests** - End-to-end flow: user creation → course enrollment → class completion → evaluation → certificate
6. **Test file upload edge cases** - Large files, corrupted files, virus scan scenarios
7. **Add performance tests** for report generation (`reportes/views.py` has aggregation queries)

### Low Priority
8. **Add type hints** to test methods for better IDE support
9. **Configure test coverage** with `coverage.py` and set minimum thresholds
10. **Add CI pipeline** to run tests automatically (no GitHub Actions detected)

---

*Testing analysis: 2026-04-24*
