"""
MIGRACIÓN FICHA TÉCNICA – MATERIALES (ACCESS → DJANGO)
====================================================

DECISIÓN CLAVE
--------------
El campo "materiales" proveniente de la base histórica (Access / Excel)
NO se migra a FichaTecnica.descripcion.

Se migra ÍNTEGRAMENTE a:
    FichaTecnica.observacion

RESUMEN
-------
Materiales (Access) → Sector OBSERVACIONES del modelo FichaTecnica (Django)

ORIGEN
------
En la base histórica del museo, el campo "materiales" fue utilizado como
DESCRIPCIÓN TEXTUAL libre de la composición material de la obra,
no como un catálogo normalizado.

CRITERIO DE MIGRACIÓN
--------------------
- El texto se copia completo
- Sin normalización
- Sin correcciones
- Sin interpretación
- Sin fragmentación

OBJETIVO
--------
- Preservar el registro histórico original
- Mantener trazabilidad con la base anterior
- Evitar decisiones irreversibles en esta etapa
- Separar descripción conceptual de descripción técnica

USO DE CAMPOS
-------------
- FichaTecnica.descripcion:
    Descripción general de la obra (conceptual / artística / histórica)

- FichaTecnica.observacion:
    Observaciones técnicas, incluyendo el texto histórico de materiales

MATERIALES NORMALIZADOS
-----------------------
Los materiales normalizados se gestionan ÚNICAMENTE mediante:
- Modelo Material
- Relación ManyToMany FichaTecnicaMaterial

El texto histórico NO se utiliza para crear materiales normalizados.

NOTA FINAL
----------
La limpieza, corrección o normalización del texto histórico se realizará
en una etapa posterior mediante scripts específicos.
"""
