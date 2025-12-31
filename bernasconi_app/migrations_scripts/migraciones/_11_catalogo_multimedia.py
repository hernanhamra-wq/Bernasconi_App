# -*- coding: utf-8 -*-
"""
MIGRACIÓN: Catálogo Multimedia
==============================
Migra los links de fotografías desde el CSV de fichas técnicas.
Los datos provienen de las columnas 'fotografia' y 'link-fotografias'.

Idempotente: no duplica registros existentes (basado en ficha + url).

Origen de datos:
- Campo 'fotografia': indica si hay foto (1 = sí)
- Campo 'link-fotografias': URL de Google Drive con las imágenes
"""
import os
import sys
import csv
import django

# ============================================================
# CONFIG DJANGO
# ============================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bernasconi_app.settings")
django.setup()

from apps.ficha_tecnica.models import FichaTecnica
from apps.catalogo_multimedia.models import CatalogoMultimedia

# ============================================================
# RUTAS
# ============================================================
CSV_PATH = os.path.join(BASE_DIR, "migrations_scripts", "csv_files", "ficha técnica.csv")

# ============================================================
# HELPERS
# ============================================================

def limpiar_texto(valor):
    """Limpia un valor de texto."""
    if not valor:
        return None

    texto = str(valor).strip()
    texto = texto.replace('\ufeff', '')

    if texto.lower() in ['', 'nan', 'none', 'null']:
        return None

    return texto


def limpiar_inventario(valor):
    """Limpia el número de inventario para búsqueda."""
    if not valor:
        return None

    valor = str(valor).strip()
    valor = valor.replace('\ufeff', '').strip()

    if not valor:
        return None

    return valor


def determinar_tipo_archivo(url):
    """Determina el tipo de archivo basado en la URL."""
    if not url:
        return "imagen"  # Default

    url_lower = url.lower()

    # Google Drive folders suelen contener imágenes
    if 'drive.google.com' in url_lower:
        return "imagen"

    # Extensiones comunes
    if any(ext in url_lower for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']):
        return "imagen"
    elif any(ext in url_lower for ext in ['.mp4', '.avi', '.mov', '.wmv', '.webm']):
        return "video"
    elif any(ext in url_lower for ext in ['.mp3', '.wav', '.ogg', '.flac']):
        return "audio"
    elif any(ext in url_lower for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']):
        return "documento"

    return "imagen"  # Default para links de Drive


# ============================================================
# MAIN
# ============================================================

def run():
    print("▶ Iniciando Migración de Catálogo Multimedia")

    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encuentra el CSV en {CSV_PATH}")
        return

    # Pre-cargar fichas existentes por inventario
    fichas_por_inventario = {f.inventario: f for f in FichaTecnica.objects.all() if f.inventario}
    print(f"  📋 {len(fichas_por_inventario)} fichas cargadas")

    # Pre-cargar multimedia existente para evitar duplicados
    multimedia_existente = set()
    for m in CatalogoMultimedia.objects.all():
        if m.archivo:
            # archivo puede ser FileField con URL o nombre
            key = (m.ficha_id, str(m.archivo))
            multimedia_existente.add(key)

    print(f"  📷 {len(multimedia_existente)} registros multimedia existentes")

    creados = 0
    ya_existentes = 0
    fichas_no_encontradas = 0
    sin_link = 0
    errores = 0

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for i, fila in enumerate(reader, start=1):
            try:
                # Obtener inventario
                inventario = limpiar_inventario(fila.get('inventario'))
                if not inventario:
                    continue

                # Buscar ficha
                ficha = fichas_por_inventario.get(inventario)
                if not ficha:
                    fichas_no_encontradas += 1
                    continue

                # Obtener link de fotografías
                link_foto = limpiar_texto(fila.get('link-fotografias'))

                if not link_foto:
                    sin_link += 1
                    continue

                # Verificar si ya existe
                key = (ficha.id, link_foto)
                if key in multimedia_existente:
                    ya_existentes += 1
                    continue

                # Determinar tipo
                tipo = determinar_tipo_archivo(link_foto)

                # Crear descripción
                titulo_ficha = ficha.titulo[:50] if ficha.titulo else f"Inv. {inventario}"
                descripcion = f"Fotografía de {titulo_ficha} (migrado desde legacy)"

                # Crear registro
                # Nota: 'archivo' es FileField pero guardamos la URL como referencia
                # En producción se debería descargar y subir el archivo
                multimedia = CatalogoMultimedia(
                    ficha=ficha,
                    tipo=tipo,
                    descripcion=descripcion[:255],
                )

                # Guardamos la URL en el campo archivo temporalmente
                # El FileField aceptará la URL como string
                # Idealmente se debería migrar los archivos físicos
                multimedia.archivo.name = link_foto[:255]
                multimedia.save()

                multimedia_existente.add(key)
                creados += 1

                if creados <= 5:
                    print(f"  ✓ Creado para Inv. {inventario}: {link_foto[:50]}...")

            except Exception as e:
                errores += 1
                if errores <= 5:
                    print(f"  ⚠ Error en fila {i}: {e}")

    print(f"\n✔ Proceso finalizado.")
    print(f"  🆕 Registros multimedia creados: {creados}")
    print(f"  ⏭ Ya existentes (saltados): {ya_existentes}")
    print(f"  📭 Sin link de foto: {sin_link}")
    print(f"  ❓ Fichas no encontradas: {fichas_no_encontradas}")
    print(f"  ❌ Errores: {errores}")
    print(f"  📊 Total en BD: {CatalogoMultimedia.objects.count()}")


if __name__ == "__main__":
    run()
