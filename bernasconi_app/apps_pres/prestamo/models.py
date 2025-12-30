from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Prestamo(models.Model):

    ESTADO_CHOICES = [
        ('SOLICITADO', 'Solicitado'),
        ('EN_EVALUACION', 'En evaluación'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('EN_PREPARACION', 'En preparación'),
        ('EN_TRANSITO_IDA', 'En tránsito (ida)'),
        ('EN_DESTINO', 'En destino'),
        ('EN_TRANSITO_VUELTA', 'En tránsito (vuelta)'),
        ('DEVUELTO', 'Devuelto'),
        ('CANCELADO', 'Cancelado'),
    ]

    ficha = models.ForeignKey(
        'ficha_tecnica.FichaTecnica',
        on_delete=models.CASCADE,
        related_name='prestamos'
    )

    institucion_origen = models.ForeignKey(
        'institucion.Institucion',
        on_delete=models.SET_NULL,
        null=True,
        related_name='prestamos_origen'
    )

    institucion_destino = models.ForeignKey(
        'institucion.Institucion',
        on_delete=models.SET_NULL,
        null=True,
        related_name='prestamos_destino'
    )

    n_de_prestamo = models.CharField(max_length=50)
    direccion_destino = models.CharField(max_length=255, blank=True, null=True)
    contacto_destino = models.CharField(max_length=255, blank=True, null=True)
    seguro_solicitado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_traslado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    fecha_inicio = models.DateField()
    fecha_fin_prevista = models.DateField()
    fecha_devolucion_real = models.DateField(blank=True, null=True)

    requisitos_especiales = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    estado = models.CharField(
        max_length=50,
        choices=ESTADO_CHOICES,
        default='SOLICITADO',
        verbose_name='Estado del préstamo'
    )

    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='prestamos_responsable'
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='prestamos_cargados'
    )

    def __str__(self):
        return f"Préstamo {self.n_de_prestamo} - {self.ficha}"
