from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Campos extra
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    # Nivel de usuario
    SUPERADMIN = 'superadmin'
    ADMIN = 'admin'
    GUEST = 'guest'

    ROLE_CHOICES = [
        (SUPERADMIN, 'SuperAdmin'),
        (ADMIN, 'Admin'),
        (GUEST, 'Guest'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=GUEST)

    def __str__(self):
        return f"{self.username} ({self.role})"
