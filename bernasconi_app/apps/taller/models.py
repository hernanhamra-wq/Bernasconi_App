from django.db import models

class Taller(models.Model):
    nombre = models.CharField(max_length=255, unique=True, verbose_name="Nombre del taller")
    descripcion = models.TextField(null=True, blank=True)
    ubicacion = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Taller"
        verbose_name_plural = "Talleres"

    def __str__(self):
        return self.nombre