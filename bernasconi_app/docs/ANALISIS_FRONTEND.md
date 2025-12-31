# Análisis del Frontend - BernasconiApp

**Fecha:** 2025-12-31
**Estado:** Documentación para revisión futura

---

## Resumen de Correcciones Realizadas

### Errores Corregidos (Commits)

1. **`35a0855` - fix(ficha_tecnica): Corregir select_related con campos FK obsoletos**
   - Error 500 en `/ficha/buscar/` por campos FK inexistentes
   - Cambios: `fk_estado` → `fk_estado_funcional`, eliminar `fk_serie`
   - Agregar `fk_taller`, `fk_procedencia` a queries

2. **`4042833` - fix(ficha_tecnica): Actualizar templates y forms con campos FK correctos**
   - Actualizar forms.py con labels correctos
   - Actualizar 5 templates con nombres de campo correctos

---

## Estructura Actual de Templates

```
templates/                              # Globales
├── base_login.html                     # Base para login
├── base_main.html                      # Base para páginas autenticadas
├── home.html                           # Página principal
└── registration/
    ├── login.html
    └── logged_out.html

apps/ficha_tecnica/templates/ficha_tecnica/
├── fichatecnica_list.html              # Listado (NO usa base)
├── buscar_ficha_tecnica.html           # Búsqueda (NO usa base)
├── detalle_ficha_tecnica.html          # Detalle (NO usa base)
├── formulario.html                     # Carga (NO usa base)
└── editar_ficha_tecnica.html           # Edición

apps/investigacion/templates/investigacion/
├── buscar_investigacion.html           # (NO usa base)
├── detalle_investigacion.html
└── formulario.html                     # (NO usa base)
```

---

## Estructura de CSS

```
static/css/
├── styles_login.css                    # Login
├── styles_main.css                     # Home
├── ficha_tecnica.css                   # Formulario ficha
├── investigacion_form.css              # Formulario investigación
└── buscar_ficha_tecnica.css            # Búsqueda

apps/ficha_tecnica/static/css/
└── buscar_ficha_tecnica.css            # (¿Duplicado?)
```

---

## Problemas Detectados

| # | Problema | Ubicación | Impacto | Prioridad |
|---|----------|-----------|---------|-----------|
| 1 | Templates no usan herencia | Mayoría de templates | Duplicación HTML, difícil mantener | Alta |
| 2 | CSS disperso en 4+ archivos | static/css/ + apps/ | Inconsistencia visual | Alta |
| 3 | Menú navegación incompleto | home.html | Links a "#" no funcionan | Alta |
| 4 | Sin header/navbar común | Cada template propio | Inconsistencia UX | Alta |
| 5 | Tabla de resultados duplicada | list.html y buscar.html | Código duplicado | Media |
| 6 | Paginación solo en búsqueda | buscar_ficha_tecnica.html | UX inconsistente | Media |
| 7 | Sin breadcrumbs | Todos | Navegación confusa | Media |
| 8 | Sin loading states | Tablas grandes | UX pobre en 7700+ registros | Media |

---

## Sugerencias de Mejora

### 1. Estructura de Templates (Prioridad Alta)

**Crear layout base único:**

```
templates/
├── base.html                           # Base común
├── layouts/
│   ├── layout_auth.html                # Para páginas autenticadas
│   └── layout_public.html              # Para login/registro
└── partials/
    ├── _navbar.html                    # Navbar reutilizable
    ├── _sidebar.html                   # Sidebar (opcional)
    ├── _messages.html                  # Mensajes flash
    └── _pagination.html                # Paginación reutilizable
```

**Beneficios:**
- Un solo lugar para modificar header/navbar
- Consistencia visual automática
- Menos código duplicado

### 2. CSS Consolidado (Prioridad Alta)

**Reorganizar:**
```
static/css/
├── base.css                            # Variables, reset, tipografía
├── components/
│   ├── buttons.css
│   ├── forms.css
│   ├── tables.css
│   └── cards.css
└── pages/
    ├── login.css
    └── ficha.css
```

### 3. Navegación Funcional (Prioridad Alta)

**El menú en home.html está incompleto:**
```html
<!-- Actual - NO funciona -->
<li><a href="#">Catálogos</a></li>
<li><a href="#">Administración</a></li>

<!-- Sugerido -->
<nav>
  <li><a href="{% url 'home' %}">Inicio</a></li>
  <li class="dropdown">
    <a href="#">Catálogos</a>
    <ul>
      <li><a href="{% url 'ficha_tecnica:ficha_tecnica_list' %}">Fichas Técnicas</a></li>
      <li><a href="{% url 'investigacion:buscar_investigacion' %}">Investigaciones</a></li>
    </ul>
  </li>
  <li><a href="{% url 'admin:index' %}">Administración</a></li>
</nav>
```

### 4. Reutilización de Código (Prioridad Media)

| Componente | Archivos que lo duplican | Solución |
|------------|--------------------------|----------|
| Header/Topbar | Todos los templates de ficha | Crear `_header.html` |
| Tabla resultados | buscar.html, list.html | Mismo template con flag |
| Paginación | buscar_ficha_tecnica.html | Crear `_pagination.html` |
| Mensajes flash | formulario.html, detalle.html | Crear `_messages.html` |

### 5. Mejoras UX (Prioridad Media)

| Mejora | Descripción |
|--------|-------------|
| Breadcrumbs | Navegación "Inicio > Fichas > Detalle" |
| Loading states | Spinner mientras carga tabla grande |
| Responsive | Revisar tablas en móvil |
| Confirmaciones | Modal en vez de `confirm()` nativo |
| Filtros avanzados | Filtrar por estado, fecha, etc. |
| Acciones rápidas | "Nueva ficha" visible siempre |

### 6. Accesibilidad (Prioridad Media)

- Agregar `aria-label` a iconos/botones
- Contraste de colores suficiente
- `<label for="">` en todos los inputs
- Navegación por teclado en tablas

---

## Plan de Implementación Sugerido

### Fase 1 - Base (Recomendado primero)
1. Crear `templates/base.html` unificado
2. Crear `templates/partials/_navbar.html`
3. Crear `templates/partials/_messages.html`
4. Migrar todos los templates a usar `{% extends %}`

### Fase 2 - Navegación
1. Implementar menú funcional con dropdown
2. Agregar breadcrumbs

### Fase 3 - CSS
1. Consolidar CSS en estructura organizada
2. Definir variables de colores/spacing

### Fase 4 - UX
1. Agregar loading states
2. Mejorar responsive

---

## URLs Funcionales Actuales

| URL | Estado | Template |
|-----|--------|----------|
| `/auth/login/` | ✅ 200 | registration/login.html |
| `/home/` | ✅ 200 | home.html |
| `/ficha/` | ✅ 200 | fichatecnica_list.html |
| `/ficha/buscar/` | ✅ 200 | buscar_ficha_tecnica.html |
| `/ficha/cargar/` | ✅ 200 | formulario.html |
| `/ficha/<pk>/` | ✅ 200 | detalle_ficha_tecnica.html |
| `/ficha/<pk>/editar/` | ✅ 200 | editar_ficha_tecnica.html |
| `/investigacion/buscar/` | ✅ 200 | buscar_investigacion.html |
| `/investigacion/cargar/` | ✅ 200 | formulario.html |
| `/investigacion/<pk>/` | ✅ 200 | detalle_investigacion.html |
| `/admin/` | ⏳ Por verificar | Django Admin |

---

## Próximos Pasos

1. **Verificar admins de todas las apps** - Ver qué campos están configurados
2. **Probar admin nativo** - Confirmar que funciona post-cambios
3. **Usar admin como referencia** - Para mejorar flujo de usuario en frontend
4. **Implementar mejoras** - Según prioridad definida

---

## Notas

- Este documento se genera para no perder el análisis realizado
- Revisar antes de implementar cambios de frontend
- El admin de Django puede servir como modelo de UX para el frontend
