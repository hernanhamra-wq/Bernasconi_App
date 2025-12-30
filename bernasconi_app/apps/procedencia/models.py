from django.db import models
from apps.core.models import AuditableModel


class Procedencia(AuditableModel):
    """
    Tabla reutilizable para registrar el origen de las obras.

    Permite:
    - Asociar múltiples obras a la misma procedencia (ej: 10 obras del mismo donante)
    - Mantener historial de adquisiciones
    - Generar reportes por tipo de procedencia
    """

    TIPO_CHOICES = [
        ('DONACION', 'Donación'),
        ('COMPRA', 'Compra'),
        ('LEGADO', 'Legado'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('EXCAVACION', 'Excavación'),
        ('COMODATO', 'Comodato'),
        ('DEPOSITO', 'Depósito'),
        ('DESCONOCIDO', 'Desconocido'),
    ]

    nombre = models.CharField(
        max_length=255,
        verbose_name="Nombre/Descripción",
        help_text="Nombre del donante, vendedor o descripción de la procedencia"
    )

    tipo_procedencia = models.CharField(
        max_length=50,
        choices=TIPO_CHOICES,
        default='DESCONOCIDO',
        verbose_name="Tipo de procedencia"
    )

    pais = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="País de origen"
    )

    region = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Región/Provincia"
    )

    localidad = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Localidad"
    )

    fecha_adquisicion = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de adquisición"
    )

    documentacion = models.TextField(
        null=True,
        blank=True,
        verbose_name="Documentación de respaldo",
        help_text="Referencias a documentos legales, actas, etc."
    )

    observaciones = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observaciones"
    )

    class Meta:
        verbose_name = "Procedencia"
        verbose_name_plural = "Procedencias"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_procedencia_display()})"
