from django.db import models

class Institucion(models.Model):
    nombre = models.CharField(max_length=255)
    tipo_institucion = models.CharField(max_length=100)
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
