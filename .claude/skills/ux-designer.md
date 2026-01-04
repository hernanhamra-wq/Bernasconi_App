---
name: ux-designer-museo
description: Evaluador UX especializado para sistemas de gestión de museo. Audita usabilidad, flujos de trabajo y experiencia de usuario para conservadores, catalogadores y administradores de colecciones.
---

# UX Designer - Gestión de Museo

Skill para evaluar y mejorar la experiencia de usuario en aplicaciones de gestión museística.

## Cuándo usar este skill

Invocar cuando el usuario mencione: "evaluar UX", "mejorar usabilidad", "revisar diseño", "flujo de usuario", "hacer más fácil de usar".

## Fases de Auditoría UX

### FASE 1: Auditoría General
- Inspección visual de interfaces
- Testing de interacciones
- Análisis de flujos de usuario
- Consistencia visual entre pantallas

### FASE 2: Flujos Específicos de Museo
Evaluar eficiencia de tareas críticas:
- **Búsqueda de obra**: ¿Cuántos clics para encontrar una ficha técnica?
- **Alta de obra nueva**: ¿El formulario es claro? ¿Campos obligatorios visibles?
- **Consulta de estado**: ¿Se ve rápido el estado de conservación?
- **Historial de movimientos**: ¿Es fácil rastrear ubicaciones anteriores?
- **Registro de intervenciones**: ¿Flujo intuitivo para conservadores?

### FASE 3: Usabilidad para Roles
Considerar diferentes usuarios:
- **Conservador**: Necesita acceso rápido a estado, materiales, intervenciones
- **Catalogador**: Necesita formularios eficientes, campos claros
- **Investigador**: Necesita búsqueda avanzada, exportación de datos
- **Administrador**: Necesita dashboards, reportes, visión general

### FASE 4: Accesibilidad
- Navegación por teclado
- Contraste de colores (WCAG AA)
- Etiquetas ARIA
- Tamaño de fuentes legible
- Mensajes de error claros

### FASE 5: Eficiencia Visual
- **Jerarquía visual**: ¿Lo importante se ve primero?
- **Densidad de información**: ¿Muy cargado o muy vacío?
- **Escaneo rápido**: ¿Se puede encontrar info sin leer todo?
- **Agrupación lógica**: ¿Datos relacionados están juntos?

### FASE 6: Feedback al Usuario
- Estados de carga visibles
- Confirmaciones de acciones
- Mensajes de error útiles
- Estados vacíos informativos

## Formato de Reporte

Generar reporte con:

```
## Auditoría UX - BernasconiApp

### Puntuación General
- Funcionalidad: X/10
- Diseño Visual: X/10
- Usabilidad: X/10
- Accesibilidad: X/10
- Eficiencia de Flujos: X/10
- **TOTAL: XX/50** (Grado: A-F)

### Problemas Críticos (bloquean uso)
1. [Problema] - [Archivo:línea] - [Solución]

### Problemas Importantes (dificultan uso)
1. [Problema] - [Archivo:línea] - [Solución]

### Mejoras Recomendadas (optimización)
1. [Mejora] - [Beneficio esperado]

### Flujos de Museo - Evaluación
| Tarea | Clics actuales | Clics óptimos | Estado |
|-------|----------------|---------------|--------|
| Buscar obra | X | Y | OK/Mejorar |
| Alta de obra | X | Y | OK/Mejorar |
| Ver estado conservación | X | Y | OK/Mejorar |
```

## Principios de UX para Museo

1. **Acceso rápido a lo frecuente**: Las tareas diarias deben ser inmediatas
2. **Información en contexto**: No obligar a navegar para ver datos relacionados
3. **Búsqueda poderosa**: Los usuarios buscan más de lo que navegan
4. **Minimalismo funcional**: Solo mostrar lo necesario para cada tarea
5. **Consistencia**: Mismos patrones en toda la aplicación
6. **Recuperación de errores**: Fácil deshacer y corregir
