from django.db import models
from django.conf import settings   # ✅ seguimos usando AUTH_USER_MODEL
from apps.estado_obra.models import EstadoObra   # ✅ nuevo import para la FK

class FichaTecnica(models.Model):
    n_de_ficha = models.BigIntegerField(null=True, blank=True)
    inventario = models.CharField(max_length=255, null=True, blank=True)
    n_de_inventario_anterior = models.TextField(null=True, blank=True)

    titulo = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)

    anio = models.CharField(max_length=10, null=True, blank=True)
    fecha_de_carga = models.DateTimeField(auto_now_add=True)

    dimensiones = models.TextField(null=True, blank=True)
    ancho = models.FloatField(null=True, blank=True)
    alto = models.FloatField(null=True, blank=True)
    diametro = models.FloatField(null=True, blank=True)
    profundidad = models.FloatField(null=True, blank=True)

    seguimiento = models.BooleanField(default=False)

    # 🔹 cambio: ahora fk_estado es ForeignKey a EstadoObra
    fk_estado = models.ForeignKey(
        EstadoObra,                  # ✅ referencia al catálogo de estados
        on_delete=models.SET_NULL,   # ✅ si se borra el estado, queda NULL
        null=True,
        blank=True,
        related_name='fichas'
    )

    fk_responsable_carga = models.ForeignKey(
        settings.AUTH_USER_MODEL,    # ✅ sigue apuntando al modelo de usuario
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas_cargadas'
    )

    fk_serie = models.ForeignKey(
        'serie.Serie',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    fk_multimedia_principal = models.ForeignKey(
        'catalogo_multimedia.CatalogoMultimedia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    materiales = models.ManyToManyField(
        'material.Material',
        through='material.FichaTecnicaMaterial',
        related_name='fichas'
    )

    def __str__(self):
        return f"Ficha {self.id} - {self.titulo}"
