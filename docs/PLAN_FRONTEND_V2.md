# PLAN FRONTEND V2 - Respuestas y Plan de Implementación

## Respuestas a tus consultas

### 1. FONDO DE PANTALLA EN HOME + DARK MODE

**Situación actual:**
- El dark mode está implementado con **CSS Variables + JavaScript**
- El JS guarda la preferencia en `localStorage` para persistir entre sesiones
- Las imágenes disponibles: `edificio.jpg`, `edificio2.jpg`, `frente_museo.png`

**Solución para dark mode con fondo:**
```css
/* Light mode: imagen normal */
.home-bg { background-image: url('/static/img/edificio.jpg'); }

/* Dark mode: misma imagen con overlay oscuro */
[data-theme="dark"] .home-bg {
  background-image:
    linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
    url('/static/img/edificio.jpg');
}
```
Esto mantiene la misma imagen pero la oscurece con un gradiente superpuesto.

---

### 2. FICHA TÉCNICA - MEJORAS NECESARIAS

#### 2a. MATERIALES - Selector mejorado
**Problema:** Lista enorme de checkboxes
**Solución propuesta:**
- Select2 con búsqueda y agrupación por tipo
- Selector en cascada: primero TIPO → luego MATERIAL (alfabético)
- Botón "+ Agregar material" para múltiples
- Poder agregar detalle/técnica a cada material

**Implementación:**
```
[Tipo de Material ▼] [Material ▼] [Detalle] [+ Agregar]

Materiales agregados:
✕ Madera - Cedro (tallado)
✕ Metal - Bronce (fundido)
```

#### 2b. UBICACIÓN ACTUAL
**Ya existe en el modelo:**
- `apps_ubicacion/reg_ubicacion_actual/` - Ubicación actual
- `apps_ubicacion/reg_historial_mov/` - Historial de movimientos
- `apps_ubicacion/ubicacion_lugar/` - Catálogo de lugares
- `apps_ubicacion/contenedor_ubicacion/` - Contenedores

**El modelo FichaTecnica ya tiene el método:**
```python
def ubicacion_actual(self):
    # Retorna último movimiento COMPLETADO
```

**Falta:** Crear la UI para:
1. Mostrar ubicación actual en la ficha
2. Botón "Registrar movimiento" → crea entrada en historial
3. Estados: EN_TRANSITO, EN_CUARENTENA, EXHIBIDO, ALMACENADO

#### 2c. BOTONES DE ACCIONES EN FICHA
**Agregar en detalle_ficha_tecnica.html:**
```
[Generar Informe PDF] [Nueva Intervención] [Registrar Movimiento]
[Nueva Investigación] [Registrar Préstamo] [Subir Multimedia]
```

#### 2d. BORRADO DE FICHAS
**Opciones:**
1. **Soft delete (recomendado):** Agregar campo `activo = BooleanField(default=True)` y filtrar en queries
2. **Hard delete:** Solo para SuperAdmin con confirmación doble

**Implementación recomendada:** Soft delete con:
- Estado `ACTIVO`, `OCULTO`, `ANULADO`
- Las fichas anuladas no aparecen en búsquedas normales
- SuperAdmin puede ver y restaurar

#### 2e. FOTOS Y MULTIMEDIA
**Ya existe:** `catalogo_multimedia` vinculado a `FichaTecnica`
- `fk_multimedia_principal` - Imagen principal
- `imagen` - Campo directo en ficha
- Tabla `CatalogoMultimedia` para múltiples archivos

**Falta:** UI para agregar múltiples fotos desde la ficha

---

### 3. PANEL DE ADMINISTRADOR

**Respuesta:** Sí, Django Admin es bastante intuitivo para no-programadores.

**Panel restringido por roles:**
```python
# Ya existe en Usuario:
ROLE_CHOICES = [
    (SUPERADMIN, 'SuperAdmin'),  # TODO
    (ADMIN, 'Admin'),             # CRUD catálogos + gestión fichas
    (GUEST, 'Guest'),             # Solo lectura
]
```

**Implementación:**
- SuperAdmin: Acceso total + configuración sistema + usuarios
- Admin: CRUD catálogos + gestión fichas/préstamos/donaciones
- Guest: Solo visualización

Se puede crear un "Admin simplificado" custom si el Django Admin resulta complejo.

---

### 4. FONDOS DE PANTALLA POR SECCIÓN

| Sección | Imagen sugerida | Dark mode |
|---------|----------------|-----------|
| Home/Dashboard | edificio.jpg | + overlay 60% negro |
| Fichas Técnicas | mesa1.jpg - mesa9.jpg | + overlay 60% negro |
| Investigaciones | mesa6.jpg | + overlay 60% negro |
| Ubicaciones | edificio2.jpg | + overlay 60% negro |
| Login | frente_museo.png | + overlay 50% negro |

---

### 5. ORDENAMIENTO EN LISTADOS

**Implementar en todas las tablas:**
```
┌─────────────────────────────────────────────────┐
│ ID ▲▼ │ Título ▲▼ │ Año ▲▼ │ Estado ▲▼ │ ...  │
└─────────────────────────────────────────────────┘
```
- Click en header → ordena ASC
- Segundo click → ordena DESC
- Iconos: ▲ (ASC), ▼ (DESC), ▲▼ (no ordenado)

---

### 6. CAMPOS FALTANTES EN VER FICHA

**Dublin Core (ya en modelo, falta en template):**
- categoria_objeto
- periodo_historico
- datacion
- origen_geografico
- tematica
- palabras_clave

**Conservación (ya en modelo, falta en template):**
- temperatura_requerida_min/max
- humedad_requerida_min/max
- nivel_iluminacion
- requiere_vitrina
- condiciones_especiales

**Propiedad Legal (ya en modelo, falta en template):**
- propietario_legal
- tipo_propiedad
- derechos_reproduccion
- nivel_confidencialidad

**Relaciones (falta mostrar):**
- Autores (M2M)
- Ubicación actual (método)
- Investigaciones vinculadas
- Intervenciones vinculadas
- Préstamos/Donaciones

---

### 7. CATÁLOGOS Y CRUDs FALTANTES

#### CRUDs a crear (frontend):

| Catálogo | Modelo existe | CRUD UI | Permisos |
|----------|--------------|---------|----------|
| Materiales | ✅ | ❌ Crear | Admin+ |
| Tipo Material | ✅ (campo tipo) | ❌ Crear | Admin+ |
| Ubicaciones/Lugares | ✅ | ❌ Crear | Admin+ |
| Contenedores | ✅ | ❌ Crear | Admin+ |
| Autores | ✅ | ❌ Crear | Admin+ |
| Procedencias | ✅ | ❌ Crear | Admin+ |
| Estados de Obra | ✅ | ❌ Crear | Admin+ |
| Talleres | ✅ | ❌ Crear | Admin+ |
| Usuarios | ✅ | ❌ Crear | SuperAdmin |
| Instituciones | ✅ | ❌ Crear | Admin+ |
| Tipos de Plaga | ✅ | ❌ Crear | Admin+ |

#### Gestiones a crear:

| Gestión | Modelo existe | UI | Permisos |
|---------|--------------|-----|----------|
| Préstamos | ✅ Prestamo | ❌ Crear | Admin+ |
| Donaciones | ✅ Donacion | ❌ Crear | Admin+ |
| Intervenciones | ✅ Intervencion | ❌ Crear | Admin+ |
| Seguimiento Xilófagos | ✅ | ❌ Crear | Admin+ |
| Historial Movimientos | ✅ | ❌ Crear | Admin+ |
| Multimedia | ✅ | ❌ Crear | Admin+ |

---

### 8. SISTEMA DE PERMISOS

```python
# Decorador para vistas
@role_required(['superadmin', 'admin'])
def mi_vista(request):
    pass

# En templates
{% if user.role == 'superadmin' %}
  <a href="{% url 'usuarios:list' %}">Gestionar Usuarios</a>
{% endif %}
```

| Funcionalidad | Guest | Admin | SuperAdmin |
|--------------|-------|-------|------------|
| Ver fichas | ✅ | ✅ | ✅ |
| Crear/Editar fichas | ❌ | ✅ | ✅ |
| Eliminar fichas | ❌ | ❌ | ✅ |
| Ver catálogos | ✅ | ✅ | ✅ |
| CRUD catálogos | ❌ | ✅ | ✅ |
| Gestionar usuarios | ❌ | ❌ | ✅ |
| Config. sistema | ❌ | ❌ | ✅ |

---

### 9. PÁGINAS NUEVAS PROPUESTAS

1. **Dashboard mejorado**
   - Estadísticas en tiempo real
   - Obras en tránsito / cuarentena
   - Alertas de conservación
   - Préstamos próximos a vencer

2. **Gestión de Préstamos**
   - Listado con filtros por estado
   - Formulario de solicitud
   - Seguimiento de estados

3. **Gestión de Donaciones**
   - Registro de nuevas donaciones
   - Documentación adjunta

4. **Control de Ubicaciones**
   - Mapa visual (opcional)
   - Registro rápido de movimientos
   - Obras en cuarentena

5. **Seguimiento de Plagas**
   - Registro de detecciones
   - Seguimiento de tratamientos
   - Alertas

6. **Reportes/Informes**
   - Generar PDF de ficha completa
   - Exportar listados a Excel
   - Estadísticas

7. **Gestión de Usuarios** (SuperAdmin)
   - CRUD usuarios
   - Asignar roles
   - Historial de actividad

---

## ORDEN DE IMPLEMENTACIÓN SUGERIDO

### FASE 1 - Mejoras inmediatas (1-2 días)
1. ✅ Fondo de pantalla en home con dark mode
2. ✅ Completar campos en detalle_ficha_tecnica
3. ✅ Agregar botones de acciones
4. ✅ Ordenamiento en tablas

### FASE 2 - Selector de materiales (1 día)
1. Rediseñar selector con dropdown por tipo
2. Permitir múltiples materiales con detalle

### FASE 3 - CRUDs catálogos (2-3 días)
1. Template base para CRUD
2. Materiales, Autores, Ubicaciones
3. Procedencias, Estados, Talleres

### FASE 4 - Gestiones (3-4 días)
1. Préstamos (listado, crear, detalle)
2. Donaciones
3. Intervenciones
4. Movimientos/Ubicaciones

### FASE 5 - Permisos y seguridad (1-2 días)
1. Implementar decoradores
2. Filtrar en templates
3. Panel de usuarios

### FASE 6 - Reportes (2-3 días)
1. PDF de ficha completa
2. Exportar a Excel
3. Dashboard con estadísticas reales
