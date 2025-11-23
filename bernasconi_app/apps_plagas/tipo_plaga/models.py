from django.db import models

class TipoPlaga(models.Model):
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre de la plaga"
    )
    descripcion = models.TextField(
        verbose_name="Descripción general",
        blank=True,
        null=True
    )
    recomendaciones_tratamiento = models.TextField(
        verbose_name="Recomendaciones de tratamiento",
        blank=True,
        null=True
    )
    historial_apariciones = models.TextField(
        verbose_name="Historial de apariciones",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Tipo de plaga"
        verbose_name_plural = "Tipos de plagas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
