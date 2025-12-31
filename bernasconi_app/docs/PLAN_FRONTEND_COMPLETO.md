# Plan Completo de Frontend - BernasconiApp

**Fecha:** 2025-12-31
**Estado:** Documento de planificación

---

## 1. Análisis de Páginas Actuales y Correcciones

### 1.1 auth/login/ - Página de Login

**Estado actual:** Funcional, diseño aceptable

**Problemas detectados:**
- No tiene opción de "Olvidé contraseña"
- No indica requisitos de contraseña
- Label dice "Correo Electrónico" pero acepta username

**Campos del modelo Usuario:**
| Campo | En página | Estado |
|-------|-----------|--------|
| username | ✅ | OK |
| password | ✅ | OK |
| email | ❌ | No se usa para login |

**Sugerencias:**
- Cambiar label a "Usuario o Email"
- Agregar link "¿Olvidaste tu contraseña?"
- Agregar mensaje de bienvenida más cálido

---

### 1.2 home/ - Página Principal

**Estado actual:** Funcional pero incompleto

**Problemas detectados:**
- Menú con links rotos (`href="#"`)
- No muestra información útil
- No tiene accesos rápidos a funciones principales

**Sugerencias:**
- Agregar dashboard con estadísticas:
  - Total de fichas: 7,739
  - Investigaciones: 6
  - Fichas con seguimiento
  - Obras en cuarentena
- Menú funcional con dropdowns
- Accesos rápidos: "Nueva Ficha", "Buscar", "Admin"

---

### 1.3 investigacion/cargar/ - Formulario de Investigación

**Estado actual:** Problemas de contraste

**Problemas detectados:**
- Fondo con imagen hace difícil leer
- Contraste insuficiente (texto blanco sobre fondo claro)
- Labels blancos sobre glass effect translúcido
- DIVs no cerrados correctamente en HTML (líneas 51, 57, 64, 72, 78, 85)

**Campos del modelo Investigacion:**
| Campo | En formulario | Estado |
|-------|---------------|--------|
| investigacion_id | ✅ (auto) | OK |
| ficha | ✅ | OK |
| investigador | ✅ | OK |
| num_investigacion | ✅ | OK |
| titulo_investigacion | ✅ | OK |
| detalle_investigacion | ✅ | OK |
| anio_realizacion | ✅ | OK |

**Todos los campos están presentes.**

**Correcciones CSS necesarias:**
```css
/* Problema actual */
.field label {
  color: rgba(255,255,255,0.85);  /* Blanco sobre fondo claro = mal contraste */
}

/* Solución */
.field label {
  color: #1a1a1a;  /* Texto oscuro */
  text-shadow: none;
}

/* O agregar fondo oscuro al glass */
.glass {
  background: rgba(30, 30, 30, 0.85);  /* Fondo oscuro */
}
```

---

### 1.4 investigacion/buscar/ - Búsqueda de Investigaciones

**Estado actual:** Funcional, mismo problema de contraste

**Campos mostrados en tabla:**
| Campo | Mostrado | Estado |
|-------|----------|--------|
| investigacion_id | ✅ | OK |
| ficha | ✅ | OK |
| num_investigacion | ✅ | OK |
| titulo_investigacion | ✅ | OK |
| anio_realizacion | ✅ | OK |
| investigador | ✅ | OK |

**Todos los campos relevantes están presentes.**

---

### 1.5 ficha/cargar/ - Formulario de Ficha Técnica

**Estado actual:** Funcional, faltan campos nuevos

**Campos del modelo FichaTecnica vs Formulario:**

| Sección | Campo | En form | Prioridad |
|---------|-------|---------|-----------|
| **Identificación** | n_de_ficha | ✅ | - |
| | inventario | ✅ | - |
| | n_de_inventario_anterior | ✅ | - |
| **Descripción** | titulo | ✅ | - |
| | descripcion | ✅ | - |
| | observacion | ✅ | - |
| | anio | ✅ | - |
| **Estado** | estado_conservacion | ❌ | Alta |
| | fk_estado_funcional | ✅ | - |
| | seguimiento | ✅ | - |
| **Ejemplar** | tipo_ejemplar | ❌ | Media |
| | edicion | ❌ | Media |
| | series_legacy | ✅ | - |
| **Dimensiones** | dimensiones | ✅ | - |
| | ancho/alto/diametro/profundidad | ✅ | - |
| **Relaciones** | fk_responsable_carga | ✅ | - |
| | fk_taller | ✅ | - |
| | fk_procedencia | ✅ | - |
| | fk_multimedia_principal | ✅ | - |
| | materiales | ✅ | - |
| | autores | ❌ | Alta |
| **Dublin Core** | categoria_objeto | ❌ | Alta |
| | periodo_historico | ❌ | Media |
| | datacion | ❌ | Media |
| | origen_geografico | ❌ | Media |
| | tematica | ❌ | Media |
| | palabras_clave | ❌ | Media |
| **Conservación** | temperatura_min/max | ❌ | Baja |
| | humedad_min/max | ❌ | Baja |
| | nivel_iluminacion | ❌ | Baja |
| | requiere_vitrina | ❌ | Baja |
| | condiciones_especiales | ❌ | Baja |
| **Legal** | propietario_legal | ❌ | Media |
| | tipo_propiedad | ❌ | Media |
| | derechos_reproduccion | ❌ | Baja |
| | nivel_confidencialidad | ❌ | Baja |

**Campos faltantes críticos:**
1. `autores` (ManyToMany) - Muy importante
2. `estado_conservacion` (Choice) - Importante
3. `categoria_objeto` (Choice) - Dublin Core
4. `tipo_ejemplar` / `edicion` - Clasificación

---

### 1.6 ficha/buscar/ - Búsqueda de Fichas

**Estado actual:** Funcional

**Campos mostrados:**
| Campo | Mostrado | Sugerencia |
|-------|----------|------------|
| id | ✅ | OK |
| imagen | ✅ | OK |
| inventario | ✅ | OK |
| titulo | ✅ | OK |
| anio | ✅ | OK |
| fk_estado_funcional | ✅ | OK |
| seguimiento | ✅ | OK |
| fecha_de_carga | ✅ | OK |

**Sugerencias:**
- Agregar filtros avanzados (por estado, año, categoría)
- Mostrar autor principal
- Mostrar estado_conservacion

---

### 1.7 ficha/<pk>/ - Detalle de Ficha

**Estado actual:** Funcional, faltan campos nuevos

**Campos mostrados vs disponibles:**
- Muestra: ID, N°Ficha, Inventario, Año, Estado, Responsable, Seguimiento, Fecha
- Falta: Autores, Categoría, Conservación, Dublin Core, Legal

---

### 1.8 Páginas faltantes (404)

| URL | Estado | Necesita |
|-----|--------|----------|
| `/investigacion/` | 404 | Agregar vista listado o redirect |
| `/ficha/<pk>/editar/` | ? | Verificar |

---

## 2. Sistema de Modo Claro/Oscuro

### 2.1 Implementación con CSS Variables

```css
/* static/css/theme.css */

:root {
  /* Modo claro (default) */
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --bg-card: #ffffff;
  --text-primary: #1a1a1a;
  --text-secondary: #666666;
  --text-muted: #999999;
  --border-color: #e0e0e0;
  --accent-color: #14a096;
  --accent-hover: #0d7d75;
  --shadow: rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] {
  /* Modo oscuro */
  --bg-primary: #1a1a1a;
  --bg-secondary: #2d2d2d;
  --bg-card: #333333;
  --text-primary: #e9eef5;
  --text-secondary: #b0b0b0;
  --text-muted: #808080;
  --border-color: #404040;
  --accent-color: #20c4b8;
  --accent-hover: #14a096;
  --shadow: rgba(0, 0, 0, 0.3);
}

/* Aplicar variables */
body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

.card {
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 8px var(--shadow);
}

.btn-primary {
  background-color: var(--accent-color);
}
```

### 2.2 Toggle Button

```html
<!-- En navbar -->
<button id="theme-toggle" class="theme-toggle" aria-label="Cambiar tema">
  <span class="icon-sun">☀️</span>
  <span class="icon-moon">🌙</span>
</button>
```

```javascript
// static/js/theme.js
const toggle = document.getElementById('theme-toggle');
const html = document.documentElement;

// Cargar preferencia guardada o del sistema
const savedTheme = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const theme = savedTheme || (prefersDark ? 'dark' : 'light');
html.setAttribute('data-theme', theme);

toggle.addEventListener('click', () => {
  const current = html.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});
```

---

## 3. Asesoría de Diseño Frontend

### 3.1 ¿Qué puedo hacer por vos?

| Aspecto | Nivel de ayuda | Descripción |
|---------|----------------|-------------|
| **Estructura HTML** | Alto | Layouts, semántica, accesibilidad |
| **CSS/Estilos** | Alto | Variables, componentes, responsive |
| **UX/Flujos** | Alto | Navegación, formularios, feedback |
| **Paleta de colores** | Medio-Alto | Combinaciones, contraste, accesibilidad |
| **Tipografía** | Medio | Jerarquía, legibilidad |
| **Iconografía** | Medio | Sugerir librerías (Heroicons, Lucide) |
| **Animaciones** | Medio | Transiciones sutiles, microinteracciones |
| **Imágenes/Assets** | Bajo | No puedo crear imágenes, solo optimizar |

### 3.2 Principios de Diseño Recomendados

**Para un sistema de museo:**

1. **Claridad sobre decoración**
   - Fondos neutros (blanco/gris claro o gris oscuro)
   - Dejar que las imágenes de obras sean protagonistas
   - Evitar backgrounds con fotos que compitan

2. **Jerarquía visual**
   - Títulos claros y grandes
   - Espaciado generoso
   - Agrupación lógica de campos

3. **Consistencia**
   - Mismos colores de botones en toda la app
   - Mismo estilo de cards/tablas
   - Navegación predecible

4. **Feedback al usuario**
   - Estados de hover claros
   - Mensajes de éxito/error visibles
   - Loading states

5. **Accesibilidad**
   - Contraste mínimo 4.5:1 para texto
   - Focus visible para navegación por teclado
   - Labels asociados a inputs

### 3.3 Paleta de Colores Sugerida

```css
/* Paleta institucional museo */
:root {
  /* Primarios */
  --museo-verde: #14a096;      /* Actual - mantener */
  --museo-verde-dark: #0d7d75;

  /* Neutros */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-500: #6b7280;
  --gray-700: #374151;
  --gray-900: #111827;

  /* Estados */
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
  --info: #3b82f6;
}
```

---

## 4. Páginas a Desarrollar

### 4.1 Prioridad Alta (Core del sistema)

| # | Página | URL | Descripción |
|---|--------|-----|-------------|
| 1 | **Dashboard** | `/home/` | Mejorar con estadísticas y accesos rápidos |
| 2 | **Ficha - Formulario completo** | `/ficha/cargar/` | Agregar campos faltantes (autores, Dublin Core) |
| 3 | **Ficha - Detalle completo** | `/ficha/<pk>/` | Mostrar todos los campos organizados |
| 4 | **Ficha - Editar** | `/ficha/<pk>/editar/` | Verificar que funcione correctamente |
| 5 | **Investigación - Arreglar contraste** | `/investigacion/cargar/` | CSS fix urgente |

### 4.2 Prioridad Media (Funcionalidad completa)

| # | Página | URL | Descripción |
|---|--------|-----|-------------|
| 6 | Listado de Autores | `/autor/` | CRUD de autores |
| 7 | Listado de Materiales | `/material/` | CRUD de materiales |
| 8 | Ubicaciones - Listado | `/ubicacion/` | Ver todas las ubicaciones |
| 9 | Ubicaciones - Mapa/Vista | `/ubicacion/mapa/` | Vista espacial del museo |
| 10 | Movimientos - Registrar | `/movimiento/nuevo/` | Registrar traslado de obra |
| 11 | Movimientos - Historial | `/movimiento/historial/` | Ver historial de movimientos |
| 12 | Plagas - Registro | `/plaga/registrar/` | Cargar detección de plaga |
| 13 | Plagas - Listado | `/plaga/` | Ver registros de plagas |

### 4.3 Prioridad Baja (Módulos secundarios)

| # | Página | URL | Descripción |
|---|--------|-----|-------------|
| 14 | Préstamos - Listado | `/prestamo/` | Ver préstamos activos |
| 15 | Préstamos - Nuevo | `/prestamo/nuevo/` | Solicitar préstamo |
| 16 | Préstamos - Workflow | `/prestamo/<pk>/` | Gestionar estados |
| 17 | Donaciones - Listado | `/donacion/` | Ver donaciones |
| 18 | Instituciones | `/institucion/` | CRUD instituciones |
| 19 | Multimedia - Galería | `/multimedia/` | Ver archivos |
| 20 | Reportes - Dashboard | `/reportes/` | Estadísticas avanzadas |
| 21 | Reportes - Exportar | `/reportes/exportar/` | CSV, PDF |
| 22 | Usuarios - Gestión | `/usuarios/` | Admin de usuarios (solo superadmin) |

### 4.4 Componentes Reutilizables a Crear

| Componente | Uso |
|------------|-----|
| `_navbar.html` | Navegación global |
| `_sidebar.html` | Menú lateral (opcional) |
| `_breadcrumbs.html` | Navegación jerárquica |
| `_pagination.html` | Paginador reutilizable |
| `_messages.html` | Alertas/notificaciones |
| `_card.html` | Contenedor de contenido |
| `_table.html` | Tabla con estilos |
| `_modal.html` | Diálogos modales |
| `_form_field.html` | Campo de formulario estilizado |
| `_search_bar.html` | Barra de búsqueda |
| `_theme_toggle.html` | Botón modo claro/oscuro |

---

## 5. Plan de Implementación

### Fase 1: Correcciones Urgentes (Inmediato)
1. ✅ Corregir errores 500 en vistas (HECHO)
2. ⏳ Arreglar contraste en investigacion/cargar/
3. ⏳ Cerrar DIVs mal cerrados en HTML
4. ⏳ Agregar URL para `/investigacion/` (redirect a buscar)

### Fase 2: Base de Diseño (1-2 días)
1. Crear `base.html` unificado
2. Crear sistema de variables CSS
3. Implementar modo claro/oscuro
4. Crear navbar funcional

### Fase 3: Formularios Completos (2-3 días)
1. Agregar campos faltantes a ficha técnica
2. Organizar en fieldsets/secciones
3. Implementar selector de autores (inline)

### Fase 4: Páginas Nuevas (según necesidad)
- Desarrollar según prioridad definida

---

## 6. Próximos Pasos Inmediatos

1. **Arreglar contraste investigacion** - CSS fix
2. **Agregar ruta /investigacion/** - Redirect
3. **Crear base.html unificado**
4. **Implementar dark mode**

¿Por cuál empezamos?
