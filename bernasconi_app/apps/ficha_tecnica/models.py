from django.db import models
from django.conf import settings
from apps.estado_obra.models import EstadoObra


class FichaTecnica(models.Model):
    # ============================================================
    # IDENTIFICACIÓN / INVENTARIO
    # ============================================================
    n_de_ficha = models.BigIntegerField(null=True, blank=True)
    inventario = models.CharField(
        max_length=255,
        unique=True,  # Garantiza unicidad a nivel de base de datos
        null=True,
        blank=True,
        verbose_name="Número de inventario"
    )
    n_de_inventario_anterior = models.TextField(null=True, blank=True)

    # ============================================================
    # DESCRIPCIÓN GENERAL
    # ============================================================
    titulo = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)

    anio = models.CharField(max_length=10, null=True, blank=True)

    fecha_de_carga = models.DateTimeField(auto_now_add=True)
    fecha_de_modificacion = models.DateTimeField(auto_now=True)

    # ============================================================
    # ESTADO FÍSICO (Valores fijos en columna)
    # ============================================================
    ESTADO_CONSERVACION_CHOICES = [
        ('BUENO', 'Bueno'),
        ('REGULAR', 'Regular'),
        ('MALO', 'Malo'),
    ]
    estado_conservacion = models.CharField(
        max_length=20, 
        choices=ESTADO_CONSERVACION_CHOICES, 
        null=True, 
        blank=True,
        verbose_name="Estado de conservación física"
    )
    # ============================================================
    # EJEMPLAR / SERIE
    # ============================================================
    TIPO_EJEMPLAR_CHOICES = [
        ("original", "Original"),
        ("copia", "Copia"),
        ("serie_1", "Serie 1"),
        ("serie_2", "Serie 2"),
        ("serie_3", "Serie 3"),
        ("serie_4", "Serie 4"),
        ("serie_5", "Serie 5"),
        ("serie_6", "Serie 6"),
    ]

    tipo_ejemplar = models.CharField(
        max_length=20,
        choices=TIPO_EJEMPLAR_CHOICES,
        null=True,
        blank=True
    )

    edicion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Ej: 3/50, edición limitada, prueba de artista"
    )

    # valor original del legacy (NO normalizado)
    series_legacy = models.TextField(null=True, blank=True)

    # ============================================================
    # DIMENSIONES
    # ============================================================
    dimensiones = models.TextField(null=True, blank=True)
    ancho = models.FloatField(null=True, blank=True)
    alto = models.FloatField(null=True, blank=True)
    diametro = models.FloatField(null=True, blank=True)
    profundidad = models.FloatField(null=True, blank=True)

    # ============================================================
    # CONTROL / SEGUIMIENTO
    # ============================================================
    seguimiento = models.BooleanField(default=False)
    
    imagen = models.ImageField(upload_to='fichas/', null=True, blank=True)

    fk_estado_funcional = models.ForeignKey(
        EstadoObra,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas'
    )

    fk_responsable_carga = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas_cargadas'
    )

    # ============================================================
    # RELACIONES
    # ============================================================
    fk_taller = models.ForeignKey(
        'taller.Taller',
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

    fk_procedencia = models.ForeignKey(
        'procedencia.Procedencia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas',
        verbose_name='Procedencia'
    )

    autores = models.ManyToManyField(
        'autor.Autor',
        through='autor.FichaAutor',
        related_name='fichas',
        blank=True
    )

    materiales = models.ManyToManyField(
        'material.Material',
        through='material.FichaTecnicaMaterial',
        related_name='fichas'
    )

    # ============================================================
    # META
    # ============================================================
 
    class Meta:
        verbose_name = "Ficha técnica"
        verbose_name_plural = "Fichas técnicas"

    def __str__(self):
        return f"Ficha {self.id} - {self.titulo}"
