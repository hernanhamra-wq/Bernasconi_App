from django.db import models

# ===================================================================
# MODELO TIPO DE MATERIAL
# ===================================================================
class MaterialTipo(models.Model):
    """Modelo para representar los tipos de material (ej: Pintura, Escultura, Documento, etc.)"""
    
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre del tipo de material"
    )
    descripcion = models.TextField(
        null=True,
        blank=True,
        verbose_name="Descripción"
    )

    class Meta:
        verbose_name = "Tipo de Material"
        verbose_name_plural = "Tipos de Material"
        db_table = "catalogo_material_tipos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
