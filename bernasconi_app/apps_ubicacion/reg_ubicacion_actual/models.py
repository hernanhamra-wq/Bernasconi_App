"""
MODELO DEPRECADO - Mantener solo por compatibilidad con datos existentes.

La ubicación actual ahora se calcula dinámicamente desde RegHistorialMov
usando FichaTecnica.ubicacion_actual()

Este modelo será eliminado en una versión futura.
"""
from django.db import models
from django.conf import settings
from apps.ficha_tecnica.models import FichaTecnica
from apps.estado_obra.models import EstadoObra
from apps_ubicacion.ubicacion_lugar.models import UbicacionLugar
from apps_ubicacion.contenedor_ubicacion.models import ContenedorUbicacion


class RegUbicacionActual(models.Model):
    """
    DEPRECADO: Usar FichaTecnica.ubicacion_actual() en su lugar.
    Este modelo se mantiene temporalmente por compatibilidad.
    """
    fk_ficha = models.ForeignKey(
        FichaTecnica,
        on_delete=models.CASCADE,
        related_name="ubicacion_actual"
    )

    fk_estado = models.ForeignKey(
        EstadoObra,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ubicaciones_actuales"
    )

    fk_lugar = models.ForeignKey(
        UbicacionLugar,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ubicaciones_actuales"
    )

    fk_contenedor = models.ForeignKey(
        ContenedorUbicacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ubicaciones_actuales"
    )

    fecha_desde = models.DateTimeField(auto_now_add=True)

    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='ubicaciones_registradas',
        verbose_name='Usuario que registró'
    )

    def __str__(self):
        return f"{self.fk_ficha} en {self.fk_lugar} desde {self.fecha_desde}"
