from django.db import migrations, models


def fix_certificado_activo(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        if schema_editor.connection.vendor == 'postgresql':
            cursor.execute("""
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'cursos_curso' AND column_name = 'certificado_activo'
            """)
            if cursor.fetchone():
                cursor.execute(
                    "ALTER TABLE cursos_curso ALTER COLUMN certificado_activo DROP NOT NULL;"
                )
            else:
                cursor.execute(
                    "ALTER TABLE cursos_curso ADD COLUMN certificado_activo BOOLEAN DEFAULT FALSE;"
                )
        elif schema_editor.connection.vendor == 'sqlite':
            cursor.execute("PRAGMA table_info(cursos_curso)")
            rows = cursor.fetchall()
            exists = any(row[1] == 'certificado_activo' for row in rows)
            if not exists:
                cursor.execute(
                    "ALTER TABLE cursos_curso ADD COLUMN certificado_activo BOOLEAN DEFAULT 0;"
                )


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0007_clase_add_constraints_and_default'),
    ]

    operations = [
        migrations.RunPython(fix_certificado_activo, migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='curso',
                    name='certificado_activo',
                    field=models.BooleanField(default=False, null=True),
                ),
            ],
        ),
    ]
