from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0008_curso_certificado_activo'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='curso',
                    name='certificado_requiere_clases',
                    field=models.BooleanField(default=False),
                ),
                migrations.AddField(
                    model_name='curso',
                    name='certificado_requiere_evaluaciones',
                    field=models.BooleanField(default=False),
                ),
                migrations.AddField(
                    model_name='curso',
                    name='certificado_porcentaje_minimo_clases',
                    field=models.PositiveIntegerField(default=0),
                ),
                migrations.AddField(
                    model_name='curso',
                    name='certificado_vigencia_meses',
                    field=models.PositiveIntegerField(default=12),
                ),
            ],
        ),
    ]
