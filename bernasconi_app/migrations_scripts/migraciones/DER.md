# Diagrama Entidad-Relación (DER)

## Diagrama Principal

```mermaid
erDiagram
    %% ============================================
    %% CORE: Ficha Técnica y relaciones directas
    %% ============================================

    FichaTecnica {
        bigint id PK
        bigint n_de_ficha
        varchar inventario UK
        text titulo
        text descripcion
        varchar anio
        varchar estado_conservacion
        datetime fecha_de_carga
        datetime fecha_de_modificacion
        float ancho
        float alto
        float profundidad
        float diametro
        boolean seguimiento
    }

    Usuario {
        bigint id PK
        varchar username UK
        varchar email
        varchar rol
    }

    Autor {
        bigint id PK
        varchar nombre
        text biografia
    }

    Material {
        bigint id PK
        varchar nombre UK
        varchar tipo
        text descripcion
    }

    EstadoObra {
        bigint id PK
        varchar nombre_estado UK
    }

    Taller {
        bigint id PK
        varchar nombre
        varchar direccion
    }

    Procedencia {
        bigint id PK
        varchar tipo_procedencia
        varchar descripcion
    }

    %% Relaciones M2M
    FichaAutor {
        bigint id PK
        int fk_ficha_id FK
        int fk_autor_id FK
        int orden
    }

    FichaMaterial {
        bigint id PK
        int ficha_id FK
        int material_id FK
        varchar detalle
    }

    %% Relaciones
    FichaTecnica ||--o{ FichaAutor : "tiene"
    Autor ||--o{ FichaAutor : "participa"
    FichaTecnica ||--o{ FichaMaterial : "usa"
    Material ||--o{ FichaMaterial : "compone"
    FichaTecnica }o--|| EstadoObra : "estado_funcional"
    FichaTecnica }o--|| Usuario : "responsable_carga"
    FichaTecnica }o--o| Taller : "restaurado_en"
    FichaTecnica }o--o| Procedencia : "origen"

    %% ============================================
    %% MULTIMEDIA
    %% ============================================

    CatalogoMultimedia {
        bigint id PK
        int ficha_id FK
        varchar archivo
        varchar tipo
        varchar descripcion
    }

    FichaTecnica ||--o{ CatalogoMultimedia : "multimedia"
    FichaTecnica }o--o| CatalogoMultimedia : "foto_principal"

    %% ============================================
    %% INVESTIGACIONES E INTERVENCIONES
    %% ============================================

    Investigacion {
        int investigacion_id PK
        int ficha_id FK
        int investigador_id FK
        int num_investigacion
        varchar titulo
        text detalle
        int anio_realizacion
    }

    Intervencion {
        int intervencion_id PK
        int ficha_id FK
        int responsable_id FK
        int n_intervencion
        date fecha_inicio
        date fecha_finalizacion
        text diagnostico
        text procedimientos
    }

    FichaTecnica ||--o{ Investigacion : "investigaciones"
    Usuario ||--o{ Investigacion : "realiza"
    FichaTecnica ||--o{ Intervencion : "intervenciones"
    Usuario ||--o{ Intervencion : "responsable"
```

## Diagrama de Ubicaciones

```mermaid
erDiagram
    %% ============================================
    %% SISTEMA DE UBICACIÓN
    %% ============================================

    UbicacionLugar {
        bigint id PK
        varchar nombre_lugar UK
        varchar tipo_lugar
        boolean permite_contenedores
        varchar observacion
    }

    ContenedorUbicacion {
        bigint id PK
        varchar nombre_contenedor
        int fk_lugar_general_id FK
        int fk_padre_id FK
        varchar tipo_contenedor
        varchar modo_almacenamiento
        int capacidad_maxima
        varchar estado
    }

    RegUbicacionActual {
        bigint id PK
        int fk_ficha_id FK
        int fk_estado_id FK
        int fk_lugar_id FK
        int fk_contenedor_id FK
        datetime fecha_desde
    }

    RegHistorialMov {
        bigint id PK
        int fk_ficha_id FK
        int fk_lugar_origen_id FK
        int fk_lugar_destino_id FK
        int fk_contenedor_origen_id FK
        int fk_contenedor_destino_id FK
        datetime fecha_movimiento
        varchar motivo
        varchar estado
    }

    %% Relaciones
    UbicacionLugar ||--o{ ContenedorUbicacion : "contiene"
    ContenedorUbicacion ||--o{ ContenedorUbicacion : "padre-hijo"

    FichaTecnica ||--o| RegUbicacionActual : "ubicacion_actual"
    UbicacionLugar ||--o{ RegUbicacionActual : "lugar"
    ContenedorUbicacion ||--o{ RegUbicacionActual : "contenedor"
    EstadoObra ||--o{ RegUbicacionActual : "estado"

    FichaTecnica ||--o{ RegHistorialMov : "movimientos"
    UbicacionLugar ||--o{ RegHistorialMov : "origen"
    UbicacionLugar ||--o{ RegHistorialMov : "destino"
```

## Diagrama de Préstamos y Donaciones

```mermaid
erDiagram
    %% ============================================
    %% PRÉSTAMOS Y DONACIONES
    %% ============================================

    Institucion {
        bigint id PK
        varchar nombre
        varchar tipo_institucion
        varchar direccion
        varchar contacto_persona
        varchar telefono
        varchar email
    }

    Prestamo {
        bigint id PK
        int ficha_id FK
        int institucion_origen_id FK
        int institucion_destino_id FK
        varchar n_de_prestamo
        date fecha_inicio
        date fecha_fin_prevista
        date fecha_devolucion_real
        varchar estado
        decimal seguro_solicitado
        decimal costo_traslado
    }

    Donacion {
        bigint id PK
        int ficha_id FK
        int institucion_donante_id FK
        date fecha_donacion
        varchar condicion_legal
        decimal valuacion
        varchar documento_pdf
    }

    %% Relaciones
    FichaTecnica ||--o{ Prestamo : "prestamos"
    Institucion ||--o{ Prestamo : "origen"
    Institucion ||--o{ Prestamo : "destino"
    Usuario ||--o{ Prestamo : "responsable"

    FichaTecnica ||--o{ Donacion : "donaciones"
    Institucion ||--o{ Donacion : "donante"
    Usuario ||--o{ Donacion : "registra"
```

## Diagrama de Control de Plagas

```mermaid
erDiagram
    %% ============================================
    %% CONTROL DE PLAGAS (MIT)
    %% ============================================

    TipoPlaga {
        bigint id PK
        varchar nombre
        text descripcion
        text recomendaciones_tratamiento
        text historial_apariciones
    }

    ManejoPlagas {
        bigint id PK
        int ficha_id FK
        int responsable_id FK
        int tipo_plaga_id FK
        varchar titulo
        text propuesta_detalle
    }

    RegistroPlaga {
        int registro_id PK
        int ficha_id FK
        int manejo_id FK
        int tipologia_plaga_id FK
        date fecha_registro
        int conteo_larvas
        int conteo_esqueletos
        int conteo_incisiones
        int conteo_tapones
        text observaciones
    }

    SeguimientoXilofago {
        int seguimiento_id PK
        int registro_plaga_id FK
        date fecha_seguimiento
        text observacion
        varchar nueva_actividad
    }

    %% Relaciones
    FichaTecnica ||--o{ ManejoPlagas : "planes_mit"
    TipoPlaga ||--o{ ManejoPlagas : "tipo"
    Usuario ||--o{ ManejoPlagas : "responsable"

    FichaTecnica ||--o{ RegistroPlaga : "registros_plaga"
    ManejoPlagas ||--o{ RegistroPlaga : "plan"
    TipoPlaga ||--o{ RegistroPlaga : "tipologia"

    RegistroPlaga ||--o{ SeguimientoXilofago : "seguimientos"
```

## Resumen de Relaciones

### Tabla Central: FichaTecnica

| Relación | Tipo | Tabla Relacionada |
|----------|------|-------------------|
| autores | M:N | Autor (via FichaAutor) |
| materiales | M:N | Material (via FichaMaterial) |
| estado_funcional | N:1 | EstadoObra |
| responsable_carga | N:1 | Usuario |
| taller | N:1 | Taller |
| procedencia | N:1 | Procedencia |
| multimedia_principal | N:1 | CatalogoMultimedia |
| catalogo_multimedia | 1:N | CatalogoMultimedia |
| investigaciones | 1:N | Investigacion |
| intervenciones | 1:N | Intervencion |
| ubicacion_actual | 1:1 | RegUbicacionActual |
| historial_movimientos | 1:N | RegHistorialMov |
| prestamos | 1:N | Prestamo |
| donaciones | 1:N | Donacion |
| planes_mit | 1:N | ManejoPlagas |
| registros_plaga | 1:N | RegistroPlaga |

### Cardinalidades

- **1:1** - Una ficha tiene una ubicación actual
- **1:N** - Una ficha puede tener múltiples investigaciones, intervenciones, movimientos, etc.
- **M:N** - Autores y materiales se relacionan con fichas mediante tablas intermedias
- **N:1** - Múltiples fichas pueden tener el mismo estado, responsable, taller, etc.

---

*Generado automáticamente - Última actualización: 2024-12*
