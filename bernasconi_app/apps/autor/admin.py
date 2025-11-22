from django.contrib import admin
from .models import Autor, FichaAutor


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(FichaAutor)
class FichaAutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_ficha', 'fk_autor', 'orden')
    list_filter = ('fk_autor',)
    search_fields = ('fk_autor__nombre', 'fk_ficha__id')
