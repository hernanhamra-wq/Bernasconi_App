from django.db import models

# ===================================================================
# MODELO UBICACION
# ===================================================================
class Ubicacion(models.Model):
    """Modelo para ubicar físicamente una obra en el museo o depósito."""
    
    sector = models.CharField(max_length=100, verbose_name="Sector")
    sala = models.CharField(max_length=100, verbose_name="Sala", null=True, blank=True)
    caja = models.CharField(max_length=50, verbose_name="Caja", null=True, blank=True)
    
    class Meta:
        db_table = 'catalogo_ubicacion'
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"
        ordering = ['sector', 'sala', 'caja']

    def __str__(self):
        ubic = f"{self.sector}"
        if self.sala:
            ubic += f" / {self.sala}"
        if self.caja:
            ubic += f" / {self.caja}"
        return ubic
