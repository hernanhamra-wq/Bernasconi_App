from django.db import models
from django.contrib.auth import get_user_model
from apps.ficha_tecnica.models import FichaTecnica   # Ajustar según tu app real
from apps_plagas.tipo_plaga.models import TipoPlaga          # La tabla tipo_plaga que ya hicimos

User = get_user_model()

class ManejoPlagas(models.Model):
    ficha = models.ForeignKey(
        FichaTecnica,
        on_delete=models.CASCADE,
        related_name="planes_manejo",
        verbose_name="Obra afectada"
    )
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="planes_manejo_plagas",
        verbose_name="Responsable del plan"
    )
    tipo_plaga = models.ForeignKey(
        TipoPlaga,
        on_delete=models.SET_NULL,
        null=True,
        related_name="planes_asociados",
        verbose_name="Tipo de plaga"
    )
    titulo = models.CharField(
        max_length=255,
        verbose_name="Título del plan MIT"
    )
    propuesta_detalle = models.TextField(
        verbose_name="Descripción del plan y tratamiento"
    )

    class Meta:
        verbose_name = "Plan de manejo de plagas (MIT)"
        verbose_name_plural = "Planes de manejo de plagas (MIT)"
        ordering = ["ficha", "tipo_plaga"]

    def __str__(self):
        return f"{self.titulo} – {self.ficha}"
