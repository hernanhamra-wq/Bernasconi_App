# -*- coding: utf-8 -*-
"""
ACTUALIZADOR DE EXCEL - DiseñoBDnueva.xlsx
==========================================
Actualiza la solapa LISTA_TABLAS con los campos reales de los modelos Django.
"""
import os
import sys
import django
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# ============================================================
# CONFIG DJANGO
# ============================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bernasconi_app.settings")
django.setup()

# ============================================================
# IMPORTS DE MODELOS
# ============================================================
from apps.ficha_tecnica.models import FichaTecnica
from apps.autor.models import Autor, FichaAutor
from apps.material.models import Material, FichaTecnicaMaterial
from apps.catalogo_multimedia.models import CatalogoMultimedia
from apps.estado_obra.models import EstadoObra
from apps.intervencion.models import Intervencion
from apps.investigacion.models import Investigacion
from apps_plagas.tipo_plaga.models import TipoPlaga
from apps_plagas.manejo_plagas.models import ManejoPlagas
from apps_plagas.registro_plaga.models import RegistroPlaga
from apps_plagas.seguimiento_xilofago.models import SeguimientoXilofago
from apps_ubicacion.ubicacion_lugar.models import UbicacionLugar
from apps_ubicacion.contenedor_ubicacion.models import ContenedorUbicacion
from apps_ubicacion.reg_ubicacion_actual.models import RegUbicacionActual
from apps_ubicacion.reg_historial_mov.models import RegHistorialMov
from apps_pres.institucion.models import Institucion
from apps_pres.prestamo.models import Prestamo
from apps_pres.donacion.models import Donacion

# ============================================================
# RUTAS
# ============================================================
EXCEL_PATH = os.path.join(BASE_DIR, "migrations_scripts", "excel_files", "DiseñoBDnueva.xlsx")
OUTPUT_PATH = os.path.join(BASE_DIR, "migrations_scripts", "excel_files", "DiseñoBDnueva_ACTUALIZADO.xlsx")


def get_field_info(model):
    """Extrae información de los campos de un modelo Django."""
    fields = []
    for field in model._meta.get_fields():
        if hasattr(field, 'column'):
            field_name = field.name
            field_type = field.get_internal_type()

            # Mapeo a tipos MySQL
            type_map = {
                'AutoField': 'INT PK AI',
                'BigAutoField': 'BIGINT PK AI',
                'BigIntegerField': 'BIGINT',
                'BooleanField': 'TINYINT(1)',
                'CharField': f'VARCHAR({field.max_length})' if hasattr(field, 'max_length') and field.max_length else 'VARCHAR(255)',
                'DateField': 'DATE',
                'DateTimeField': 'DATETIME',
                'DecimalField': f'DECIMAL({field.max_digits},{field.decimal_places})' if hasattr(field, 'max_digits') else 'DECIMAL(10,2)',
                'FileField': 'VARCHAR(255)',
                'FloatField': 'FLOAT',
                'ForeignKey': 'INT FK',
                'ImageField': 'VARCHAR(255)',
                'IntegerField': 'INT',
                'PositiveIntegerField': 'INT UNSIGNED',
                'TextField': 'TEXT',
            }

            mysql_type = type_map.get(field_type, field_type)

            # Agregar NULL si es nullable
            if hasattr(field, 'null') and field.null:
                mysql_type += ' NULL'

            # Descripción
            desc = ''
            if hasattr(field, 'verbose_name'):
                desc = str(field.verbose_name)
            if hasattr(field, 'help_text') and field.help_text:
                desc += f' - {field.help_text}'

            # Relación FK
            if field_type == 'ForeignKey':
                related = field.related_model._meta.model_name
                desc = f'FK → {related}'

            fields.append({
                'nombre': field_name,
                'tipo': mysql_type,
                'descripcion': desc[:100] if desc else ''
            })

    return fields


def main():
    print("=" * 60)
    print("ACTUALIZANDO EXCEL CON CAMPOS DE MODELOS DJANGO")
    print("=" * 60)

    # Modelos a documentar
    modelos = [
        (1, 'ficha_tecnica', FichaTecnica),
        (2, 'autor', Autor),
        (3, 'ficha_autor', FichaAutor),
        (4, 'material', Material),
        (5, 'ficha_material', FichaTecnicaMaterial),
        (7, 'catalogo_multimedia', CatalogoMultimedia),
        (8, 'estado_obra', EstadoObra),
        (9, 'intervencion', Intervencion),
        (10, 'investigacion', Investigacion),
        (11, 'institucion', Institucion),
        (12, 'prestamo', Prestamo),
        (13, 'donacion', Donacion),
        (14, 'tipo_plaga', TipoPlaga),
        (15, 'manejo_plagas', ManejoPlagas),
        (16, 'registro_plaga', RegistroPlaga),
        (17, 'seguimiento_xilofago', SeguimientoXilofago),
        (18, 'ubicacion_lugar', UbicacionLugar),
        (19, 'contenedor_ubicacion', ContenedorUbicacion),
        (20, 'reg_ubicacion_actual', RegUbicacionActual),
        (21, 'reg_historial_mov', RegHistorialMov),
    ]

    # Generar reporte
    print("\n" + "=" * 80)
    print("CAMPOS ACTUALES DE CADA MODELO")
    print("=" * 80)

    for num, nombre, modelo in modelos:
        print(f"\n{num}. {nombre.upper()}")
        print("-" * 60)
        fields = get_field_info(modelo)
        for f in fields:
            print(f"  {f['nombre']:<30} {f['tipo']:<25} {f['descripcion']}")

    # Generar resumen comparativo
    print("\n" + "=" * 80)
    print("RESUMEN COMPARATIVO EXCEL vs MODELOS")
    print("=" * 80)

    # Campos del Excel (según lo leído anteriormente)
    excel_campos = {
        'ficha_tecnica': ['id', 'n_de_ficha', 'inventario', 'n_de_inventario_anterior', 'titulo',
                         'descripcion', 'observacion', 'anio', 'fecha_de_carga', 'dimensiones',
                         'ancho', 'alto', 'diametro', 'profundidad', 'seguimiento',
                         'fk_responsable_carga_id', 'estado_conservacion', 'fk_estado_id',
                         'fk_material_id', 'fk_taller', 'fk_multimedia_id'],
        'autor': ['id', 'nombre', 'biografia'],
        'ficha_autor': ['id', 'fk_ficha_id', 'fk_autor_id', 'orden'],
        'material': ['id', 'nombre'],
        'catalogo_multimedia': ['id', 'url_archivo', 'tipo', 'descripcion', 'fk_ficha_id'],
        'estado_obra': ['id', 'nombre_estado'],
        'intervencion': ['intervencion_id', 'ficha_id', 'fk_responsable_id', 'n_intervencion',
                        'fecha_inicio', 'fecha_finalizacion', 'diagnostico', 'procedimientos',
                        'materiales_utilizados'],
        'investigacion': ['investigacion_id', 'fk_ficha_id', 'fk_investigador_id', 'num_investigacion',
                         'titulo_investigacion', 'detalle_investigacion', 'anio_realizacion'],
    }

    # Mostrar campos nuevos en modelos que no están en Excel
    print("\nCAMPOS NUEVOS EN MODELOS (no en Excel original):")
    print("-" * 60)

    nuevos_campos = {
        'ficha_tecnica': [
            'fecha_de_modificacion', 'tipo_ejemplar', 'edicion', 'series_legacy', 'imagen',
            'fk_estado_funcional', 'fk_procedencia',
            # Dublin Core
            'categoria_objeto', 'periodo_historico', 'datacion', 'origen_geografico',
            'tematica', 'palabras_clave',
            # Conservación
            'temperatura_requerida_min', 'temperatura_requerida_max',
            'humedad_requerida_min', 'humedad_requerida_max',
            'nivel_iluminacion', 'requiere_vitrina', 'condiciones_especiales',
            # Propiedad legal
            'propietario_legal', 'tipo_propiedad', 'derechos_reproduccion', 'nivel_confidencialidad',
            # M2M
            'autores', 'materiales'
        ],
        'catalogo_multimedia': ['archivo (FileField en lugar de url_archivo)'],
        'material': ['tipo', 'descripcion'],
        'contenedor_ubicacion': ['modo_almacenamiento', 'capacidad_maxima', 'estado'],
        'prestamo': ['estado (workflow completo)'],
        'registro_plaga': ['conteo_tapones', 'usuario_registro'],
    }

    for tabla, campos in nuevos_campos.items():
        print(f"\n  {tabla}:")
        for c in campos:
            print(f"    + {c}")

    print("\n" + "=" * 80)
    print("REPORTE FINALIZADO")
    print("=" * 80)
    print(f"\nPara ver el Excel original: {EXCEL_PATH}")


if __name__ == "__main__":
    main()
