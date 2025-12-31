# -*- coding: utf-8 -*-
"""
ORQUESTADOR DE MIGRACIONES
==========================
Ejecuta todos los scripts de migración en orden.
Cada script es idempotente (puede re-ejecutarse sin duplicar datos).

Uso:
    python run_all.py

Orden de ejecución:
    00. Usuarios (seed)
    01. Materiales (normalización desde CSV)
    02. Autores (normalización desde CSV)
    03. Tipos de plaga (seed)
    04. Ubicaciones (desde CSV)
    05. Fichas técnicas (desde CSV)
    06. Ficha-Autor M2M
    07. Ficha-Material M2M
    08. Ubicación inicial [pendiente - requiere historial]
    09. Xilófagos (RegistroPlaga)
    10. Investigaciones
"""

import _00_usuarios
import _01_materiales
import _02_autores
import _03_tipos_plaga
import _04_ubicaciones
import _05_fichas
import _06_ficha_autor
import _07_ficha_material
# import _08_ubicacion_inicial  # pendiente
import _09_xilofagos
import _10_investigaciones


def main():
    print("=" * 60)
    print("🚀 INICIO MIGRACIÓN COMPLETA - BernasconiApp")
    print("=" * 60)

    # FASE 1: Seeds (sin dependencias)
    print("\n" + "─" * 60)
    print("FASE 1: SEEDS")
    print("─" * 60)

    _00_usuarios.run()
    _03_tipos_plaga.run()

    # FASE 2: Catálogos (normalizados desde CSV)
    print("\n" + "─" * 60)
    print("FASE 2: CATÁLOGOS")
    print("─" * 60)

    _01_materiales.run()
    _02_autores.run()

    # FASE 3: Ubicaciones
    print("\n" + "─" * 60)
    print("FASE 3: UBICACIONES")
    print("─" * 60)
    _04_ubicaciones.run()

    # FASE 4: Fichas técnicas
    print("\n" + "─" * 60)
    print("FASE 4: FICHAS TÉCNICAS")
    print("─" * 60)
    _05_fichas.run()

    # FASE 5: Relaciones M2M
    print("\n" + "─" * 60)
    print("FASE 5: RELACIONES M2M")
    print("─" * 60)
    _06_ficha_autor.run()
    _07_ficha_material.run()

    # FASE 6: Datos secundarios
    print("\n" + "─" * 60)
    print("FASE 6: DATOS SECUNDARIOS")
    print("─" * 60)
    # _08_ubicacion_inicial.run()  # pendiente
    _09_xilofagos.run()
    _10_investigaciones.run()

    print("\n" + "=" * 60)
    print("✅ MIGRACIÓN COMPLETA FINALIZADA")
    print("=" * 60)


if __name__ == "__main__":
    main()
