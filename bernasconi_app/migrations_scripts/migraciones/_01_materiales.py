import os
import sys
import csv
import json
import re
import django
from difflib import SequenceMatcher

# ============================================================
# CONFIG DJANGO
# ============================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bernasconi_app.settings")
django.setup()

from apps.material.models import Material

# ============================================================
# RUTAS
# ============================================================
CSV_PATH = os.path.join(BASE_DIR, "migrations_scripts", "csv_files", "ficha técnica.csv")
JSON_PATH = os.path.join(BASE_DIR, "migrations_scripts", "json_files", "materiales_canonicos.json")

# ============================================================
# HELPERS
# ============================================================

def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    return text.strip()

def tokenize_material(text: str) -> list:
    """
    Tokenizador estricto: separa por simbolos, camelcase,
    elimina palabras cortas y CUALQUIER palabra con números.
    """
    if not text: return []

    # 1. Separar CamelCase
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # 2. Separar por símbolos y conectores
    text = re.sub(r'(?i)\s+y\s+|\s+con\s+|[\+\/\(\)\-\.\*\:\,]', ' ', text)

    palabras = text.split()
    
    exclusiones = {
        # Conectores y comunes
        "de", "en", "el", "la", "con", "del", "sin", "id", "los", "las", 
        "para", "por", "como", "son", "sobre", "esta", "donde", "tiene",
        # Colores (Se ignoran como materiales)
        "azul", "blanco", "negro", "negra", "rojo", "roja", "gris", "marron", 
        "bordo", "rosado", "rosada", "plateado", "dorado",
        # Estados y Adjetivos
        "alterado", "amuecada", "amigdaloide", "bandeado", "barnizada", 
        "bañado", "bordado", "cocida", "cocido", "color", "cristalina", 
        "depósito", "enchapado", "enlozado", "entelada", "esmaltada", 
        "especular", "forrado", "galvanizada", "magnética", "pintado", 
        "posible", "priori", "revestido", "usado", "variedades",
        # Objetos/Partes (No son materiales)
        "broche", "cable", "caja", "cinta", "clavos", "cobertor", "conector", 
        "cuadro", "etiqueta", "hojas", "marco", "moneda", "tapa", "uniones"
    }
    
    resultado = []
    for p in palabras:
        # REGLA: Si tiene números, se va (ej: 100, 70etiqueta)
        if any(char.isdigit() for char in p):
            continue
            
        p_norm = normalize_text(p)
        
        # REGLA: Solo palabras de más de 3 letras que no estén en exclusiones
        if p_norm and p_norm not in exclusiones and len(p_norm) > 3:
            resultado.append(p_norm)
            
    return resultado

def to_camel_case(text: str) -> str:
    return "".join(word.capitalize() for word in text.split())

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def infer_tipo(nombre: str) -> str:
    n = nombre.lower()
    if any(k in n for k in ["madera", "papel", "carton", "cuero", "tela", "lana", "algodon", "fibra"]):
        return "Orgánico"
    if any(k in n for k in ["metal", "hierro", "cobre", "bronce", "aluminio", "plata", "acero", "niquel", "zinc"]):
        return "Metal"
    if any(k in n for k in ["vidrio", "ceramica", "porcelana", "loza", "yeso"]):
        return "Inorgánico"
    if any(k in n for k in ["liquido", "alcohol", "aceite", "formol", "nafta", "kerosene"]):
        return "Líquido"
    if any(k in n for k in ["biologico", "hueso", "piel", "marfil", "pelo", "pluma"]):
        return "Biológico"
    if any(k in n for k in ["cuarzo", "marmol", "basalto", "piedra", "lutita", "mica", "mineral"]):
        return "Mineral"
    return "Sin clasificar"

# ============================================================
# MAIN
# ============================================================

def run():
    print("▶ Iniciando Migración Estricta de Materiales")

    if not os.path.exists(JSON_PATH):
        print(f"❌ Error: No se encuentra el JSON en {JSON_PATH}")
        return

    with open(JSON_PATH, encoding="utf-8") as f:
        canonicos = json.load(f)

    canon_map = {normalize_text(m["nombre"]): m for m in canonicos}
    encontrados_finales = set()
    nuevos_nombres = []
    corregidos = []

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for fila in reader:
            celda = fila.get("materiales")
            if not celda: continue

            tokens = tokenize_material(celda)
            for t in tokens:
                encontrados_finales.add(t)

    for mat in sorted(encontrados_finales):
        if mat in canon_map:
            continue

        similar = None
        for canon_key in canon_map:
            # 0.85 es el balance ideal para corregir errores de tipeo
            if similarity(mat, canon_key) >= 0.85:
                similar = canon_key
                break

        if similar:
            corregidos.append((mat, canon_map[similar]["nombre"]))
            continue

        nombre_final = to_camel_case(mat)
        tipo = infer_tipo(mat)

        nuevo_item = {
            "nombre": nombre_final,
            "tipo": tipo,
            "descripcion": "Material detectado durante la migración"
        }

        canonicos.append(nuevo_item)
        canon_map[mat] = nuevo_item
        nuevos_nombres.append(nombre_final)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(canonicos, f, ensure_ascii=False, indent=2)

    print("💾 Persistiendo en Base de Datos...")
    for m in canonicos:
        Material.objects.get_or_create(
            nombre=m["nombre"],
            defaults={
                "tipo": m["tipo"],
                "descripcion": m["descripcion"]
            }
        )

    print(f"\n✔ Proceso finalizado.")
    print(f"🆕 Nuevos materiales únicos: {len(nuevos_nombres)}")
    print(f"🛠 Correcciones aplicadas: {len(corregidos)}")
    if nuevos_nombres:
        print(f"Lista de nuevos registrados: {', '.join(nuevos_nombres)}")

if __name__ == "__main__":
    run()