from django.db import models
from django.conf import settings


class Donacion(models.Model):

    CONDICION_LEGAL_CHOICES = [
        ('PLENA_PROPIEDAD', 'Plena propiedad'),
        ('COMODATO', 'Comodato'),
        ('DEPOSITO', 'Depósito'),
        ('LEGADO', 'Legado testamentario'),
        ('CESION_TEMPORAL', 'Cesión temporal'),
        ('USUFRUCTO', 'Usufructo'),
        ('EN_TRAMITE', 'En trámite'),
        ('OTRO', 'Otro'),
    ]

    ficha = models.ForeignKey(
        'ficha_tecnica.FichaTecnica',
        on_delete=models.CASCADE,
        related_name='donaciones',
        verbose_name='Ficha técnica'
    )

    institucion_donante = models.ForeignKey(
        'institucion.Institucion',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='donaciones_realizadas',
        verbose_name='Institución donante'
    )

    fecha_donacion = models.DateField(
        verbose_name='Fecha de la donación'
    )

    condicion_legal = models.CharField(
        max_length=50,
        choices=CONDICION_LEGAL_CHOICES,
        default='PLENA_PROPIEDAD',
        verbose_name='Condición legal'
    )

    valuacion = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valuación estimada'
    )

    documento_pdf = models.FileField(
        upload_to='documentos_donacion/',
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Documento PDF'
    )

    observaciones = models.TextField(
        null=True,
        blank=True,
        verbose_name='Observaciones'
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuario que registró'
    )

    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='donaciones_responsable',
        verbose_name='Responsable institucional'
    )

    class Meta:
        verbose_name = 'Donación'
        verbose_name_plural = 'Donaciones'
        ordering = ['-fecha_donacion']

    def __str__(self):
        return f"Donación de {self.ficha} ({self.fecha_donacion})"
