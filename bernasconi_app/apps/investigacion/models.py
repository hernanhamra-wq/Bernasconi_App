from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Investigacion(models.Model):
    investigacion_id = models.AutoField(primary_key=True)

    ficha = models.ForeignKey(
        'ficha_tecnica.FichaTecnica',
        on_delete=models.CASCADE,
        related_name='investigaciones',
        verbose_name='Ficha técnica'
    )

    investigador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='investigaciones_realizadas',
        verbose_name='Investigador'
    )

    num_investigacion = models.PositiveIntegerField(verbose_name='Número de investigación')

    titulo_investigacion = models.CharField(
        max_length=255,
        verbose_name='Título de la investigación'
    )

    detalle_investigacion = models.TextField(verbose_name='Detalle')

    anio_realizacion = models.PositiveIntegerField(verbose_name='Año de realización')

    class Meta:
        db_table = 'investigacion'
        verbose_name = 'Investigación'
        verbose_name_plural = 'Investigaciones'
        ordering = ['ficha', 'num_investigacion']

    def __str__(self):
        return f"{self.titulo_investigacion} ({self.anio_realizacion})"
