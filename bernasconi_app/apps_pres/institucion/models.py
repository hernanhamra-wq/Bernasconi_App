from django.db import models


class Institucion(models.Model):

    TIPO_INSTITUCION_CHOICES = [
        ('MUSEO', 'Museo'),
        ('UNIVERSIDAD', 'Universidad'),
        ('FUNDACION', 'Fundación'),
        ('GALERIA', 'Galería'),
        ('CENTRO_CULTURAL', 'Centro cultural'),
        ('BIBLIOTECA', 'Biblioteca'),
        ('ARCHIVO', 'Archivo'),
        ('GOBIERNO', 'Institución gubernamental'),
        ('PRIVADO', 'Colección privada'),
        ('OTRO', 'Otro'),
    ]

    nombre = models.CharField(max_length=255)
    tipo_institucion = models.CharField(
        max_length=100,
        choices=TIPO_INSTITUCION_CHOICES,
        default='OTRO'
    )
    direccion = models.CharField(max_length=255, blank=True, null=True)
    contacto_persona = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Institución"
        verbose_name_plural = "Instituciones"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
