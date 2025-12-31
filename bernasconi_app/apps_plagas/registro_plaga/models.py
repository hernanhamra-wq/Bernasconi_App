from django.db import models
from django.conf import settings
from apps.ficha_tecnica.models import FichaTecnica
from apps_plagas.manejo_plagas.models import ManejoPlagas
from apps_plagas.tipo_plaga.models import TipoPlaga


class RegistroPlaga(models.Model):
    registro_id = models.AutoField(primary_key=True)
    ficha = models.ForeignKey(FichaTecnica, on_delete=models.CASCADE)
    manejo = models.ForeignKey(
        ManejoPlagas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    fecha_registro = models.DateField()
    conteo_larvas = models.IntegerField(default=0)
    conteo_esqueletos = models.IntegerField(default=0)
    conteo_incisiones = models.IntegerField(default=0)
    conteo_tapones = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name="Conteo de tapones",
        help_text="Orificios sellados por el insecto (indicador de actividad pasada)"
    )
    tipologia_plaga = models.ForeignKey(
        TipoPlaga,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Tipo de plaga"
    )
    observaciones = models.TextField(blank=True)

    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_plaga_creados',
        verbose_name='Usuario que registró'
    )

    class Meta:
        app_label = 'registro_plaga'
        verbose_name = "Registro de Plaga"
        verbose_name_plural = "Registros de Plagas"

    def __str__(self):
        return f"Registro {self.registro_id} – {self.ficha}"
