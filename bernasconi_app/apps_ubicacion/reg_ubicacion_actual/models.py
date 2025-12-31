"""
MODELO DE UBICACIÓN INICIAL (SNAPSHOT LEGACY)

Este modelo almacena la ubicación inicial de cada obra migrada desde el sistema legacy.
Representa la "foto" de dónde estaban las obras al momento de la migración (6,912 registros).

USO ACTUAL:
- Almacena ubicación inicial migrada desde CSV (sector/sala/caja)
- Se usa como punto de partida antes de que existan movimientos

RELACIÓN CON RegHistorialMov:
- RegUbicacionActual: Ubicación inicial (datos legacy)
- RegHistorialMov: Movimientos futuros (trazabilidad)
- FichaTecnica.ubicacion_actual(): Calcula ubicación actual desde el último movimiento,
  o retorna None si no hay movimientos (usar este modelo como fallback)

Script de migración: _08_ubicacion_inicial.py
"""
from django.db import models
from django.conf import settings
from apps.ficha_tecnica.models import FichaTecnica
from apps.estado_obra.models import EstadoObra
from apps_ubicacion.ubicacion_lugar.models import UbicacionLugar
from apps_ubicacion.contenedor_ubicacion.models import ContenedorUbicacion


class RegUbicacionActual(models.Model):
    """
    Ubicación inicial de la obra (migrada desde sistema legacy).

    Para obtener ubicación actual:
    1. Buscar último movimiento en RegHistorialMov
    2. Si no hay movimientos, usar este registro como fallback
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
