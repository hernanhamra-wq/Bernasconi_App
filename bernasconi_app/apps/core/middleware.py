"""
Middleware para capturar el usuario actual en cada request.
Permite que AuditableModel auto-popule created_by y updated_by.
"""
from threading import local

_user = local()


class CurrentUserMiddleware:
    """
    Middleware que guarda el usuario actual en thread-local storage.
    Esto permite acceder al usuario desde cualquier parte del código,
    incluyendo el método save() de los modelos.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Guardar el usuario actual (o None si no está autenticado)
        _user.value = request.user if hasattr(request, 'user') and request.user.is_authenticated else None

        response = self.get_response(request)

        # Limpiar después del request
        _user.value = None

        return response


def get_current_user():
    """
    Retorna el usuario del request actual.
    Usar desde modelos para obtener el usuario que está haciendo la acción.
    """
    return getattr(_user, 'value', None)
