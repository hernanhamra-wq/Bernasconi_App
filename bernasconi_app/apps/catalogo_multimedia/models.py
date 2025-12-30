from django.db import models
from apps.ficha_tecnica.models import FichaTecnica


def get_upload_path(instance, filename):
    """
    Genera ruta dinámica basada en tipo de archivo.
    Ejemplo: multimedia/imagen/2024/12/foto.jpg
    """
    import datetime
    now = datetime.datetime.now()
    return f'multimedia/{instance.tipo}/{now.year}/{now.month:02d}/{filename}'


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

    # Cambiado de CharField a FileField para gestión real de archivos
    archivo = models.FileField(
        upload_to=get_upload_path,
        max_length=255,
        null=True,  # Permitir null para migración de datos existentes
        blank=True,
        verbose_name="Archivo multimedia"
    )

    tipo = models.CharField(max_length=20, choices=TIPO_ARCHIVO)
    descripcion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Catálogo Multimedia"
        verbose_name_plural = "Catálogos Multimedia"
        ordering = ["ficha", "tipo"]

    def __str__(self):
        return f"{self.ficha_id} - {self.tipo}"
