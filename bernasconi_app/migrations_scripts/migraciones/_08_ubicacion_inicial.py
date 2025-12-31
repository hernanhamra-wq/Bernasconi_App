# -*- coding: utf-8 -*-
"""
MIGRACIÓN: Ubicación Inicial de Obras
=====================================
Migra la ubicación inicial de cada obra desde el CSV.
Crea registros en reg_ubicacion_actual basándose en los campos:
- sector: Código de sector (ej: 23H, 34N)
- sala: Nombre de sala (ej: sala6, Naturales)
- ubicación: Ubicación descriptiva
- caja: Número de caja/contenedor

Estrategia de mapeo:
1. Primero intenta mapear por 'sector' → UbicacionLugar
2. Si no, intenta por 'sala' → UbicacionLugar
3. Si no, intenta por 'ubicación' → UbicacionLugar
4. Si encuentra caja, busca en ContenedorUbicacion

Idempotente: no duplica registros existentes.
"""
import os
import sys
import csv
import django
from datetime import datetime

# ============================================================
# CONFIG DJANGO
# ============================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bernasconi_app.settings")
django.setup()

from django.contrib.auth import get_user_model
from apps.ficha_tecnica.models import FichaTecnica
from apps.estado_obra.models import EstadoObra
from apps_ubicacion.ubicacion_lugar.models import UbicacionLugar
from apps_ubicacion.contenedor_ubicacion.models import ContenedorUbicacion
from apps_ubicacion.reg_ubicacion_actual.models import RegUbicacionActual

User = get_user_model()

# ============================================================
# RUTAS
# ============================================================
CSV_PATH = os.path.join(BASE_DIR, "migrations_scripts", "csv_files", "ficha técnica.csv")

# ============================================================
# HELPERS
# ============================================================

def normalizar(texto):
    """Normaliza texto para comparación."""
    if not texto:
        return ""
    return texto.lower().strip().replace("  ", " ")


def extraer_numero_caja(texto):
    """Extrae número de caja de un texto."""
    import re
    if not texto:
        return None

    # Buscar patrones como "caja 123", "CAJA 456", "caja123"
    match = re.search(r'caja\s*(\d+)', texto.lower())
    if match:
        return int(match.group(1))

    # Si es solo un número
    try:
        return int(float(texto))
    except (ValueError, TypeError):
        return None


def cargar_lugares():
    """Carga lugares en diccionario para búsqueda rápida."""
    lugares = {}
    for lugar in UbicacionLugar.objects.all():
        nombre_norm = normalizar(lugar.nombre_lugar)
        lugares[nombre_norm] = lugar

        # Variantes sin 'sector '
        if nombre_norm.startswith('sector '):
            lugares[nombre_norm[7:]] = lugar

        # Variantes sin 'sala '
        if nombre_norm.startswith('sala '):
            lugares[nombre_norm[5:]] = lugar

    return lugares


def cargar_contenedores():
    """Carga contenedores en diccionario para búsqueda rápida."""
    contenedores = {}
    for cont in ContenedorUbicacion.objects.all():
        nombre_norm = normalizar(cont.nombre_contenedor)
        contenedores[nombre_norm] = cont

        # Por número si es "Caja X"
        if nombre_norm.startswith('caja '):
            try:
                num = int(nombre_norm[5:])
                contenedores[f"caja_{num}"] = cont
            except ValueError:
                pass

    return contenedores


def buscar_lugar(sector, sala, ubicacion, lugares_dict):
    """Busca el lugar más apropiado para una ficha."""
    # 1. Por sector (más específico)
    if sector:
        sector_norm = normalizar(sector)
        lugar = lugares_dict.get(f"sector {sector_norm}") or lugares_dict.get(sector_norm)
        if lugar:
            return lugar

    # 2. Por sala
    if sala:
        sala_norm = normalizar(sala)
        # Limpiar "sala" del inicio si está
        if sala_norm.startswith('sala'):
            sala_norm = sala_norm[4:].strip()

        lugar = lugares_dict.get(f"sala {sala_norm}") or lugares_dict.get(sala_norm)
        if lugar:
            return lugar

        # Mapeos especiales de sala
        mapeo_salas = {
            'sala6': 'sala 6',
            'sala8': 'sala 8',
            'sala7': 'sala 7',
            'sala5': 'sala 5',
            'sala4': 'sala 4',
            'sala2': 'sala 2',
            'naturales': 'sala ciencias naturales',
            'cincioni': 'sala cincioni',
        }
        if sala_norm in mapeo_salas:
            lugar = lugares_dict.get(mapeo_salas[sala_norm])
            if lugar:
                return lugar

    # 3. Por ubicación directa
    if ubicacion:
        ubi_norm = normalizar(ubicacion)
        lugar = lugares_dict.get(ubi_norm)
        if lugar:
            return lugar

        # Extraer sector de ubicación (ej: "sector 30A" → "30a")
        if 'sector' in ubi_norm:
            import re
            match = re.search(r'sector\s*(\w+)', ubi_norm)
            if match:
                sector_extraido = match.group(1)
                lugar = lugares_dict.get(f"sector {sector_extraido}") or lugares_dict.get(sector_extraido)
                if lugar:
                    return lugar

    return None


def buscar_contenedor(caja, ubicacion, contenedores_dict, lugar):
    """Busca el contenedor más apropiado."""
    # 1. Por número de caja
    num_caja = extraer_numero_caja(caja)
    if num_caja:
        cont = contenedores_dict.get(f"caja_{num_caja}")
        if cont:
            return cont

    # 2. Extraer caja de ubicación
    if ubicacion:
        num_caja = extraer_numero_caja(ubicacion)
        if num_caja:
            cont = contenedores_dict.get(f"caja_{num_caja}")
            if cont:
                return cont

    return None


# ============================================================
# MAIN
# ============================================================

def run():
    print("▶ Iniciando Migración de Ubicación Inicial")

    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encuentra el CSV en {CSV_PATH}")
        return

    # Pre-cargar datos
    lugares_dict = cargar_lugares()
    contenedores_dict = cargar_contenedores()
    fichas_por_inventario = {f.inventario: f for f in FichaTecnica.objects.all() if f.inventario}

    # Estado por defecto: Depósito
    estado_deposito = EstadoObra.objects.filter(nombre_estado__icontains='dep').first()
    if not estado_deposito:
        estado_deposito = EstadoObra.objects.first()

    # Usuario legacy
    usuario_legacy = User.objects.filter(username='sistema_legacy').first()

    # Ubicaciones existentes
    ubicaciones_existentes = set(
        RegUbicacionActual.objects.values_list('fk_ficha_id', flat=True)
    )

    print(f"  📋 {len(fichas_por_inventario)} fichas cargadas")
    print(f"  📍 {len(lugares_dict)} lugares disponibles")
    print(f"  📦 {len(contenedores_dict)} contenedores disponibles")
    print(f"  ⏭ {len(ubicaciones_existentes)} ubicaciones ya registradas")

    creados = 0
    ya_existentes = 0
    sin_lugar = 0
    sin_ficha = 0
    errores = 0

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for i, fila in enumerate(reader, start=1):
            try:
                # Obtener inventario
                inventario = (fila.get('inventario') or '').strip()
                if not inventario:
                    continue

                # Buscar ficha
                ficha = fichas_por_inventario.get(inventario)
                if not ficha:
                    sin_ficha += 1
                    continue

                # Verificar si ya existe ubicación
                if ficha.id in ubicaciones_existentes:
                    ya_existentes += 1
                    continue

                # Obtener datos de ubicación
                sector = fila.get('sector', '')
                sala = fila.get('sala', '')
                ubicacion = fila.get('ubicación', '')
                caja = fila.get('caja', '')

                # Buscar lugar
                lugar = buscar_lugar(sector, sala, ubicacion, lugares_dict)
                if not lugar:
                    sin_lugar += 1
                    continue

                # Buscar contenedor (opcional)
                contenedor = buscar_contenedor(caja, ubicacion, contenedores_dict, lugar)

                # Crear registro de ubicación
                RegUbicacionActual.objects.create(
                    fk_ficha=ficha,
                    fk_estado=estado_deposito,
                    fk_lugar=lugar,
                    fk_contenedor=contenedor,
                    fecha_desde=datetime.now(),
                    usuario_registro=usuario_legacy
                )

                ubicaciones_existentes.add(ficha.id)
                creados += 1

                if creados <= 5:
                    cont_str = f" → {contenedor.nombre_contenedor}" if contenedor else ""
                    print(f"  ✓ Inv. {inventario}: {lugar.nombre_lugar}{cont_str}")

                if creados % 1000 == 0:
                    print(f"  ... {creados} ubicaciones creadas")

            except Exception as e:
                errores += 1
                if errores <= 5:
                    print(f"  ⚠ Error en fila {i}: {e}")

    print(f"\n✔ Proceso finalizado.")
    print(f"  🆕 Ubicaciones creadas: {creados}")
    print(f"  ⏭ Ya existentes: {ya_existentes}")
    print(f"  ❓ Sin lugar mapeado: {sin_lugar}")
    print(f"  ❓ Fichas no encontradas: {sin_ficha}")
    print(f"  ❌ Errores: {errores}")
    print(f"  📊 Total en BD: {RegUbicacionActual.objects.count()}")


if __name__ == "__main__":
    run()
