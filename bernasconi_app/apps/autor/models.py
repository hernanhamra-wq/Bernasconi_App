from django.db import models

class Autor(models.Model):
    nombre = models.CharField(max_length=255)
    biografia = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'autor'
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return self.nombre


class FichaAutor(models.Model):
    fk_ficha = models.ForeignKey(
        'ficha_tecnica.FichaTecnica',
        on_delete=models.CASCADE,
        db_column='fk_ficha_id'
    )
    fk_autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        db_column='fk_autor_id'
    )

    orden = models.IntegerField(default=1)

    class Meta:
        db_table = 'ficha_autor'
        verbose_name = 'Autor de ficha técnica'
        verbose_name_plural = 'Autores de fichas técnicas'
        unique_together = ('fk_ficha', 'fk_autor')

    def __str__(self):
        return f"{self.fk_autor.nombre} → {self.fk_ficha.titulo if hasattr(self.fk_ficha, 'titulo') else self.fk_ficha.id}"
