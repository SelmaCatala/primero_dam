# Bloque 04 - Esquemas esperados para TRUSTED y ANALYTICS

Este documento continúa los bloques 01, 02 y 03. Después de ejecutar el job de Glue Spark, se deben catalogar las salidas generadas en S3 para que puedan usarse en AWS Glue Data Quality y Amazon Athena.

## Tabla `oficinas_empleo_trusted_2025`

Ruta S3 esperada:

```text
s3://TU_BUCKET/trusted/oficinas/
```

Filas esperadas: **96**. Columnas esperadas: **19**.

| Columna | Tipo recomendado Glue/Athena | Comentario |
|---|---|---|
| registro_id | string | Identificador único mes-oficina |
| mes | string | Periodo `yyyy-MM` |
| oficina_id | string | Código de oficina |
| oficina | string | Nombre normalizado desde dimensión |
| provincia | string | Provincia corregida desde dimensión |
| comunidad_autonoma | string | Comunidad autónoma corregida |
| zona_operativa | string | Zona operativa corregida |
| canal_principal | string | Dominio: presencial, online, telefono |
| prioridad_media_expedientes | string | Dominio: alta, media, baja |
| expedientes_recibidos | int | Métrica operativa >= 0 |
| expedientes_resueltos | int | Métrica operativa >= 0 y <= recibidos |
| documentacion_pendiente | int | Métrica operativa >= 0 |
| incidencias_abiertas | int | Métrica operativa >= 0 |
| tiempo_medio_espera_min | double | Tiempo medio >= 0 |
| nivel_servicio | string | Dominio: alto, medio, bajo |
| satisfaccion_media | double | Rango de negocio 1 a 5 |
| tasa_resolucion_pct | double | KPI entre 0 y 100 |
| ratio_incidencias_pct | double | KPI >= 0 |
| riesgo_operativo | string | Dominio: alto, medio, bajo |

## Tabla `kpis_mensuales_por_oficina_2025`

Ruta S3 esperada:

```text
s3://TU_BUCKET/analytics/kpis_oficina/
```

Filas esperadas: **96**. Columnas esperadas: **14**.

Columnas: `mes, oficina_id, oficina, provincia, comunidad_autonoma, zona_operativa, expedientes_recibidos, expedientes_resueltos, documentacion_pendiente, incidencias_abiertas, tiempo_medio_espera_min, satisfaccion_media, tasa_resolucion_pct, ratio_incidencias_pct`.

## Tabla `kpis_mensuales_por_provincia_2025`

Ruta S3 esperada:

```text
s3://TU_BUCKET/analytics/kpis_provincia/
```

Filas esperadas: **48**. Columnas esperadas: **11**.

Columnas: `mes, provincia, comunidad_autonoma, expedientes_recibidos, expedientes_resueltos, documentacion_pendiente, incidencias_abiertas, tiempo_medio_espera_min, satisfaccion_media, tasa_resolucion_pct, ratio_incidencias_pct`.

## Tabla `resumen_ejecutivo_2025`

Ruta S3 esperada:

```text
s3://TU_BUCKET/analytics/resumen/
```

Filas esperadas: **1**. Columnas esperadas: **10**.

Columnas: `anio, oficinas_analizadas, provincias_analizadas, expedientes_recibidos_total, expedientes_resueltos_total, incidencias_abiertas_total, documentacion_pendiente_total, tasa_resolucion_global_pct, espera_media_global_min, satisfaccion_media_global`.

## Criterio de aceptación

La capa TRUSTED debe pasar calidad final. Las tablas ANALYTICS deben tener coherencia de filas, métricas no negativas y agregados compatibles con el resumen ejecutivo.
