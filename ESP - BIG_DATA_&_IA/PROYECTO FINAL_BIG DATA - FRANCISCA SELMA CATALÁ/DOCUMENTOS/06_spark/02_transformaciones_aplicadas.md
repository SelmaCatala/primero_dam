# Transformaciones aplicadas en el Bloque 03

## 1. Deduplicación

Se elimina el duplicado intencional de `registro_id`, pasando de 97 filas RAW a 96 filas TRUSTED.

## 2. Enriquecimiento territorial

Se realiza un `join` con `dim_oficinas_empleo` para usar la dimensión maestra como fuente de verdad de:

- `oficina`
- `provincia`
- `comunidad_autonoma`
- `zona_operativa`

Esto corrige la provincia nula existente en RAW.

## 3. Normalización numérica

Se castean y corrigen las métricas operativas:

- `expedientes_recibidos`
- `expedientes_resueltos`
- `documentacion_pendiente`
- `incidencias_abiertas`
- `tiempo_medio_espera_min`
- `satisfaccion_media`

Los negativos se normalizan a cero cuando no tienen sentido operativo.

## 4. Imputaciones controladas

- `expedientes_recibidos` nulo: se imputa como `expedientes_resueltos + documentacion_pendiente`, manteniendo coherencia mínima de negocio.
- `tiempo_medio_espera_min` nulo: se imputa con la media de la oficina y, si no existe, con media global.
- `satisfaccion_media` nula: se imputa a 3.0 como valor neutro.

## 5. Reglas de dominio

- `satisfaccion_media` queda acotada entre 1 y 5.
- `nivel_servicio` queda restringido a `alto`, `medio` o `bajo`; `excelente` se mapea a `alto`.
- `canal_principal` queda restringido a `presencial`, `online` o `telefono`.

## 6. Consistencia de negocio

Se garantiza que `expedientes_resueltos <= expedientes_recibidos` en la capa TRUSTED.

## 7. KPIs calculados

- `tasa_resolucion_pct = expedientes_resueltos / expedientes_recibidos * 100`
- `ratio_incidencias_pct = incidencias_abiertas / expedientes_recibidos * 100`
- `riesgo_operativo`: clasificación `alto`, `medio` o `bajo` según resolución, incidencias, espera, satisfacción y nivel de servicio.

## 8. Salidas generadas

- Capa TRUSTED limpia.
- KPIs mensuales por oficina.
- KPIs mensuales por provincia.
- Resumen ejecutivo anual.
