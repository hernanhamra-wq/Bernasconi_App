# Documentación de Migraciones CSV → Base de Datos

## Índice de Scripts de Migración

| Script | Tabla(s) | Estado |
|--------|----------|--------|
| `_00_usuarios.py` | usuarios | ✅ Completado |
| `_01_materiales.py` | material | ✅ Completado |
| `_02_autores.py` | autor | ✅ Completado |
| `_03_tipos_plaga.py` | tipo_plaga | ✅ Completado |
| `_04_ubicaciones.py` | ubicacion_lugar, contenedor_ubicacion | ✅ Completado |
| `_05_fichas.py` | ficha_tecnica | ✅ Completado |
| `_06_ficha_autor.py` | ficha_autor (M2M) | ✅ Completado |
| `_07_ficha_material.py` | ficha_material (M2M) | ✅ Completado |
| `_08_ubicacion_inicial.py` | reg_ubicacion_actual | ⏸️ Pendiente |
| `_09_xilofagos.py` | registro_plaga | ✅ Completado |
| `_10_investigaciones.py` | investigacion | ✅ Completado |
| `_11_catalogo_multimedia.py` | catalogo_multimedia | ✅ Completado |

## Tablas SIN script de migración (no hay datos legacy)

| Tabla | App | Motivo |
|-------|-----|--------|
| estado_obra | apps/estado_obra | Seed manual (valores fijos) |
| intervencion | apps/intervencion | CSV vacío (0 filas) |
| institucion | apps_pres/institucion | Sin datos legacy |
| prestamo | apps_pres/prestamo | CSV vacío (0 filas) |
| donacion | apps_pres/donacion | Sin datos legacy |
| manejo_plagas | apps_plagas/manejo_plagas | Sin datos legacy |
| seguimiento_xilofago | apps_plagas/seguimiento_xilofago | Sin datos legacy |
| reg_ubicacion_actual | apps_ubicacion/reg_ubicacion_actual | Pendiente historial |
| reg_historial_mov | apps_ubicacion/reg_historial_mov | Sin datos legacy |

---

## Tabla: Material

### Función

Catálogo normalizado de materiales de las obras.
Centraliza y unifica los materiales detectados durante la migración desde el sistema legacy.

### Relación

- **Material ⟷ FichaTecnica** (N:M)
  La relación se resuelve mediante una tabla intermedia.

### Origen de datos

- Campo textual libre del sistema legacy.(excel/csv)
- Sin normalización, sin validaciones y con alta variabilidad semántica.

### Decisiones tomadas

- **Material es un catálogo maestro**, mantenido en `materiales_canonicos.json`.
- No depende de otras tablas del sistema.
- El catálogo se **actualiza en cada ejecución de la migración**:

  - Si el script detecta un material no existente, puede incorporarse al catálogo.

- El texto legacy se **normaliza** para evitar duplicados semánticos.
- Se eliminan:

  - colores
  - adjetivos
  - estados
  - conectores
  - partes de objetos

- Se descartan tokens que contengan números.
- Se corrigen errores de tipeo mediante similitud textual (> 0.85).
- Los nuevos materiales detectados **no se descartan**: se agregan al catálogo.
- El tipo de material se **infiere automáticamente**.
- La migración es **idempotente**: no duplica registros existentes.
- El archivo JSON actúa como **fuente de verdad** durante la migración inicial.

### Notas

- El texto original del sistema legacy no se persiste en la base de datos; se utiliza únicamente para inferencia.
- El catálogo queda preparado para reutilización, ampliación y futuras migraciones.
- La estrategia prioriza consistencia semántica sobre fidelidad literal del texto legacy.

---
## Tabla: Serie

### Función

Preservar la información de **serie** tal como fue registrada en el sistema legacy, sin reinterpretación ni normalización semántica.

### Relación

* **Serie ⟷ FichaTecnica**: **1:N lógico**
  * Cada ficha técnica posee un único valor de serie (campo textual).
  * El mismo texto de serie puede aparecer en múltiples fichas técnicas.
  * No existe una entidad Serie independiente en el modelo.

### Origen de datos

* Campo textual libre del sistema legacy (Excel / CSV).
* Sin normalización ni validaciones.
* Alta variabilidad semántica:
  * valores numéricos (`serie1`, `serie2`)
  * referencias a lugares o instituciones
  * combinaciones múltiples separadas por `;`

### Decisiones tomadas

* **Serie no se modela como tabla independiente**.
* Se mantiene como **campo de texto** en `FichaTecnica`.
* El valor legacy se **migra sin transformaciones**.
* No se infieren subatributos (año, taller, colección, etc.).
* No se aplica normalización ni catalogación.
* La migración es **idempotente** y no introduce información nueva.

### Notas

* El campo Serie no representa una entidad estable ni consistente en el sistema legacy.
* Normalizar este dato durante la migración implicaría reinterpretación histórica.
* Se prioriza fidelidad al origen y seguridad técnica por sobre estructuración forzada.
* Posibles modelos curatoriales podrán definirse en etapas posteriores, con datos consolidados.

---
## Tabla: CatalogoMultimedia

### Función

Almacena referencias a archivos multimedia (imágenes, videos, audios, documentos) asociados a cada ficha técnica.
Actualmente almacena URLs de Google Drive provenientes del sistema legacy.

### Relación

* **CatalogoMultimedia → FichaTecnica** (N:1)
  * Cada registro multimedia pertenece a una ficha técnica.
  * Una ficha puede tener múltiples archivos multimedia.

### Origen de datos

* Columna `link-fotografias` del CSV de fichas técnicas.
* URLs de carpetas o archivos de Google Drive.
* 656 fichas tienen links de fotografías (de 7738 total).

### Decisiones tomadas

* Se migra la URL completa como referencia al archivo.
* El campo `archivo` (FileField) almacena temporalmente la URL.
* En producción se debería:
  * Descargar los archivos de Drive
  * Subirlos al storage de Django
  * Actualizar las referencias
* Tipo de archivo se infiere automáticamente (default: imagen).
* La migración es **idempotente**: no duplica registros existentes.

### Campos del modelo

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT PK | Identificador único |
| ficha | INT FK | FK → ficha_tecnica |
| archivo | VARCHAR(255) | Ruta/URL del archivo |
| tipo | VARCHAR(20) | imagen, video, audio, documento |
| descripcion | VARCHAR(255) | Descripción del archivo |

### Notas

* La foto principal de una ficha se referencia en `FichaTecnica.fk_multimedia_principal`.
* Las URLs de Drive pueden cambiar; se recomienda migrar a storage propio.
* Script: `_11_catalogo_multimedia.py`

---

## Resumen de Migración

### Estadísticas actuales

| Tabla | Registros |
|-------|-----------|
| usuarios | ~692 |
| material | ~500+ (normalizado) |
| autor | ~1500+ (normalizado) |
| tipo_plaga | 4 (seed) |
| ubicacion_lugar | ~50 |
| contenedor_ubicacion | ~200 |
| ficha_tecnica | 7738 |
| ficha_autor (M2M) | ~7000+ |
| ficha_material (M2M) | ~10000+ |
| registro_plaga | 241 |
| investigacion | 6 |
| catalogo_multimedia | 656 |

### Ejecución completa

```bash
cd migrations_scripts/migraciones
python run_all.py
```

### Ejecución individual

```bash
python _11_catalogo_multimedia.py
```
