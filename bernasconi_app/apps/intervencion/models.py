from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Intervencion(models.Model):
    intervencion_id = models.AutoField(primary_key=True)

    ficha = models.ForeignKey(
        'ficha_tecnica.FichaTecnica',
        on_delete=models.CASCADE,
        related_name='intervenciones',
        verbose_name='Ficha técnica'
    )

    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='intervenciones_realizadas',
        verbose_name='Responsable'
    )

    n_intervencion = models.PositiveIntegerField(verbose_name='Número de intervención')

    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
    fecha_finalizacion = models.DateField(verbose_name='Fecha de finalización', null=True, blank=True)

    diagnostico = models.TextField(verbose_name='Diagnóstico técnico')
    procedimientos = models.TextField(verbose_name='Procedimientos aplicados')
    materiales_utilizados = models.TextField(verbose_name='Materiales utilizados')

    class Meta:
        db_table = 'intervencion'
        verbose_name = 'Intervención'
        verbose_name_plural = 'Intervenciones'
        ordering = ['ficha', 'n_intervencion']

    def __str__(self):
        return f"Intervención {self.n_intervencion} – {self.ficha}"
