# BernasconiApp

Sistema de gestión de inventario patrimonial para el **Museo Bernasconi**. Desarrollado para migrar y centralizar colecciones históricas desde bases de datos Access a MySQL.

## Características

- Catálogo digital de obras y colecciones
- Gestión de autores, materiales y técnicas
- Control de intervenciones (restauraciones)
- Registro de investigaciones académicas
- Sistema de préstamos y donaciones
- Control integrado de plagas (MIT)
- Trazabilidad de ubicación física
- Auditoría automática de cambios

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
│   ├── core/               # Auditoría (AuditableModel)
│   ├── procedencia/        # Origen de obras
│   ├── usuarios/           # Usuarios y roles
│   ├── ficha_tecnica/      # Catálogo de obras (CORE)
│   ├── autor/              # Autores
│   ├── material/           # Materiales
│   └── ...
├── apps_pres/              # Préstamos y donaciones
├── apps_plagas/            # Control de plagas
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
- **Fichas Técnicas:** Catálogo completo de obras
- **Investigaciones:** Estudios académicos asociados
- **Búsqueda avanzada:** Multicampo con paginación

### En desarrollo
- Préstamos y donaciones
- Intervenciones (restauraciones)
- Control de plagas
- Gestión de ubicación

## Auditoría

El sistema registra automáticamente:
- Quién creó cada registro
- Cuándo se creó
- Quién lo modificó
- Cuándo se modificó

Esta información es invisible al usuario y se gestiona mediante middleware.

---

## Documentación de Migración

Ver carpeta `BASE_DE_DATOS_Y_MIGRACIONES.md`:
- `00_criterio_migracion.md` — Criterios generales y orden
- `01_catalogos.md` — Catálogos base
- `02_entidades_base.md` — Autor, multimedia, etc.
- `03_ficha_tecnica.md` — Tabla madre
- `04_serie.md` — Uso especial estampas
- `decisiones_modelado.md` — Decisiones importantes
- `problemas_legacy.md` — Datos confusos del sistema anterior

---

## Licencia

Proyecto privado - Museo Bernasconi
