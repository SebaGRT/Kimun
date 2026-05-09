#!/bin/bash
cp -r ../kimun ../manage.py ../requirements.txt ../certificados ../usuarios ../cursos ../evaluaciones ../tareas ../reportes ../calendario ../anuncios ../templates ../static ../media ../.env.vercel.local . 2>/dev/null || true
(
  # Use SQLite during collectstatic so we don't need psycopg2 in the build step
  unset SUPABASE_DB_HOST
  python manage.py collectstatic --noinput
)
