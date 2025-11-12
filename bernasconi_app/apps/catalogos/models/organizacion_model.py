from django.db import models


# ===================================================================
# MODELO ORGANIZACION
# ===================================================================
class Organizacion(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    contacto = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        db_table = 'catalogo_organizaciones'
        verbose_name = "Organización"
        verbose_name_plural = "Organizaciones"

    def __str__(self):
        return self.nombre
