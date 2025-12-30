from django.db import models


class Taller(models.Model):
    nombre = models.CharField(max_length=255, unique=True, verbose_name="Nombre del taller")
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción")
    ubicacion = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ubicación")

    # Campo contacto separado en campos específicos
    persona_contacto = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Persona de contacto"
    )
    email = models.EmailField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Email"
    )
    telefono = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Teléfono"
    )

    class Meta:
        verbose_name = "Taller"
        verbose_name_plural = "Talleres"

    def __str__(self):
        return self.nombre