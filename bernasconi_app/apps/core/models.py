from django.db import models
from django.conf import settings


class AuditableModel(models.Model):
    """
    Modelo abstracto base para auditoría.
    Todos los modelos que requieran trazabilidad deben heredar de este.

    Los campos se llenan automáticamente mediante el middleware CurrentUserMiddleware.
    El usuario del museo NO necesita cargar estos campos manualmente.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de modificación"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
        verbose_name="Creado por",
        editable=False
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated",
        verbose_name="Modificado por",
        editable=False
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Sobrescribe save() para auto-poblar created_by y updated_by.
        Usa el usuario del contexto actual (middleware).
        """
        from apps.core.middleware import get_current_user
        user = get_current_user()

        if user and user.is_authenticated:
            if not self.pk:  # Nuevo registro
                self.created_by = user
            self.updated_by = user

        super().save(*args, **kwargs)
