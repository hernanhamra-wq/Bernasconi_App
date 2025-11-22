from django.db import models

class EstadoObra(models.Model):
    nombre_estado = models.CharField(
        max_length=50,
        unique=True,              # ✅ evita duplicados
        verbose_name="Condición funcional"
    )

    def __str__(self):
        return self.nombre_estado

    class Meta:
        verbose_name = "Estado de Obra"
        verbose_name_plural = "Estados de Obra"
