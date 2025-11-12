from django.db import models

# ===================================================================
# MODELO COLABORACION (intermedia entre Obra y Autor)
# ===================================================================
class Colaboracion(models.Model):
    obra = models.ForeignKey('Obra', on_delete=models.CASCADE)
    autor = models.ForeignKey('Autor', on_delete=models.CASCADE)
    rol = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'catalogo_colaboracion'
        unique_together = ('obra', 'autor')
        verbose_name = "Colaboración"
        verbose_name_plural = "Colaboraciones"

    def __str__(self):
        return f"{self.autor} ({self.rol}) en {self.obra}"