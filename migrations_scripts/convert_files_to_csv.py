import pandas as pd
import os

# -------------------------------
# 1. Definir rutas absolutas
# -------------------------------

# Carpeta donde están los archivos Excel
excel_folder = r"C:\Users\HERNAN\Documents\BERNASCONI_APP\BernasconiApp\migrations_scripts\excel_files"
# Carpeta donde se guardarán los CSV
csv_folder = r"C:\Users\HERNAN\Documents\BERNASCONI_APP\BernasconiApp\migrations_scripts\csv_files"

# -------------------------------
# 2. Listar todos los archivos Excel
# -------------------------------

# Filtrar solo archivos .xls y .xlsx
excel_files = [f for f in os.listdir(excel_folder) if f.endswith(('.xls', '.xlsx'))]

# -------------------------------
# 3. Convertir cada Excel a CSV
# -------------------------------

for excel_file in excel_files:
    # Ruta completa del archivo Excel
    excel_path = os.path.join(excel_folder, excel_file)
    
    # Leer la primera hoja del Excel
    df = pd.read_excel(excel_path, sheet_name=0)
    
    # Nombre del CSV (mismo nombre que el Excel)
    csv_file_name = os.path.splitext(excel_file)[0] + ".csv"
    csv_path = os.path.join(csv_folder, csv_file_name)
    
    # Guardar a CSV
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    print(f"{excel_file} convertido a {csv_file_name}")

print("Todos los archivos Excel han sido convertidos a CSV.")
