from django.db import models

# ===================================================================
# MODELO AUTOR
# ===================================================================
class Autor(models.Model):
    """Modelo para representar a un Autor, coautor o colaborador."""
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    
    biografia = models.TextField(
        null=True, 
        blank=True,
        verbose_name="Biografía / Descripción"
    )
    
    fecha_nacimiento = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha de Nacimiento"
    )
    nacionalidad = models.CharField(
        max_length=50, 
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        db_table = 'catalogo_autores'
        unique_together = ('nombre', 'apellido')
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


# ===================================================================

