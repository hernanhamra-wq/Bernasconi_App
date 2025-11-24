# contenedor_ubicacion/models.py

from django.db import models
from apps_ubicacion.ubicacion_lugar.models import UbicacionLugar

class ContenedorUbicacion(models.Model):

    TIPO_ALMACEN = [
        ("ABIERTO", "Lugar Abierto"),
        ("CERRADO", "Lugar Cerrado"),
    ]

    TIPO_CONTENEDOR = [
        ("CAJON", "Cajón"),
        ("CAJA", "Caja"),
        ("VITRINA", "Vitrina"),
        ("RACK", "Rack"),
        ("ESTANTE", "Estante"),
        ("SOBRE", "Sobre"),
        ("CARPETA", "Carpeta"),
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

    tipo_almacen = models.CharField(
        max_length=20,
        choices=TIPO_ALMACEN
    )

    tipo_contenedor = models.CharField(
        max_length=50,
        choices=TIPO_CONTENEDOR
    )

    observacion = models.CharField(
        max_length=255,
        blank=True
    )

    class Meta:
        verbose_name = "Contenedor de Ubicación"
        verbose_name_plural = "Contenedores de Ubicación"

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
