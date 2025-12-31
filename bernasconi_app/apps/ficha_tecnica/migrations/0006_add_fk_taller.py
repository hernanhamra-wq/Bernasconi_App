# Generated manually - Add FK taller to FichaTecnica

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ficha_tecnica', '0005_add_missing_fields'),
        ('taller', '0002_remove_taller_contacto_taller_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichatecnica',
            name='fk_taller',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='taller.taller'
            ),
        ),
    ]
