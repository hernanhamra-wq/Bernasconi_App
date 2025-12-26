from django.contrib import admin
from .models import Autor, FichaAutor

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    # Agregamos ID para identificar duplicados y nombre
    list_display = ('id', 'nombre') 
    
    # IMPORTANTE: Estos campos son los que usará el buscador 
    # de la Ficha Técnica. Agrega 'apellido' si existe en tu modelo.
    search_fields = ('nombre',) 

    # Esto ayuda a que el admin cargue más rápido si llegas a tener miles de autores
    show_full_result_count = False

# Opcional: Solo registra FichaAutor si necesitas editar el "orden" 
# de forma manual y masiva. Si no, puedes borrar este bloque.
@admin.register(FichaAutor)
class FichaAutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_ficha', 'fk_autor', 'orden')
    list_filter = ('fk_autor',)
    # autocomplete_fields aquí también ayuda si la lista de fichas es gigante
    autocomplete_fields = ('fk_ficha', 'fk_autor')