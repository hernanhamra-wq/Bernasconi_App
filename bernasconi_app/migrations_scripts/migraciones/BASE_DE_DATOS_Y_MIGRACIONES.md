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
