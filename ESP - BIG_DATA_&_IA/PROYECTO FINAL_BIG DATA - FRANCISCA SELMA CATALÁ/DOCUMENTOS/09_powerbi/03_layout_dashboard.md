# Diseño recomendado del dashboard Power BI

## Pagina 1 - Resumen ejecutivo operativo

Objetivo: ofrecer una vision rapida del estado operativo anual y mensual.

### Filtros superiores

- Mes
- Provincia
- Oficina
- Zona operativa

### Tarjetas KPI

1. Expedientes recibidos
2. Expedientes resueltos
3. Tasa de resolucion %
4. Espera media min
5. Satisfaccion media
6. Incidencias abiertas

### Visuales principales

1. Line chart: `mes` frente a `Tasa Resolucion %` y `Espera Media Min`.
2. Bar chart: `provincia` frente a `Total Expedientes Recibidos`.
3. Bar chart: `oficina` frente a `Tasa Resolucion %`, orden ascendente para ver peor rendimiento.
4. Matrix: oficina, provincia, recibidos, resueltos, tasa, incidencias, espera, satisfaccion.

## Pagina 2 - Analisis de riesgo y calidad operativa

Objetivo: identificar oficinas prioritarias.

### Visuales recomendados

1. Scatter plot: eje X = `Espera Media Min`, eje Y = `Satisfaccion Media`, tamaño = `Incidencias Abiertas`, leyenda = provincia.
2. Bar chart: oficina frente a `Meses Riesgo Alto` si se importa la tabla trusted.
3. Bar chart: provincia frente a `Ratio Incidencias %`.
4. Tabla de detalle por oficina con meses de riesgo alto, medio y bajo.

## Pagina 3 opcional - Validacion y trazabilidad

Objetivo: demostrar que el dashboard consume datos preparados.

Visuales simples:

- Tabla con valores globales de resumen ejecutivo.
- Tabla con conteos de filas por dataset si se quiere incluir como evidencia.
- Texto explicativo: "Los datos provienen de la capa analytics generada con Glue Spark y validada con Glue Data Quality y Athena".

## Criterios de diseno

- No sobrecargar con demasiados visuales.
- Usar titulos orientados a negocio, no nombres tecnicos de columnas.
- Mantener filtros visibles.
- Mostrar los KPIs clave en la parte superior.
- No usar Power BI para corregir errores del raw; las correcciones pertenecen al pipeline AWS.
