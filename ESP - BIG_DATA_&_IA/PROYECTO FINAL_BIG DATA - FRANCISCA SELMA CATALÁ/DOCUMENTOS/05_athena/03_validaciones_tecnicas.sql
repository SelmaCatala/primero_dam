-- BLOQUE 05 - Validaciones técnicas en Amazon Athena
-- Ejecutar después de catalogar trusted y analytics.
-- Consultas alineadas con los nombres reales generados por Glue Crawler en el laboratorio.

USE proyecto_bigdata_oficinas;

-- 1. Conteo de filas de la capa trusted. Esperado: 96.
SELECT COUNT(*) AS filas_trusted
FROM trusted_oficinas;

-- 2. Conteo de filas de analytics por oficina. Esperado: 96.
SELECT COUNT(*) AS filas_kpis_oficina
FROM analytics_kpis_oficina;

-- 3. Conteo de filas de analytics por provincia. Esperado: 48.
SELECT COUNT(*) AS filas_kpis_provincia
FROM analytics_kpis_provincia;

-- 4. Conteo de filas del resumen ejecutivo. Esperado: 1.
SELECT COUNT(*) AS filas_resumen
FROM analytics_resumen;

-- 5. Verificación de duplicados. Esperado: 0 filas devueltas.
SELECT registro_id, COUNT(*) AS repeticiones
FROM trusted_oficinas
GROUP BY registro_id
HAVING COUNT(*) > 1;

-- 6. Verificación de nulos en campos clave. Esperado: 0.
SELECT COUNT(*) AS registros_con_nulos_clave
FROM trusted_oficinas
WHERE registro_id IS NULL
   OR mes IS NULL
   OR oficina_id IS NULL
   OR oficina IS NULL
   OR provincia IS NULL
   OR expedientes_recibidos IS NULL
   OR expedientes_resueltos IS NULL;

-- 7. Verificación de métricas negativas. Esperado: 0.
SELECT COUNT(*) AS registros_con_metricas_negativas
FROM trusted_oficinas
WHERE expedientes_recibidos < 0
   OR expedientes_resueltos < 0
   OR documentacion_pendiente < 0
   OR incidencias_abiertas < 0
   OR tiempo_medio_espera_min < 0;

-- 8. Validación de satisfacción en escala de negocio 1-5. Esperado: 0.
SELECT COUNT(*) AS registros_satisfaccion_fuera_rango
FROM trusted_oficinas
WHERE satisfaccion_media < 1
   OR satisfaccion_media > 5;

-- 9. Validación de dominios controlados. Esperado: 0.
SELECT COUNT(*) AS registros_con_dominios_invalidos
FROM trusted_oficinas
WHERE nivel_servicio NOT IN ('alto', 'medio', 'bajo')
   OR canal_principal NOT IN ('presencial', 'online', 'telefono')
   OR prioridad_media_expedientes NOT IN ('alta', 'media', 'baja')
   OR riesgo_operativo NOT IN ('alto', 'medio', 'bajo');

-- 10. Validación de coherencia de negocio. Esperado: 0.
SELECT COUNT(*) AS registros_resueltos_mayores_que_recibidos
FROM trusted_oficinas
WHERE expedientes_resueltos > expedientes_recibidos;

-- 11. Validación de tasas. Esperado: 0.
SELECT COUNT(*) AS registros_tasa_resolucion_invalida
FROM trusted_oficinas
WHERE tasa_resolucion_pct < 0
   OR tasa_resolucion_pct > 100;

-- 12. Resumen de control técnico para captura.
SELECT
    COUNT(*) AS filas,
    COUNT(DISTINCT registro_id) AS registros_unicos,
    COUNT(DISTINCT oficina_id) AS oficinas,
    COUNT(DISTINCT provincia) AS provincias,
    SUM(expedientes_recibidos) AS expedientes_recibidos_total,
    SUM(expedientes_resueltos) AS expedientes_resueltos_total,
    ROUND(SUM(expedientes_resueltos) * 100.0 / SUM(expedientes_recibidos), 2) AS tasa_resolucion_global_pct,
    ROUND(AVG(tiempo_medio_espera_min), 1) AS espera_media_global_min,
    ROUND(AVG(satisfaccion_media), 2) AS satisfaccion_media_global
FROM trusted_oficinas;
