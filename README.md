# BernasconiApp

Sistema de gestión de inventario patrimonial para el **Museo Bernasconi**. Desarrollado para migrar y centralizar colecciones históricas desde bases de datos Access a MySQL.

## Características

- Catálogo digital de obras y colecciones
- Gestión de autores, materiales y técnicas
- Control de intervenciones (restauraciones)
- Registro de investigaciones académicas
- Sistema de préstamos y donaciones con workflow de estados
- Control integrado de plagas (MIT)
- Trazabilidad de ubicación física
- Auditoría automática de cambios (created_by, updated_by)
- Campos Dublin Core para interoperabilidad museística
- Gestión de condiciones de conservación
- Control de propiedad legal y derechos

## Requisitos

- Python 3.10+
- MySQL 5.7+
- pip

## Instalación

```bash
# Clonar repositorio
git clone <url-del-repo>
cd BernasconiApp

# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows)
.venv\Scripts\activate

# Activar entorno (Linux/Mac)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp bernasconi_app/.env.example bernasconi_app/.env
# Editar .env con credenciales de MySQL

# Aplicar migraciones
python bernasconi_app/manage.py migrate

# Crear superusuario
python bernasconi_app/manage.py createsuperuser

# Ejecutar servidor
python bernasconi_app/manage.py runserver
```

## Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Backend | Django 5.0.3 |
| Base de datos | MySQL |
| Frontend | Templates Django |
| Autenticación | Django Auth |

## Estructura del Proyecto

```
bernasconi_app/
├── apps/                   # Apps principales
│   ├── core/               # Auditoría (AuditableModel + middleware)
│   ├── procedencia/        # Origen de obras (reutilizable)
│   ├── usuarios/           # Usuarios y roles
│   ├── ficha_tecnica/      # Catálogo de obras (CORE)
│   ├── autor/              # Autores (M2M con fichas)
│   ├── material/           # Materiales (M2M con fichas)
│   ├── taller/             # Talleres de restauración
│   ├── catalogo_multimedia/# Archivos multimedia (FileField)
│   ├── estado_obra/        # Estados de conservación
│   ├── intervencion/       # Restauraciones
│   └── investigacion/      # Estudios académicos
├── apps_pres/              # Préstamos y donaciones
│   ├── institucion/        # Instituciones colaboradoras
│   ├── prestamo/           # Préstamos con workflow de estados
│   └── donacion/           # Donaciones recibidas
├── apps_plagas/            # Control de plagas (MIT)
├── apps_ubicacion/         # Ubicación física
├── templates/              # Templates HTML
└── static/                 # CSS, JS, imágenes
```

## Roles de Usuario

| Rol | Permisos |
|-----|----------|
| SuperAdmin | Control total + gestión de usuarios |
| Admin | CRUD de fichas, intervenciones, investigaciones |
| Guest | Solo lectura/consulta |

## Módulos

### Funcionales
- **Fichas Técnicas:** Catálogo completo de obras con campos Dublin Core
- **Investigaciones:** Estudios académicos asociados
- **Búsqueda avanzada:** Multicampo con paginación
- **Procedencia:** Registro de origen de obras (donación, compra, legado, etc.)

### En desarrollo
- Préstamos y donaciones (modelos con workflow listos)
- Intervenciones (restauraciones)
- Control de plagas

## Sistema de Ubicación

### Lugares Físicos
Tipos: SALA, DEPOSITO, TALLER, ARCHIVO, LABORATORIO, CUARENTENA, EXTERNO

### Movimientos
Registro completo de origen y destino con estados:
- PENDIENTE → EN_TRANSITO → COMPLETADO / CANCELADO

Motivos: EXPOSICION, RESTAURACION, PRESTAMO, CUARENTENA, INVESTIGACION, etc.

### Contenedores
Tipos: CAJON, CAJA, VITRINA, RACK, ESTANTE, PLANERO, PESEBRE, TUBO, etc.

Funcionalidades:
- Jerarquía de contenedores (contenedor dentro de contenedor)
- Control de capacidad y estado (DISPONIBLE, PARCIAL, LLENO)
- Cálculo automático de ocupación

## Campos de Ficha Técnica

### Dublin Core (Interoperabilidad)
| Campo | Descripción |
|-------|-------------|
| `categoria_objeto` | Tipo de pieza (PINTURA, ESCULTURA, GRABADO, etc.) |
| `periodo_historico` | Época de la obra |
| `datacion` | Fecha estimada |
| `origen_geografico` | Lugar de creación |
| `tematica` | Tema principal |
| `palabras_clave` | Tags para búsqueda |

### Conservación
| Campo | Descripción |
|-------|-------------|
| `temperatura_requerida_min/max` | Rango de temperatura (°C) |
| `humedad_requerida_min/max` | Rango de humedad (%) |
| `nivel_iluminacion` | BAJA, MEDIA, ALTA, SIN_RESTRICCION |
| `requiere_vitrina` | Si necesita exhibirse en vitrina |
| `condiciones_especiales` | Requisitos adicionales |

### Propiedad Legal
| Campo | Descripción |
|-------|-------------|
| `propietario_legal` | Dueño de la obra |
| `tipo_propiedad` | PROPIEDAD_MUSEO, COMODATO, DEPOSITO, etc. |
| `derechos_reproduccion` | Restricciones de uso |
| `nivel_confidencialidad` | PUBLICO, RESTRINGIDO, CONFIDENCIAL |

## Auditoría

El sistema registra automáticamente mediante `AuditableModel` y middleware:
- `created_by` / `created_at` — Quién y cuándo creó
- `updated_by` / `updated_at` — Quién y cuándo modificó

Esta información es invisible al usuario y se gestiona automáticamente.

## Workflow de Préstamos

```
SOLICITADO → EN_EVALUACION → APROBADO → EN_PREPARACION → EN_TRANSITO_IDA
→ EN_DESTINO → EN_TRANSITO_VUELTA → DEVUELTO
                    ↓
               RECHAZADO / CANCELADO
```

---

## Documentación Técnica

- **CLAUDE.md** — Contexto técnico para desarrolladores
- **BASE_DE_DATOS_Y_MIGRACIONES.md/** — Documentación de migración desde Access

---

## Licencia

Proyecto privado - Museo Bernasconi
