# Kimün POST Handling Audit

Scope: all `views.py` files across the 8 Django apps in this repository.

## Summary
- Raw POST handling found in 2 files only: `usuarios/views.py` and `evaluaciones/views.py`.
- No `request.POST[...]` bracket access was found.
- No other `views.py` files contained `request.POST.get(` or `json.loads(request.POST...)` matches.

## Findings

| File | Line(s) | Snippet | Category | Notes |
|---|---:|---|---|---|
| `/home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/usuarios/views.py` | 41-42 | `username = request.POST.get('username')` / `password = request.POST.get('password')` | b) intentional raw POST | Login form uses direct credentials lookup before `authenticate()`. This is standard for auth flows; not a ModelForm candidate. Prefer `AuthenticationForm` only if standardizing UX/validation. |
| `/home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/usuarios/views.py` | 340 | `usuario_id = request.POST.get('usuario_id')` | c) simple form processing that could use Form but not critical | Course enrollment picks a user by id and creates an `InscripcionCurso`. A small `Form` with `ModelChoiceField` would improve validation and reduce manual lookup, but current pattern is straightforward. |
| `/home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/evaluaciones/views.py` | 67 | `preguntas_data = json.loads(request.POST.get('preguntas', '[]'))` | b) intentional raw POST | Custom nested question payload is being submitted alongside `EvaluacionForm`. This is not a `ModelForm` concern; it is custom JSON handling. Keep only if the frontend intentionally sends serialized questions. |
| `/home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/evaluaciones/views.py` | 128 | `preguntas_data = json.loads(request.POST.get('preguntas', '[]'))` | b) intentional raw POST | Same pattern in edit flow. The base evaluation fields are handled by `EvaluacionForm`; the question payload is custom and should remain separate or be refactored to a dedicated `FormSet`/serializer. |
| `/home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/evaluaciones/views.py` | 267 | `respuestas = json.loads(request.POST.get('respuestas', '{}'))` | b) intentional raw POST | AJAX/JSON-style answer submission. This should stay custom, but it needs strong input validation because the payload comes from the client and drives scoring logic. |
| `/home/sebacc/Documents/UDD/Ingeniería de Software/Proyecto-Kimün/evaluaciones/views.py` | 451 | `preguntas_data = json.loads(request.POST.get('preguntas', '[]'))` | b) intentional raw POST | Bank question bulk-create endpoint. Raw JSON is reasonable here, but it is still user-controlled structured input and should be validated carefully. |

## Security / Robustness Notes
- `evaluaciones/views.py` relies on `json.loads()` of client input in 4 places; malformed JSON is partially handled, but nested keys still assume trusted structure (`pregunta_data['texto']`, `alt_data['texto']`, `pregunta_data['alternativas']`).
- Bulk question creation/editing can still raise errors if payload shape is wrong after parsing; validation should cover required keys, types, and array lengths.
- The login flow does not use `AuthenticationForm`, so it lacks built-in field-level validation and standardized error handling, though the current usage is acceptable.
- The enrollment view manually trusts `usuario_id`; switching to a `Form` with `ModelChoiceField` would add cleaner validation and clearer error reporting.
- No direct `request.POST[...]` access was found, which reduces KeyError risk on top-level POST fields.

## Recommendation
- Keep the auth and AJAX JSON endpoints as intentional raw POST handling, but document them and strengthen validation.
- Refactor the enrollment view to a small Django `Form` if you want consistency and better validation.
- Consider a `FormSet`/structured serializer approach for evaluation question payloads if this area is likely to grow.
