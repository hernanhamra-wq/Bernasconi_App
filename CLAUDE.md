# BernasconiApp - Contexto del Proyecto

## Stack
- **Backend:** Django 5.0.3 / Python 3 / MySQL
- **Frontend:** Templates Django + CSS custom
- **Entorno:** `.venv/` (Windows: `.venv\Scripts\activate`)

## Estructura
```
BernasconiApp/bernasconi_app/
├── bernasconi_app/     # Settings, urls, wsgi
├── apps/               # Core, ficha_tecnica, autor, material, etc.
├── apps_pres/          # Préstamos, donaciones, instituciones
├── apps_plagas/        # Registro plagas, seguimiento xilófagos
├── apps_ubicacion/     # Lugares, contenedores, movimientos
├── templates/          # Templates globales + crud/
├── static/css/         # base.css (tema claro/oscuro)
└── media/              # Archivos subidos
```

## Comandos
```bash
python bernasconi_app/manage.py runserver
python bernasconi_app/manage.py makemigrations
python bernasconi_app/manage.py migrate
python bernasconi_app/manage.py check
```

## Convenciones
- Apps en español, modelos en singular
- FKs con prefijo `fk_` (fk_procedencia, fk_estado)
- `AuditableModel` para auditoría automática (created_at, updated_at, created_by, updated_by)

## Componentes Reutilizables

### CRUDViewMixin (`apps/core/crud_views.py`)
```python
from apps.core.crud_views import CRUDViewMixin

class MiViews(CRUDViewMixin):
    model = MiModelo
    form_class = MiForm
    app_name = 'mi_app'
    list_columns = [{'field': 'nombre', 'label': 'Nombre', 'is_link': True}]
    search_fields = ['nombre', 'descripcion']

# urls.py
mi_views = MiViews()
urlpatterns = mi_views.get_urls()
```

### Templates Genéricos (`templates/crud/`)
- `generic_list.html` - Lista con búsqueda, paginación, filtros
- `generic_form.html` - Formulario crear/editar
- `generic_detail.html` - Vista detalle
- `generic_delete.html` - Confirmación eliminar

## Principios de Desarrollo

1. **Reutilización** - Crear componentes genéricos antes de repetir código
2. **Preguntar** - Si una tarea implica 3+ archivos similares, proponer solución genérica
3. **Orden** - Base primero, implementaciones después, ajustes al final
4. **Tokens** - Usar herencia de templates, mixins, no repetir

## CRUDs Implementados
| Módulo | App | URL |
|--------|-----|-----|
| Fichas Técnicas | ficha_tecnica | /ficha/ |
| Autores | autor | /autores/ |
| Materiales | material | /materiales/ |
| Multimedia | catalogo_multimedia | /multimedia/ |
| Situaciones | estado_obra | /estados/ |
| Lugares | ubicacion_lugar | /lugares/ |
| Contenedores | contenedor_ubicacion | /contenedores/ |
| Movimientos | reg_historial_mov | /movimientos/ |
| Préstamos | prestamo | /prestamos/ |
| Donaciones | donacion | /donaciones/ |
| Instituciones | institucion | /instituciones/ |
| Intervenciones | intervencion | /intervenciones/ |
| Registro Plagas | registro_plaga | /registro-plagas/ |
| Seguimiento Xilófagos | seguimiento_xilofago | /seguimiento-xilofagos/ |
| Investigaciones | investigacion | /investigacion/ |
| Usuarios | usuarios | /usuarios/ |
| Auditoría | core | /config/auditoria/ |

## Notas
- Tema claro/oscuro en CSS con `[data-theme="dark"]`
- Migraciones de datos en `migrations_scripts/migraciones/` (ya ejecutadas)
- `EstadoObra` = Situación operativa (Exposición, Depósito, Cuarentena, etc.)
- `estado_conservacion` en FichaTecnica = Condición física (Bueno/Regular/Malo)
