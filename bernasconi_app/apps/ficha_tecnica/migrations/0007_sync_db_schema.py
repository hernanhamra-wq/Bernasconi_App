# Generated manually - Sync DB schema with model

from django.db import migrations


def rename_column(apps, schema_editor):
    """Rename fk_estado_id to fk_estado_funcional_id and drop fk_serie_id."""
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        # Check if old column exists
        cursor.execute("SHOW COLUMNS FROM ficha_tecnica_fichatecnica LIKE 'fk_estado_id'")
        if cursor.fetchone():
            cursor.execute(
                "ALTER TABLE ficha_tecnica_fichatecnica "
                "CHANGE COLUMN fk_estado_id fk_estado_funcional_id BIGINT NULL"
            )

        # Check if fk_serie_id exists and drop it
        cursor.execute("SHOW COLUMNS FROM ficha_tecnica_fichatecnica LIKE 'fk_serie_id'")
        if cursor.fetchone():
            # First drop foreign key if exists
            cursor.execute(
                "SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE "
                "WHERE TABLE_NAME = 'ficha_tecnica_fichatecnica' "
                "AND COLUMN_NAME = 'fk_serie_id' "
                "AND REFERENCED_TABLE_NAME IS NOT NULL"
            )
            for row in cursor.fetchall():
                cursor.execute(
                    f"ALTER TABLE ficha_tecnica_fichatecnica DROP FOREIGN KEY {row[0]}"
                )
            cursor.execute(
                "ALTER TABLE ficha_tecnica_fichatecnica DROP COLUMN fk_serie_id"
            )


def reverse_rename(apps, schema_editor):
    """Reverse the rename."""
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        cursor.execute("SHOW COLUMNS FROM ficha_tecnica_fichatecnica LIKE 'fk_estado_funcional_id'")
        if cursor.fetchone():
            cursor.execute(
                "ALTER TABLE ficha_tecnica_fichatecnica "
                "CHANGE COLUMN fk_estado_funcional_id fk_estado_id BIGINT NULL"
            )


class Migration(migrations.Migration):

    dependencies = [
        ('ficha_tecnica', '0006_add_fk_taller'),
    ]

    operations = [
        migrations.RunPython(rename_column, reverse_rename),
    ]
