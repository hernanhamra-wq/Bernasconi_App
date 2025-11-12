from django.db import models

# ===================================================================
# MODELO MULTIMEDIA
# ===================================================================
class Multimedia(models.Model):
    """Modelo para almacenar multimedia asociada a una obra (fotos, videos)."""
    
    url_foto = models.URLField(
        max_length=500, 
        null=True, 
        blank=True,
        verbose_name="URL Foto"
    )
    url_video = models.URLField(
        max_length=500, 
        null=True, 
        blank=True,
        verbose_name="URL Video"
    )
    descripcion = models.TextField(
        null=True, 
        blank=True,
        verbose_name="Descripción"
    )
    fk_obra = models.ForeignKey(
        'Obra', 
        on_delete=models.CASCADE, 
        related_name='multimedia',
        verbose_name="Obra asociada"
    )

    class Meta:
        db_table = 'catalogo_multimedia'
        verbose_name = "Multimedia"
        verbose_name_plural = "Multimedias"
        ordering = ['id']

    def __str__(self):
        tipo = "Foto" if self.url_foto else "Video"
