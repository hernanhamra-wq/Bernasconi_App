from django.db import models


class UbicacionLugar(models.Model):

    TIPO_LUGAR_CHOICES = [
        ('SALA', 'Sala de exposición'),
        ('DEPOSITO', 'Depósito'),
        ('TALLER', 'Taller de restauración'),
        ('ARCHIVO', 'Archivo'),
        ('LABORATORIO', 'Laboratorio'),
        ('EXTERNO', 'Ubicación externa'),
    ]

    nombre_lugar = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre del lugar"
    )

    tipo_lugar = models.CharField(
        max_length=50,
        choices=TIPO_LUGAR_CHOICES,
        verbose_name="Tipo de lugar"
    )

    permite_contenedores = models.BooleanField(
        default=False,
        verbose_name="¿Permite contenedores?"
    )

    observacion = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )

    def __str__(self):
        return f"{self.nombre_lugar} ({self.tipo_lugar})"

    class Meta:
        verbose_name = "Lugar físico"
        verbose_name_plural = "Lugares físicos"
        ordering = ["nombre_lugar"]
