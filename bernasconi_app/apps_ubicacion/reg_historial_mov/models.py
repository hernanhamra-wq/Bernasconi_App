from django.db import models
from django.conf import settings

from apps.ficha_tecnica.models import FichaTecnica
from apps.estado_obra.models import EstadoObra
from apps_ubicacion.ubicacion_lugar.models import UbicacionLugar
from apps_ubicacion.contenedor_ubicacion.models import ContenedorUbicacion


class RegHistorialMov(models.Model):
    fk_ficha = models.ForeignKey(
        FichaTecnica,
        on_delete=models.CASCADE,
        related_name="historial_movimientos"
    )

    fk_estado = models.ForeignKey(
        EstadoObra,
        on_delete=models.SET_NULL,
        null=True,
        related_name="historial_movimientos"
    )

    fk_lugar_destino = models.ForeignKey(
        UbicacionLugar,
        on_delete=models.SET_NULL,
        null=True,
        related_name="historial_movimientos_destino"
    )

    fk_contenedor_destino = models.ForeignKey(
        ContenedorUbicacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="historial_movimientos_destino"
    )

    fecha_movimiento = models.DateTimeField(auto_now_add=True)

    fk_responsable_mov = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="movimientos_realizados"
    )

    motivo = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Movimiento de {self.fk_ficha} → {self.fk_lugar_destino} ({self.fecha_movimiento})"
