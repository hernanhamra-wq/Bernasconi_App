import csv
import os


# ============================================================
# RESOLUCIÓN DE RUTAS (FORMA ROBUSTA)
# ============================================================

# __file__ es la ruta del archivo actual (material_inspeccion.py)
# os.path.abspath() la convierte en ruta absoluta
# os.path.dirname() se queda solo con el directorio
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carpeta donde están todos los CSV de migración
# Esta carpeta debe existir dentro del mismo directorio del script
DATA_DIR = os.path.join(BASE_DIR, "csv_files")

# Ruta completa al archivo CSV específico
CSV_PATH = os.path.join(DATA_DIR, "ficha técnica.csv")


# ============================================================
# FUNCIÓN PRINCIPAL DE INSPECCIÓN
# ============================================================

def inspeccionar_madera():
    """
    Lee el archivo 'ficha técnica.csv' y:
    - recorre todas las filas
    - busca en la columna 'materiales'
    - extrae valores que contienen la palabra 'madera'
    - muestra los valores únicos encontrados (sin normalizar)
    """

    # Verificamos que el archivo exista antes de continuar
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"No se encontró el archivo: {CSV_PATH}")

    # Set para guardar valores únicos (no permite duplicados)
    valores_madera = set()

    # Contador para saber cuántas filas se inspeccionaron
    total_filas = 0

    # Abrimos el CSV
    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:

        # DictReader convierte cada fila en un diccionario:
        # clave = nombre de la columna
        # valor = contenido de la celda
        reader = csv.DictReader(csvfile)

        # Validación defensiva: la columna debe existir
        if "materiales" not in reader.fieldnames:
            raise ValueError(
                f"La columna 'materiales' no existe. Columnas encontradas: {reader.fieldnames}"
            )

        # Recorremos fila por fila
        for fila in reader:
            total_filas += 1

            # Tomamos el valor de la columna 'materiales'
            celda = fila.get("materiales")

            # Si la celda está vacía, pasamos a la siguiente fila
            if not celda:
                continue

            # Buscamos la palabra 'madera' sin importar mayúsculas
            # No normalizamos: queremos ver el dato crudo
            if "madera" in celda.lower():
                # strip() elimina espacios al inicio y al final
                valores_madera.add(celda.strip())

    # ========================================================
    # SALIDA POR CONSOLA
    # ========================================================

    print("🔎 INSPECCIÓN DE MATERIALES — MADERA")
    print(f"📄 Total de filas inspeccionadas: {total_filas}")
    print(f"🌳 Valores únicos que contienen 'madera': {len(valores_madera)}\n")

    # Mostramos los valores ordenados alfabéticamente
    for valor in sorted(valores_madera):
        print(f"- {valor}")


# ============================================================
# PUNTO DE ENTRADA DEL SCRIPT
# ============================================================

# Este bloque permite que el archivo:
# - se ejecute solo
# - o sea llamado desde all.py u otro script
if __name__ == "__main__":
    inspeccionar_madera()
