-- BLOQUE 04 - Validaciones SQL opcionales para TRUSTED y ANALYTICS en Amazon Athena
-- Consultas alineadas con los nombres reales generados por Glue Crawler en el laboratorio.

USE proyecto_bigdata_oficinas;

-- 1. Volumetría esperada en trusted: 96 filas.
SELECT COUNT(*) AS filas_trusted
FROM trusted_oficinas;

-- 2. Registro_id único.
SELECT registro_id, COUNT(*) AS repeticiones
FROM trusted_oficinas
GROUP BY registro_id
HAVING COUNT(*) > 1;

-- 3. Campos clave no nulos.
SELECT COUNT(*) AS registros_con_nulos_clave
FROM trusted_oficinas
WHERE registro_id IS NULL
   OR mes IS NULL
   OR oficina_id IS NULL
   OR oficina IS NULL
   OR provincia IS NULL
   OR expedientes_recibidos IS NULL
   OR expedientes_resueltos IS NULL
   OR tiempo_medio_espera_min IS NULL;

-- 4. Métricas no negativas.
SELECT COUNT(*) AS registros_con_metricas_negativas
FROM trusted_oficinas
WHERE expedientes_recibidos < 0
   OR expedientes_resueltos < 0
   OR documentacion_pendiente < 0
   OR incidencias_abiertas < 0
   OR tiempo_medio_espera_min < 0;

-- 5. Regla cruzada de negocio: resueltos no debe superar recibidos.
SELECT COUNT(*) AS registros_resueltos_mayor_recibidos
FROM trusted_oficinas
WHERE expedientes_resueltos > expedientes_recibidos;

-- 6. Dominios funcionales controlados.
SELECT
  SUM(CASE WHEN nivel_servicio NOT IN ('alto','medio','bajo') THEN 1 ELSE 0 END) AS nivel_servicio_invalido,
  SUM(CASE WHEN canal_principal NOT IN ('presencial','online','telefono') THEN 1 ELSE 0 END) AS canal_invalido,
  SUM(CASE WHEN riesgo_operativo NOT IN ('alto','medio','bajo') THEN 1 ELSE 0 END) AS riesgo_invalido,
  SUM(CASE WHEN satisfaccion_media < 1 OR satisfaccion_media > 5 THEN 1 ELSE 0 END) AS satisfaccion_fuera_rango
FROM trusted_oficinas;

-- 7. Volumetría de capas analytics.
SELECT 'kpis_oficina' AS tabla, COUNT(*) AS filas FROM analytics_kpis_oficina
UNION ALL
SELECT 'kpis_provincia' AS tabla, COUNT(*) AS filas FROM analytics_kpis_provincia
UNION ALL
SELECT 'resumen' AS tabla, COUNT(*) AS filas FROM analytics_resumen;

-- 8. Coherencia entre el resumen anual y la agregación de la tabla analytics por provincia.
SELECT
  r.expedientes_recibidos_total AS resumen_recibidos,
  SUM(p.expedientes_recibidos) AS analytics_provincia_recibidos,
  r.expedientes_resueltos_total AS resumen_resueltos,
  SUM(p.expedientes_resueltos) AS analytics_provincia_resueltos
FROM analytics_resumen r
CROSS JOIN analytics_kpis_provincia p
GROUP BY r.expedientes_recibidos_total, r.expedientes_resueltos_total;
