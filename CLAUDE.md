# BernasconiApp - Contexto del Proyecto

## Descripción
Sistema de gestión de inventario patrimonial para el **Museo Bernasconi**. Centraliza el catálogo de obras, colecciones históricas y artefactos. Migrado desde bases de datos Access a MySQL.

## Stack Tecnológico
- **Backend:** Django 5.0.3 (Python 3)
- **Base de datos:** MySQL
- **ORM:** Django ORM
- **Frontend:** Templates Django (HTML/CSS/JS)
- **Entorno virtual:** `.venv/`

## Estructura del Proyecto

```
BernasconiApp/
├── .venv/                      # Entorno virtual Python
├── bernasconi_app/             # Proyecto Django principal
│   ├── bernasconi_app/         # Configuración (settings, urls, wsgi)
│   ├── apps/                   # Apps principales
│   │   ├── core/               # Modelo base AuditableModel + middleware
│   │   ├── procedencia/        # Origen de obras (reutilizable)
│   │   ├── usuarios/           # Modelo de usuario personalizado
│   │   ├── ficha_tecnica/      # CORE - Catálogo de obras
│   │   ├── autor/              # Autores (M2M con fichas)
│   │   ├── material/           # Materiales (M2M con fichas)
│   │   ├── taller/             # Talleres de restauración
│   │   ├── catalogo_multimedia/# Archivos multimedia
│   │   ├── estado_obra/        # Estados de conservación
│   │   ├── intervencion/       # Restauraciones
│   │   └── investigacion/      # Estudios académicos
│   ├── apps_pres/              # Apps de préstamos
│   │   ├── institucion/        # Instituciones colaboradoras
│   │   ├── prestamo/           # Préstamos de obras
│   │   └── donacion/           # Donaciones recibidas
│   ├── apps_plagas/            # Control de plagas (MIT)
│   │   ├── tipo_plaga/         # Catálogo de plagas
│   │   ├── manejo_plagas/      # Planes de manejo
│   │   ├── registro_plaga/     # Registros de avistamiento
│   │   └── seguimiento_xilofago/ # Seguimiento de xilófagos
│   ├── apps_ubicacion/         # Ubicación física
│   │   ├── ubicacion_lugar/    # Lugares (salas, depósitos)
│   │   ├── contenedor_ubicacion/ # Contenedores jerárquicos
│   │   ├── reg_ubicacion_actual/ # Ubicación actual de obras
│   │   └── reg_historial_mov/  # Historial de movimientos
│   ├── templates/              # Templates globales
│   ├── static/                 # CSS, JS, imágenes
│   └── media/                  # Archivos subidos (multimedia)
└── README.md
```

## Comandos Importantes

```bash
# Activar entorno virtual (Windows)
.venv\Scripts\activate

# Ejecutar servidor de desarrollo
python bernasconi_app/manage.py runserver

# Crear migraciones
python bernasconi_app/manage.py makemigrations

# Aplicar migraciones
python bernasconi_app/manage.py migrate

# Crear superusuario
python bernasconi_app/manage.py createsuperuser

# Verificar configuración
python bernasconi_app/manage.py check
```

## Roles de Usuario
- **SUPERADMIN:** Control total + gestión de usuarios
- **ADMIN:** CRUD de fichas, intervenciones, investigaciones
- **GUEST:** Solo lectura/consulta

## Decisiones de Arquitectura

### Auditoría (apps.core)
- Modelo abstracto `AuditableModel` con campos: `created_at`, `updated_at`, `created_by`, `updated_by`
- Middleware `CurrentUserMiddleware` captura usuario automáticamente
- Los campos de auditoría son **invisibles al usuario** y se llenan automáticamente

### Integridad Referencial
- FKs de auditoría usan `on_delete=PROTECT` para no perder trazabilidad
- Si se intenta eliminar un usuario con registros asociados, Django lo impide

### Procedencia (apps.procedencia)
- Tabla reutilizable para registrar origen de obras
- Permite asociar múltiples obras a la misma procedencia
- Tipos: DONACION, COMPRA, LEGADO, TRANSFERENCIA, EXCAVACION, COMODATO, DEPOSITO

### Inventario
- Campo `inventario` en FichaTecnica tiene constraint `unique=True`
- Garantiza unicidad a nivel de base de datos

### Multimedia
- `CatalogoMultimedia.archivo` es `FileField` (no CharField)
- Los archivos se guardan en `media/multimedia/{tipo}/{año}/{mes}/`

## Convenciones de Código
- Nombres de apps en español
- Modelos en singular (Autor, Material, Ficha)
- ForeignKeys con prefijo `fk_` (fk_procedencia, fk_estado)
- Verbose_name en español para el admin

## Variables de Entorno (.env)
```
DB_NAME=bernasconi_db
DB_USER=root
DB_PASSWORD=****
DB_HOST=localhost
DB_PORT=3306
```

## Estado del Proyecto

### Funcional
- Gestión de Fichas Técnicas (CRUD)
- Búsqueda avanzada
- Gestión de Investigaciones
- Autenticación por roles
- Admin de Django

### En desarrollo (modelos listos, sin vistas)
- Préstamos
- Donaciones
- Intervenciones
- Sistema de Plagas
- Sistema de Ubicación

## Fases de Desarrollo

### FASE 1 - Completada
- App core (auditoría)
- App procedencia
- Inventario único
- PROTECT en FKs de auditoría
- usuario_registro en modelos
- FileField para multimedia

### FASE 2 - Completada
- Choices en campos de texto libre:
  - `tipo_lugar` en UbicacionLugar (SALA, DEPOSITO, TALLER, ARCHIVO, LABORATORIO, EXTERNO)
  - `tipo_institucion` en Institucion (MUSEO, UNIVERSIDAD, FUNDACION, GALERIA, etc.)
  - `condicion_legal` en Donacion (PLENA_PROPIEDAD, COMODATO, DEPOSITO, LEGADO, etc.)
  - `motivo` en RegHistorialMov (EXPOSICION, RESTAURACION, PRESTAMO, ALMACENAMIENTO, etc.)
- Campo `estado` en Prestamo con workflow completo (SOLICITADO→EN_EVALUACION→APROBADO→EN_DESTINO→DEVUELTO)
- Campo `contacto` en Taller separado en: `persona_contacto`, `email`, `telefono`

### FASE 3 - Completada
- Campos Dublin Core en FichaTecnica:
  - `categoria_objeto` (PINTURA, ESCULTURA, GRABADO, etc.)
  - `periodo_historico`, `datacion`, `origen_geografico`
  - `tematica`, `palabras_clave`
- Campos de conservación en FichaTecnica:
  - `temperatura_requerida_min/max`, `humedad_requerida_min/max`
  - `nivel_iluminacion` (BAJA, MEDIA, ALTA, SIN_RESTRICCION)
  - `requiere_vitrina`, `condiciones_especiales`
- Campos de propiedad legal en FichaTecnica:
  - `propietario_legal`, `tipo_propiedad` (PROPIEDAD_MUSEO, COMODATO, etc.)
  - `derechos_reproduccion`, `nivel_confidencialidad`

### FASE 4 - Completada (Ubicación)

#### Lugares (ubicacion_lugar)
- TIPO_LUGAR_CHOICES: SALA, DEPOSITO, TALLER, ARCHIVO, LABORATORIO, **CUARENTENA**, EXTERNO
- Campo `permite_contenedores` para habilitar/deshabilitar contenedores

#### Movimientos (reg_historial_mov)
- Campos de origen: `fk_lugar_origen`, `fk_contenedor_origen`
- Campos de destino: `fk_lugar_destino`, `fk_contenedor_destino`
- MOTIVO_CHOICES: EXPOSICION, RESTAURACION, PRESTAMO, ALMACENAMIENTO, INVESTIGACION, FOTOGRAFIA, MANTENIMIENTO, REUBICACION, **CUARENTENA**, EMERGENCIA, OTRO
- ESTADO_MOVIMIENTO_CHOICES: PENDIENTE, EN_TRANSITO, COMPLETADO, CANCELADO
- Campo `observaciones`
- FK `fk_responsable_mov` con PROTECT

#### Contenedores (contenedor_ubicacion)
- TIPO_CONTENEDOR: CAJON, CAJA, VITRINA, RACK, ESTANTE, SOBRE, CARPETA, **PLANERO**, **PESEBRE**, **TUBO**, OTRO
- MODO_ALMACENAMIENTO: DIRECTO (sin contenedor), EN_CONTENEDOR
- ESTADO_CONTENEDOR: DISPONIBLE, PARCIAL, LLENO, EN_REPARACION, BAJA
- Campo `capacidad_maxima` (opcional)
- Constraint único: `(nombre_contenedor, fk_lugar_general)`
- Métodos: `obras_actuales()`, `espacio_disponible()`, `porcentaje_ocupacion()`, `ruta_completa()`

#### FichaTecnica - Métodos de ubicación
- `ubicacion_actual()`: Retorna dict con lugar, contenedor, fecha, motivo del último movimiento COMPLETADO
- `en_cuarentena()`: Retorna True si la obra está en área de cuarentena

#### Modelo deprecado
- `RegUbicacionActual`: Marcado como DEPRECADO. Usar `FichaTecnica.ubicacion_actual()` en su lugar.
- Se mantiene temporalmente por compatibilidad con datos legacy
