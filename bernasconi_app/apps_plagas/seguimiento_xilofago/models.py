from django.db import models
# 💡 Importación necesaria para la ForeignKey
from apps_plagas.registro_plaga.models import RegistroPlaga 

class SeguimientoXilofago(models.Model):
    # Clave Primaria
    seguimiento_id = models.AutoField(primary_key=True)
    
    # 🌟 CORRECCIÓN/MEJORA: Usar la clase importada (RegistroPlaga) en lugar de la cadena de texto larga.
    registro_plaga = models.ForeignKey(
        RegistroPlaga, # Uso directo de la clase importada
        on_delete=models.CASCADE,
        related_name='seguimientos'
    )
    
    # Campos de Datos
    fecha_seguimiento = models.DateField()
    observacion = models.TextField()
    nueva_actividad = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Opcional: baja, alta, nula"
    )

    class Meta:
        verbose_name = "Seguimiento xilófago"
        verbose_name_plural = "Seguimientos xilófagos"
        # Ordenar por fecha_seguimiento de forma descendente
        ordering = ['-fecha_seguimiento']

    def __str__(self):
        # Muestra el ID y la fecha del seguimiento
        return f"Seguimiento {self.seguimiento_id} - {self.fecha_seguimiento}"