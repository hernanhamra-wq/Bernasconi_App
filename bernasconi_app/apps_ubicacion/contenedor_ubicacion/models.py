# contenedor_ubicacion/models.py

from django.db import models
from apps_ubicacion.ubicacion_lugar.models import UbicacionLugar

class ContenedorUbicacion(models.Model):

    MODO_ALMACENAMIENTO = [
        ("DIRECTO", "Directo (sin contenedor)"),
        ("EN_CONTENEDOR", "Dentro de contenedor"),
    ]

    ESTADO_CONTENEDOR = [
        ("DISPONIBLE", "Disponible"),
        ("PARCIAL", "Parcialmente ocupado"),
        ("LLENO", "Lleno"),
        ("EN_REPARACION", "En reparación"),
        ("BAJA", "Dado de baja"),
    ]

    TIPO_CONTENEDOR = [
        ("CAJON", "Cajón"),
        ("CAJA", "Caja"),
        ("VITRINA", "Vitrina"),
        ("RACK", "Rack"),
        ("ESTANTE", "Estante"),
        ("SOBRE", "Sobre"),
        ("CARPETA", "Carpeta"),
        ("PLANERO", "Planero"),
        ("PESEBRE", "Pesebre"),
        ("TUBO", "Tubo"),
        ("OTRO", "Otro"),
    ]

    nombre_contenedor = models.CharField(max_length=100)

    fk_lugar_general = models.ForeignKey(
        UbicacionLugar,
        on_delete=models.CASCADE,
        verbose_name="Lugar general"
    )

    fk_padre = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subcontenedores",
        verbose_name="Contenedor padre"
    )

    modo_almacenamiento = models.CharField(
        max_length=20,
        choices=MODO_ALMACENAMIENTO,
        default='EN_CONTENEDOR',
        verbose_name="Modo de almacenamiento"
    )

    tipo_contenedor = models.CharField(
        max_length=50,
        choices=TIPO_CONTENEDOR
    )

    observacion = models.CharField(
        max_length=255,
        blank=True
    )

    # ============================================================
    # CAPACIDAD Y ESTADO
    # ============================================================
    capacidad_maxima = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Capacidad máxima (obras)",
        help_text="Cantidad máxima de obras que puede contener. Dejar vacío si no aplica."
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CONTENEDOR,
        default='DISPONIBLE',
        verbose_name="Estado del contenedor"
    )

    class Meta:
        verbose_name = "Contenedor de Ubicación"
        verbose_name_plural = "Contenedores de Ubicación"
        constraints = [
            models.UniqueConstraint(
                fields=['nombre_contenedor', 'fk_lugar_general'],
                name='unique_contenedor_por_lugar'
            )
        ]

    def __str__(self):
        return self.nombre_contenedor

    # Ruta completa (útil en el admin)
    def ruta_completa(self):
        actual = self
        partes = []
        while actual:
            partes.append(actual.nombre_contenedor)
            actual = actual.fk_padre
        return " > ".join(reversed(partes))

    def obras_actuales(self):
        """
        Cuenta las obras actualmente ubicadas en este contenedor.
        Busca en el historial de movimientos el último movimiento COMPLETADO
        de cada ficha y cuenta las que tienen este contenedor como destino.
        """
        from apps.ficha_tecnica.models import FichaTecnica
        from django.db.models import Max, Subquery, OuterRef

        # Subquery para obtener el último movimiento de cada ficha
        ultimo_mov_subquery = FichaTecnica.objects.filter(
            historial_movimientos__estado='COMPLETADO'
        ).annotate(
            ultimo_mov_id=Max('historial_movimientos__id')
        ).values('ultimo_mov_id')

        # Contar movimientos donde el destino es este contenedor
        from apps_ubicacion.reg_historial_mov.models import RegHistorialMov
        return RegHistorialMov.objects.filter(
            id__in=Subquery(ultimo_mov_subquery),
            fk_contenedor_destino=self,
            estado='COMPLETADO'
        ).count()

    def espacio_disponible(self):
        """
        Retorna True si hay espacio disponible en el contenedor.
        Si no tiene capacidad_maxima definida, siempre retorna True.
        """
        if self.capacidad_maxima is None:
            return True
        return self.obras_actuales() < self.capacidad_maxima

    def porcentaje_ocupacion(self):
        """
        Retorna el porcentaje de ocupación del contenedor.
        Si no tiene capacidad_maxima, retorna None.
        """
        if self.capacidad_maxima is None or self.capacidad_maxima == 0:
            return None
        return round((self.obras_actuales() / self.capacidad_maxima) * 100, 1)
