from django.db import models
from apps.ficha_tecnica.models import FichaTecnica

class Serie(models.Model):
    SI_NO = [
        ("si", "Sí"),
        ("no", "No"),
    ]

    ficha = models.ForeignKey(FichaTecnica, on_delete=models.CASCADE, related_name="series")
    nombre = models.CharField(max_length=255)
    original = models.CharField(max_length=2, choices=SI_NO, default="si")
    anio_impresion = models.DateField(null=True, blank=True)
    taller_reimpresion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Serie"
        verbose_name_plural = "Series"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.ficha_id})"
