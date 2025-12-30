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

    # ============================================================
    # DUBLIN CORE - Campos para interoperabilidad museística
    # ============================================================
    CATEGORIA_OBJETO_CHOICES = [
        ('PINTURA', 'Pintura'),
        ('ESCULTURA', 'Escultura'),
        ('GRABADO', 'Grabado'),
        ('DIBUJO', 'Dibujo'),
        ('FOTOGRAFIA', 'Fotografía'),
        ('CERAMICA', 'Cerámica'),
        ('TEXTIL', 'Textil'),
        ('MOBILIARIO', 'Mobiliario'),
        ('DOCUMENTO', 'Documento'),
        ('NUMISMATICA', 'Numismática'),
        ('ARQUEOLOGIA', 'Arqueología'),
        ('ETNOGRAFIA', 'Etnografía'),
        ('CIENCIAS_NATURALES', 'Ciencias naturales'),
        ('INSTRUMENTO', 'Instrumento'),
        ('INDUMENTARIA', 'Indumentaria'),
        ('OTRO', 'Otro'),
    ]

    categoria_objeto = models.CharField(
        max_length=50,
        choices=CATEGORIA_OBJETO_CHOICES,
        null=True,
        blank=True,
        verbose_name="Categoría del objeto",
        help_text="Dublin Core: dc.type"
    )

    periodo_historico = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Período histórico",
        help_text="Ej: Colonial, Siglo XIX, Art Nouveau"
    )

    datacion = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Datación",
        help_text="Dublin Core: dc.date. Ej: ca. 1850, 1920-1930"
    )

    origen_geografico = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Origen geográfico",
        help_text="Dublin Core: dc.coverage. País/región de creación"
    )

    tematica = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Temática",
        help_text="Dublin Core: dc.subject. Tema principal de la obra"
    )

    palabras_clave = models.TextField(
        null=True,
        blank=True,
        verbose_name="Palabras clave",
        help_text="Separadas por coma. Facilita búsquedas"
    )

    # ============================================================
    # CONSERVACIÓN - Condiciones ambientales requeridas
    # ============================================================
    NIVEL_ILUMINACION_CHOICES = [
        ('BAJA', 'Baja (< 50 lux)'),
        ('MEDIA', 'Media (50-150 lux)'),
        ('ALTA', 'Alta (150-300 lux)'),
        ('SIN_RESTRICCION', 'Sin restricción'),
    ]

    temperatura_requerida_min = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="Temperatura mínima (°C)"
    )

    temperatura_requerida_max = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="Temperatura máxima (°C)"
    )

    humedad_requerida_min = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="Humedad relativa mínima (%)"
    )

    humedad_requerida_max = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="Humedad relativa máxima (%)"
    )

    nivel_iluminacion = models.CharField(
        max_length=20,
        choices=NIVEL_ILUMINACION_CHOICES,
        null=True,
        blank=True,
        verbose_name="Nivel de iluminación permitido"
    )

    requiere_vitrina = models.BooleanField(
        default=False,
        verbose_name="Requiere exhibición en vitrina"
    )

    condiciones_especiales = models.TextField(
        null=True,
        blank=True,
        verbose_name="Condiciones especiales de conservación",
        help_text="Requisitos adicionales de manejo o almacenamiento"
    )

    # ============================================================
    # PROPIEDAD LEGAL
    # ============================================================
    TIPO_PROPIEDAD_CHOICES = [
        ('PROPIEDAD_MUSEO', 'Propiedad del museo'),
        ('COMODATO', 'Comodato'),
        ('DEPOSITO', 'Depósito'),
        ('PRESTAMO_LARGO', 'Préstamo a largo plazo'),
        ('EN_TRAMITE', 'En trámite'),
        ('OTRO', 'Otro'),
    ]

    NIVEL_CONFIDENCIALIDAD_CHOICES = [
        ('PUBLICO', 'Público'),
        ('RESTRINGIDO', 'Restringido'),
        ('CONFIDENCIAL', 'Confidencial'),
    ]

    propietario_legal = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Propietario legal",
        help_text="Dublin Core: dc.rights"
    )

    tipo_propiedad = models.CharField(
        max_length=50,
        choices=TIPO_PROPIEDAD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Tipo de propiedad"
    )

    derechos_reproduccion = models.TextField(
        null=True,
        blank=True,
        verbose_name="Derechos de reproducción",
        help_text="Restricciones para fotografía, publicación, etc."
    )

    nivel_confidencialidad = models.CharField(
        max_length=20,
        choices=NIVEL_CONFIDENCIALIDAD_CHOICES,
        default='PUBLICO',
        verbose_name="Nivel de confidencialidad"
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

    # ============================================================
    # MÉTODOS DE UBICACIÓN
    # ============================================================
    def ubicacion_actual(self):
        """
        Retorna la ubicación actual de la obra basándose en el último
        movimiento COMPLETADO registrado en el historial.

        Returns:
            dict con lugar, contenedor y fecha, o None si no hay historial
        """
        ultimo_movimiento = self.historial_movimientos.filter(
            estado='COMPLETADO'
        ).order_by('-fecha_movimiento').first()

        if ultimo_movimiento:
            return {
                'lugar': ultimo_movimiento.fk_lugar_destino,
                'contenedor': ultimo_movimiento.fk_contenedor_destino,
                'fecha': ultimo_movimiento.fecha_movimiento,
                'motivo': ultimo_movimiento.motivo,
            }
        return None

    def en_cuarentena(self):
        """
        Verifica si la obra está actualmente en cuarentena.

        Returns:
            bool: True si el último movimiento completado fue a cuarentena
        """
        ubicacion = self.ubicacion_actual()
        if ubicacion and ubicacion['lugar']:
            return ubicacion['lugar'].tipo_lugar == 'CUARENTENA'
        return False
