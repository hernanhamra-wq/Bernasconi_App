from django.db import models


# ===================================================================
# MODELO OBRA (Catálogo Maestro) (Tabla: catalogo_obras)
# ===================================================================
class Obra(models.Model):
    """Modelo principal que representa una Obra en el catálogo."""
    
    titulo = models.CharField(max_length=200)
    
    # RELACIÓN: Muchos a Muchos. Usa la tabla 'Colaboracion'.
    autores = models.ManyToManyField(
        'Autor', 
        through='Colaboracion',
        related_name='obras_participadas', 
        verbose_name="Autores y Colaboradores"
    )
    
    TIPO_CHOICES = (
        ('L', 'Libro'),
        ('A', 'Artículo'),
        ('E', 'Ensayo'),
        ('O', 'Otro'),
    )
    tipo_obra = models.CharField(
        max_length=1, 
        choices=TIPO_CHOICES, 
        default='L',
        verbose_name="Tipo de Obra"
    )
    
    fecha_publicacion = models.IntegerField(
        null=True, 
        blank=True,
        verbose_name="Año de Publicación"
    )
    
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Obra"
        verbose_name_plural = "Obras"
        # Renombra la tabla principal a 'catalogo_obras'
        db_table = 'catalogo_obras'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo
