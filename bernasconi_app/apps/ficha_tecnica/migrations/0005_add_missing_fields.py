# Generated manually - Add missing fields to FichaTecnica

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ficha_tecnica', '0004_add_dublin_core_conservation_legal'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichatecnica',
            name='fecha_de_modificacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='fichatecnica',
            name='estado_conservacion',
            field=models.CharField(
                blank=True,
                choices=[('BUENO', 'Bueno'), ('REGULAR', 'Regular'), ('MALO', 'Malo')],
                max_length=20,
                null=True,
                verbose_name='Estado de conservación física'
            ),
        ),
        migrations.AddField(
            model_name='fichatecnica',
            name='tipo_ejemplar',
            field=models.CharField(
                blank=True,
                choices=[
                    ('original', 'Original'),
                    ('copia', 'Copia'),
                    ('serie_1', 'Serie 1'),
                    ('serie_2', 'Serie 2'),
                    ('serie_3', 'Serie 3'),
                    ('serie_4', 'Serie 4'),
                    ('serie_5', 'Serie 5'),
                    ('serie_6', 'Serie 6'),
                ],
                max_length=20,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='fichatecnica',
            name='edicion',
            field=models.CharField(
                blank=True,
                help_text='Ej: 3/50, edición limitada, prueba de artista',
                max_length=255,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='fichatecnica',
            name='series_legacy',
            field=models.TextField(blank=True, null=True),
        ),
    ]
