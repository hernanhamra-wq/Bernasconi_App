from django.db import models


class EstadoObra(models.Model):
    """
    Situación operativa de la obra (dónde está o qué estado tiene).
    Ej: Exposición, Depósito, Cuarentena, En Préstamo, Taller, En Archivo.

    NOTA: El nombre del modelo se mantiene por compatibilidad, pero representa
    la "situación" de la obra, NO su condición física (Bueno/Regular/Malo).
    """
    nombre_estado = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nombre de la situación"
    )

    def __str__(self):
        return self.nombre_estado

    class Meta:
        verbose_name = "Situación de Obra"
        verbose_name_plural = "Situaciones de Obra"
