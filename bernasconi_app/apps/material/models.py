from django.db import models

class Material(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class FichaTecnicaMaterial(models.Model):
    ficha = models.ForeignKey(
        "ficha_tecnica.FichaTecnica",  # ✅ correcto, referencia a apps.ficha_tecnica
        on_delete=models.CASCADE,
        related_name="materiales_relacion"
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="fichas_relacion"
    )
    detalle = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="(Opcional) Ej: técnica específica del material"
    )

    class Meta:
        verbose_name = "Relación Ficha–Material"
        verbose_name_plural = "Relaciones Ficha–Material"
        unique_together = ("ficha", "material")

    def __str__(self):
        return f"{self.ficha} → {self.material}"
