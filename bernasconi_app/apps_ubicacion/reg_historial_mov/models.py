from django.db import models
from django.conf import settings

from apps.ficha_tecnica.models import FichaTecnica
from apps.estado_obra.models import EstadoObra
from apps_ubicacion.ubicacion_lugar.models import UbicacionLugar
from apps_ubicacion.contenedor_ubicacion.models import ContenedorUbicacion


class RegHistorialMov(models.Model):

    MOTIVO_CHOICES = [
        ('EXPOSICION', 'Exposición'),
        ('RESTAURACION', 'Restauración'),
        ('PRESTAMO', 'Préstamo'),
        ('ALMACENAMIENTO', 'Almacenamiento'),
        ('INVESTIGACION', 'Investigación'),
        ('FOTOGRAFIA', 'Fotografía/Documentación'),
        ('MANTENIMIENTO', 'Mantenimiento'),
        ('REUBICACION', 'Reubicación'),
        ('CUARENTENA', 'Cuarentena'),
        ('EMERGENCIA', 'Emergencia'),
        ('OTRO', 'Otro'),
    ]

    ESTADO_MOVIMIENTO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_TRANSITO', 'En tránsito'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]
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

    # ============================================================
    # ORIGEN del movimiento
    # ============================================================
    fk_lugar_origen = models.ForeignKey(
        UbicacionLugar,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="historial_movimientos_origen",
        verbose_name="Lugar de origen"
    )

    fk_contenedor_origen = models.ForeignKey(
        ContenedorUbicacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="historial_movimientos_origen",
        verbose_name="Contenedor de origen"
    )

    # ============================================================
    # DESTINO del movimiento
    # ============================================================
    fk_lugar_destino = models.ForeignKey(
        UbicacionLugar,
        on_delete=models.SET_NULL,
        null=True,
        related_name="historial_movimientos_destino",
        verbose_name="Lugar de destino"
    )

    fk_contenedor_destino = models.ForeignKey(
        ContenedorUbicacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="historial_movimientos_destino",
        verbose_name="Contenedor de destino"
    )

    # ============================================================
    # DATOS del movimiento
    # ============================================================
    fecha_movimiento = models.DateTimeField(auto_now_add=True)

    fk_responsable_mov = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        related_name="movimientos_realizados",
        verbose_name="Responsable del movimiento"
    )

    motivo = models.CharField(
        max_length=50,
        choices=MOTIVO_CHOICES,
        default='OTRO',
        verbose_name="Motivo del movimiento"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_MOVIMIENTO_CHOICES,
        default='COMPLETADO',
        verbose_name="Estado del movimiento"
    )

    observaciones = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observaciones"
    )

    def __str__(self):
        return f"Movimiento de {self.fk_ficha} → {self.fk_lugar_destino} ({self.fecha_movimiento})"
