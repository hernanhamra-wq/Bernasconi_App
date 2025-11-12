from django.db import models

# ===================================================================
# 1. MODELO AUTOR
# ===================================================================
class Autor(models.Model):
    """Modelo para representar a un Autor, coautor o colaborador."""
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    
    biografia = models.TextField(
        null=True, 
        blank=True,
        verbose_name="Biografía / Descripción"
    )
    
    fecha_nacimiento = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha de Nacimiento"
    )
    nacionalidad = models.CharField(
        max_length=50, 
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        db_table = 'catalogo_autores'
        unique_together = ('nombre', 'apellido')
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

# ===================================================================
# 2. MODELO INTERMEDIO: COLABORACION (Tabla: colaboraciones)
# Esto define la tabla de enlace para la relación Muchos a Muchos.
# ===================================================================
class Colaboracion(models.Model):
    """Tabla de enlace para la relación Muchos a Muchos entre Obra y Autor."""
    
    obra = models.ForeignKey('Obra', on_delete=models.CASCADE)
    autor = models.ForeignKey('Autor', on_delete=models.CASCADE)
    
    # Campo opcional para especificar el rol (Autor, Coautor, Ilustrador, etc.)
    rol = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = 'colaboraciones' 
        unique_together = ('obra', 'autor') 
        verbose_name = "Colaboración"
        verbose_name_plural = "Colaboraciones"
        
    def __str__(self):
        return f'{self.autor.apellido} en {self.obra.titulo}'

# ===================================================================
# 3. MODELO OBRA (Catálogo Maestro) (Tabla: catalogo_obras)
# ===================================================================
class Obra(models.Model):
    """Modelo principal que representa una Obra en el catálogo."""
    
    titulo = models.CharField(max_length=200)
    
    # RELACIÓN: Muchos a Muchos. Usa la tabla 'Colaboracion'.
    autores = models.ManyToManyField(
        'Autor', 
        through='Colaboracion',
        related_name='obras_participadas', 
        verbose_name="Autores y Colaboradores"
    )
    
    TIPO_CHOICES = (
        ('L', 'Libro'),
        ('A', 'Artículo'),
        ('E', 'Ensayo'),
        ('O', 'Otro'),
    )
    tipo_obra = models.CharField(
        max_length=1, 
        choices=TIPO_CHOICES, 
        default='L',
        verbose_name="Tipo de Obra"
    )
    
    fecha_publicacion = models.IntegerField(
        null=True, 
        blank=True,
        verbose_name="Año de Publicación"
    )
    
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Obra"
        verbose_name_plural = "Obras"
        # Renombra la tabla principal a 'catalogo_obras'
        db_table = 'catalogo_obras'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo


# ===================================================================
# 4. MODELO PRESTAMO (Tabla: prestamos)
# ===================================================================
class Prestamo(models.Model):
    """Modelo para registrar el préstamo de una Obra del catálogo."""
    
    # RELACIÓN: Clave Foránea a Obra (Uno a Muchos)
    obra = models.ForeignKey(
        'Obra', 
        on_delete=models.CASCADE, 
        related_name='historial_prestamos',
        verbose_name="Obra Prestada"
    )
    
    solicitante = models.CharField(max_length=200, verbose_name="Solicitante")
    
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion_estimada = models.DateField()
    devuelto = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        db_table = 'prestamos' # Nombre de tabla limpio
        
    def __str__(self):
        return f'Préstamo de {self.obra.titulo} a {self.solicitante}'