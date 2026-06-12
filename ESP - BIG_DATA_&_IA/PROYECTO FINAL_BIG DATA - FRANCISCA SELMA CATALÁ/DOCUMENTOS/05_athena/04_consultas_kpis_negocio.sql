-- BLOQUE 05 - Consultas de KPIs de negocio en Amazon Athena
-- Objetivo: responder preguntas de negocio del proyecto de oficinas de empleo.

USE proyecto_bigdata_oficinas;

-- 1. Resumen ejecutivo anual.
SELECT *
FROM analytics_resumen;

-- 2. Ranking anual de carga por oficina.
SELECT
    oficina_id,
    oficina,
    provincia,
    SUM(expedientes_recibidos) AS expedientes_recibidos_total,
    SUM(expedientes_resueltos) AS expedientes_resueltos_total,
    SUM(incidencias_abiertas) AS incidencias_abiertas_total,
    ROUND(SUM(expedientes_resueltos) * 100.0 / SUM(expedientes_recibidos), 2) AS tasa_resolucion_pct,
    ROUND(SUM(incidencias_abiertas) * 100.0 / SUM(expedientes_recibidos), 2) AS ratio_incidencias_pct,
    ROUND(AVG(tiempo_medio_espera_min), 1) AS espera_media_min,
    ROUND(AVG(satisfaccion_media), 2) AS satisfaccion_media
FROM trusted_oficinas
GROUP BY oficina_id, oficina, provincia
ORDER BY expedientes_recibidos_total DESC;

-- 3. Oficinas con peor tasa de resolución.
SELECT
    oficina_id,
    oficina,
    provincia,
    SUM(expedientes_recibidos) AS expedientes_recibidos_total,
    SUM(expedientes_resueltos) AS expedientes_resueltos_total,
    ROUND(SUM(expedientes_resueltos) * 100.0 / SUM(expedientes_recibidos), 2) AS tasa_resolucion_pct,
    ROUND(AVG(tiempo_medio_espera_min), 1) AS espera_media_min,
    ROUND(AVG(satisfaccion_media), 2) AS satisfaccion_media
FROM trusted_oficinas
GROUP BY oficina_id, oficina, provincia
ORDER BY tasa_resolucion_pct ASC;

-- 4. Oficinas con mayor riesgo operativo.
SELECT
    oficina_id,
    oficina,
    provincia,
    COUNT_IF(riesgo_operativo = 'alto') AS meses_riesgo_alto,
    COUNT_IF(riesgo_operativo = 'medio') AS meses_riesgo_medio,
    COUNT_IF(riesgo_operativo = 'bajo') AS meses_riesgo_bajo,
    ROUND(AVG(tasa_resolucion_pct), 2) AS tasa_resolucion_media_pct,
    ROUND(AVG(ratio_incidencias_pct), 2) AS ratio_incidencias_medio_pct,
    ROUND(AVG(tiempo_medio_espera_min), 1) AS espera_media_min,
    ROUND(AVG(satisfaccion_media), 2) AS satisfaccion_media
FROM trusted_oficinas
GROUP BY oficina_id, oficina, provincia
ORDER BY meses_riesgo_alto DESC, espera_media_min DESC;

-- 5. KPIs agregados por provincia.
SELECT
    provincia,
    comunidad_autonoma,
    SUM(expedientes_recibidos) AS expedientes_recibidos_total,
    SUM(expedientes_resueltos) AS expedientes_resueltos_total,
    SUM(incidencias_abiertas) AS incidencias_abiertas_total,
    SUM(documentacion_pendiente) AS documentacion_pendiente_total,
    ROUND(SUM(expedientes_resueltos) * 100.0 / SUM(expedientes_recibidos), 2) AS tasa_resolucion_pct,
    ROUND(SUM(incidencias_abiertas) * 100.0 / SUM(expedientes_recibidos), 2) AS ratio_incidencias_pct,
    ROUND(AVG(tiempo_medio_espera_min), 1) AS espera_media_min,
    ROUND(AVG(satisfaccion_media), 2) AS satisfaccion_media
FROM analytics_kpis_provincia
GROUP BY provincia, comunidad_autonoma
ORDER BY expedientes_recibidos_total DESC;

-- 6. Evolución mensual de KPIs por provincia.
SELECT
    mes,
    provincia,
    expedientes_recibidos,
    expedientes_resueltos,
    tasa_resolucion_pct,
    incidencias_abiertas,
    ratio_incidencias_pct,
    tiempo_medio_espera_min,
    satisfaccion_media
FROM analytics_kpis_provincia
ORDER BY mes, provincia;

-- 7. Relación entre incidencias, espera y satisfacción.
SELECT
    oficina_id,
    oficina,
    provincia,
    ROUND(AVG(ratio_incidencias_pct), 2) AS ratio_incidencias_medio_pct,
    ROUND(AVG(tiempo_medio_espera_min), 1) AS espera_media_min,
    ROUND(AVG(satisfaccion_media), 2) AS satisfaccion_media
FROM trusted_oficinas
GROUP BY oficina_id, oficina, provincia
ORDER BY ratio_incidencias_medio_pct DESC, espera_media_min DESC;

-- 8. Meses con peor comportamiento operativo.
SELECT
    mes,
    COUNT_IF(riesgo_operativo = 'alto') AS oficinas_en_riesgo_alto,
    ROUND(AVG(tasa_resolucion_pct), 2) AS tasa_resolucion_media_pct,
    ROUND(AVG(tiempo_medio_espera_min), 1) AS espera_media_min,
    ROUND(AVG(satisfaccion_media), 2) AS satisfaccion_media
FROM trusted_oficinas
GROUP BY mes
ORDER BY oficinas_en_riesgo_alto DESC, espera_media_min DESC;
