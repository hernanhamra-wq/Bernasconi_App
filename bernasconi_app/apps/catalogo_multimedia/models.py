from django.db import models
from apps.ficha_tecnica.models import FichaTecnica


class CatalogoMultimedia(models.Model):

    TIPO_ARCHIVO = [
        ("imagen", "Imagen"),
        ("video", "Video"),
        ("audio", "Audio"),
        ("documento", "Documento"),
    ]

    ficha = models.ForeignKey(
        FichaTecnica,
        on_delete=models.CASCADE,
        related_name="catalogo_multimedia"
    )

    url_archivo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_ARCHIVO)
    descripcion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Catálogo Multimedia"
        verbose_name_plural = "Catálogos Multimedia"
        ordering = ["ficha", "tipo"]

    def __str__(self):
        return f"{self.ficha_id} - {self.tipo}"
