from django.db import models
from django.conf import settings  # Para usuario personalizado

class Prestamo(models.Model):
    fk_item = models.ForeignKey(
        'Obra', on_delete=models.CASCADE, db_column='fk_item_id', verbose_name="Obra / Item"
    )
    fk_organizacion_origen = models.ForeignKey(
        'Organizacion', on_delete=models.SET_NULL, null=True, related_name='prestamos_origen', db_column='fk_organizacion_origen'
    )
    fk_organizacion_destino = models.ForeignKey(
        'Organizacion', on_delete=models.SET_NULL, null=True, related_name='prestamos_destino', db_column='fk_organizacion_destino'
    )
    fk_responsable_prestamo = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, db_column='fk_responsable_prestamo', verbose_name="Responsable del préstamo"
    )

    n_de_prestamo = models.CharField(max_length=50, unique=True)
    solicitante = models.CharField(max_length=200, verbose_name="Solicitante")
    direccion_destino = models.CharField(max_length=200, null=True, blank=True)
    contacto_destino = models.CharField(max_length=200, null=True, blank=True)
    seguro_soliditado = models.BooleanField(default=False)
    costo_traslado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin_prevista = models.DateField(null=True, blank=True)
    fecha_devolucion_real = models.DateField(null=True, blank=True)
    fecha_devolucion_estimada = models.DateField(null=True, blank=True)
    requisitos_especiales = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    devuelto = models.BooleanField(default=False)

    class Meta:
        db_table = 'catalogo_prestamos'
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"Préstamo {self.n_de_prestamo} - {self.fk_item}"
