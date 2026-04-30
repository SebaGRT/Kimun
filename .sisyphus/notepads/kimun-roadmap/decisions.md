Used a management command with --dry-run so announcement dispatch can be inspected before sending emails.
Kept at-risk detection in reportes.views as a shared helper so the dashboard and identificar_riesgo command stay consistent without duplicating business rules.

## 2025-04-23 — Material Upload Extension (video_file, office)

1. **Keep generic fields**: Decided NOT to add new model fields (e.g., `video_archivo`, `office_archivo`). The existing `archivo` and `url` fields are generic and sufficient; adding fields would complicate the model and require migration overhead.
2. **File extension validation in Form, not Model**: Validation logic for allowed extensions (`.pdf`, `.mp4`, `.docx`, etc.) lives in `MaterialForm.clean()` rather than a model validator. This keeps the model lightweight and allows the form to provide user-friendly error messages.
3. **Lowercase extension comparison**: All extension checks use `nombre.endswith('.ext')` after calling `.lower()` on the filename. This is a simple, effective case-insensitive approach without needing regex.
4. **Video player replaces download link for video_file**: In `curso_detail.html`, `video_file` materials show an inline `<video controls>` player instead of a "Descargar" button. For `office` materials, the standard download link is retained.
5. **Color/icon mapping per type**:
   - `pdf` → primary color, `bi-file-earmark-pdf`
   - `video` → danger color, `bi-play-circle`
   - `video_file` → danger color, `bi-film`
   - `office` → success color, `bi-file-earmark-text`
