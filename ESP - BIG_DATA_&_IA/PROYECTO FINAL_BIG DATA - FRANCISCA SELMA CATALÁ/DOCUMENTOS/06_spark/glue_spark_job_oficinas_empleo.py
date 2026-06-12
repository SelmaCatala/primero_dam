"""
AWS Glue Spark Job - Proyecto Final Big Data AWS: Oficinas de empleo
Ruta B Batch: RAW -> TRUSTED -> ANALYTICS

Objetivo:
- Leer datos RAW y dimensiones desde Amazon S3.
- Corregir errores detectados en Glue Data Quality RAW.
- Generar capa TRUSTED y salidas ANALYTICS listas para Athena y Power BI.

Parametros del job en AWS Glue:
--RAW_PATH s3://TU_BUCKET/raw/oficinas/oficinas_empleo_operativo_raw_2025.csv
--DIM_OFICINAS_PATH s3://TU_BUCKET/raw/dimensiones/dim_oficinas/dim_oficinas_empleo.csv
--DIM_CALENDARIO_PATH s3://TU_BUCKET/raw/dimensiones/dim_calendario/dim_calendario_2025.csv
--TRUSTED_PATH s3://TU_BUCKET/trusted/oficinas/
--ANALYTICS_OFICINA_PATH s3://TU_BUCKET/analytics/kpis_oficina/
--ANALYTICS_PROVINCIA_PATH s3://TU_BUCKET/analytics/kpis_provincia/
--ANALYTICS_RESUMEN_PATH s3://TU_BUCKET/analytics/resumen/

Notas de ejecucion:
- Usar LabRole en AWS Academy.
- Recomendado: Glue 4.0 o Glue 5.0 segun disponibilidad del laboratorio.
- El script escribe CSV con cabecera para facilitar Athena y Power BI en contexto academico.
- En produccion se recomienda Parquet + particionado para optimizar Athena.
"""

import sys
from awsglue.utils import getResolvedOptions
from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import (
    avg,
    coalesce,
    col,
    countDistinct,
    greatest,
    lit,
    lower,
    round,
    sum as spark_sum,
    trim,
    when,
)

args = getResolvedOptions(
    sys.argv,
    [
        "RAW_PATH",
        "DIM_OFICINAS_PATH",
        "DIM_CALENDARIO_PATH",
        "TRUSTED_PATH",
        "ANALYTICS_OFICINA_PATH",
        "ANALYTICS_PROVINCIA_PATH",
        "ANALYTICS_RESUMEN_PATH",
    ],
)

spark = SparkSession.builder.appName("ProyectoFinalBigDataOficinasEmpleo").getOrCreate()
spark.conf.set("spark.sql.session.timeZone", "UTC")

# -----------------------------------------------------------------------------
# 1. Lectura de datos de entrada
# -----------------------------------------------------------------------------
raw = spark.read.option("header", "true").option("inferSchema", "false").csv(args["RAW_PATH"])
dim_oficinas = spark.read.option("header", "true").option("inferSchema", "false").csv(args["DIM_OFICINAS_PATH"])
dim_calendario = spark.read.option("header", "true").option("inferSchema", "false").csv(args["DIM_CALENDARIO_PATH"])

# -----------------------------------------------------------------------------
# 2. Preparacion de dimensiones maestras
# -----------------------------------------------------------------------------
dim = dim_oficinas.select(
    col("oficina_id").alias("dim_oficina_id"),
    col("oficina").alias("dim_oficina"),
    col("provincia").alias("dim_provincia"),
    col("comunidad_autonoma").alias("dim_comunidad_autonoma"),
    col("zona_operativa").alias("dim_zona_operativa"),
)

cal = dim_calendario.select(
    col("mes").alias("cal_mes"),
    col("anio").cast("int").alias("anio"),
)

# -----------------------------------------------------------------------------
# 3. Deduplicacion y enriquecimiento con maestro de oficinas
# -----------------------------------------------------------------------------
base = raw.dropDuplicates(["registro_id"]).join(
    dim,
    raw["oficina_id"] == dim["dim_oficina_id"],
    "left",
)

# Se prioriza la dimension maestra frente al campo RAW para estabilizar territorios.
base = (
    base
    .withColumn("oficina", coalesce(col("dim_oficina"), col("oficina"), lit("Oficina no informada")))
    .withColumn("provincia", coalesce(col("dim_provincia"), col("provincia"), lit("Provincia no informada")))
    .withColumn("comunidad_autonoma", coalesce(col("dim_comunidad_autonoma"), col("comunidad_autonoma"), lit("Comunidad no informada")))
    .withColumn("zona_operativa", coalesce(col("dim_zona_operativa"), col("zona_operativa"), lit("Zona no informada")))
)

# -----------------------------------------------------------------------------
# 4. Normalizacion de tipos y dominios
# -----------------------------------------------------------------------------
clean = (
    base
    .withColumn("canal_principal", lower(trim(col("canal_principal"))))
    .withColumn("prioridad_media_expedientes", lower(trim(col("prioridad_media_expedientes"))))
    .withColumn("nivel_servicio", lower(trim(col("nivel_servicio"))))
    .withColumn("expedientes_recibidos_raw", col("expedientes_recibidos").cast("int"))
    .withColumn("expedientes_resueltos", col("expedientes_resueltos").cast("int"))
    .withColumn("documentacion_pendiente", col("documentacion_pendiente").cast("int"))
    .withColumn("incidencias_abiertas", col("incidencias_abiertas").cast("int"))
    .withColumn("tiempo_medio_espera_min", col("tiempo_medio_espera_min").cast("double"))
    .withColumn("satisfaccion_media", col("satisfaccion_media").cast("double"))
    .withColumn("expedientes_resueltos", when(col("expedientes_resueltos").isNull() | (col("expedientes_resueltos") < 0), 0).otherwise(col("expedientes_resueltos")))
    .withColumn("documentacion_pendiente", when(col("documentacion_pendiente").isNull() | (col("documentacion_pendiente") < 0), 0).otherwise(col("documentacion_pendiente")))
    .withColumn("incidencias_abiertas", when(col("incidencias_abiertas").isNull() | (col("incidencias_abiertas") < 0), 0).otherwise(col("incidencias_abiertas")))
    .withColumn(
        "expedientes_recibidos",
        when(
            col("expedientes_recibidos_raw").isNull() | (col("expedientes_recibidos_raw") < 0),
            greatest(col("expedientes_resueltos") + col("documentacion_pendiente"), lit(0)),
        ).otherwise(col("expedientes_recibidos_raw")),
    )
    .withColumn("expedientes_resueltos", when(col("expedientes_resueltos") > col("expedientes_recibidos"), col("expedientes_recibidos")).otherwise(col("expedientes_resueltos")))
    .withColumn("canal_principal", when(col("canal_principal").isin("presencial", "online", "telefono"), col("canal_principal")).otherwise("presencial"))
    .withColumn("prioridad_media_expedientes", when(col("prioridad_media_expedientes").isin("alta", "media", "baja"), col("prioridad_media_expedientes")).otherwise("media"))
    .withColumn("nivel_servicio", when(col("nivel_servicio") == "excelente", "alto").otherwise(col("nivel_servicio")))
    .withColumn("nivel_servicio", when(col("nivel_servicio").isin("alto", "medio", "bajo"), col("nivel_servicio")).otherwise("medio"))
    .withColumn("satisfaccion_media", when(col("satisfaccion_media").isNull(), 3.0).when(col("satisfaccion_media") > 5, 5.0).when(col("satisfaccion_media") < 1, 1.0).otherwise(col("satisfaccion_media")))
)

# -----------------------------------------------------------------------------
# 5. Imputacion de tiempo de espera nulo
# -----------------------------------------------------------------------------
w_oficina = Window.partitionBy("oficina_id")
clean = clean.withColumn("media_espera_oficina", avg("tiempo_medio_espera_min").over(w_oficina))
global_wait = clean.select(avg("tiempo_medio_espera_min").alias("global_wait")).first()["global_wait"]
clean = clean.withColumn(
    "tiempo_medio_espera_min",
    round(coalesce(col("tiempo_medio_espera_min"), col("media_espera_oficina"), lit(global_wait), lit(0.0)), 1),
)

# -----------------------------------------------------------------------------
# 6. Indicadores de calidad operativa y clasificacion de riesgo
# -----------------------------------------------------------------------------
trusted = (
    clean
    .withColumn(
        "tasa_resolucion_pct",
        when(col("expedientes_recibidos") > 0, round((col("expedientes_resueltos") / col("expedientes_recibidos")) * 100, 2)).otherwise(0.0),
    )
    .withColumn(
        "ratio_incidencias_pct",
        when(col("expedientes_recibidos") > 0, round((col("incidencias_abiertas") / col("expedientes_recibidos")) * 100, 2)).otherwise(0.0),
    )
    .withColumn(
        "riesgo_operativo",
        when(
            (col("tasa_resolucion_pct") < 80)
            | (col("ratio_incidencias_pct") > 5)
            | (col("tiempo_medio_espera_min") > 55)
            | (col("nivel_servicio") == "bajo"),
            "alto",
        ).when(
            (col("tasa_resolucion_pct") < 90)
            | (col("ratio_incidencias_pct") > 3)
            | (col("tiempo_medio_espera_min") > 40)
            | (col("satisfaccion_media") < 3),
            "medio",
        ).otherwise("bajo"),
    )
    .select(
        "registro_id",
        "mes",
        "oficina_id",
        "oficina",
        "provincia",
        "comunidad_autonoma",
        "zona_operativa",
        "canal_principal",
        "prioridad_media_expedientes",
        "expedientes_recibidos",
        "expedientes_resueltos",
        "documentacion_pendiente",
        "incidencias_abiertas",
        "tiempo_medio_espera_min",
        "nivel_servicio",
        "satisfaccion_media",
        "tasa_resolucion_pct",
        "ratio_incidencias_pct",
        "riesgo_operativo",
    )
)

# -----------------------------------------------------------------------------
# 7. Escritura capa TRUSTED
# -----------------------------------------------------------------------------
trusted.coalesce(1).write.mode("overwrite").option("header", "true").csv(args["TRUSTED_PATH"])

# -----------------------------------------------------------------------------
# 8. Capa ANALYTICS por oficina
# -----------------------------------------------------------------------------
kpis_oficina = (
    trusted.groupBy("mes", "oficina_id", "oficina", "provincia", "comunidad_autonoma", "zona_operativa")
    .agg(
        spark_sum("expedientes_recibidos").alias("expedientes_recibidos"),
        spark_sum("expedientes_resueltos").alias("expedientes_resueltos"),
        spark_sum("documentacion_pendiente").alias("documentacion_pendiente"),
        spark_sum("incidencias_abiertas").alias("incidencias_abiertas"),
        round(avg("tiempo_medio_espera_min"), 1).alias("tiempo_medio_espera_min"),
        round(avg("satisfaccion_media"), 2).alias("satisfaccion_media"),
    )
    .withColumn("tasa_resolucion_pct", when(col("expedientes_recibidos") > 0, round((col("expedientes_resueltos") / col("expedientes_recibidos")) * 100, 2)).otherwise(0.0))
    .withColumn("ratio_incidencias_pct", when(col("expedientes_recibidos") > 0, round((col("incidencias_abiertas") / col("expedientes_recibidos")) * 100, 2)).otherwise(0.0))
)

# -----------------------------------------------------------------------------
# 9. Capa ANALYTICS por provincia
# -----------------------------------------------------------------------------
kpis_provincia = (
    trusted.groupBy("mes", "provincia", "comunidad_autonoma")
    .agg(
        spark_sum("expedientes_recibidos").alias("expedientes_recibidos"),
        spark_sum("expedientes_resueltos").alias("expedientes_resueltos"),
        spark_sum("documentacion_pendiente").alias("documentacion_pendiente"),
        spark_sum("incidencias_abiertas").alias("incidencias_abiertas"),
        round(avg("tiempo_medio_espera_min"), 1).alias("tiempo_medio_espera_min"),
        round(avg("satisfaccion_media"), 2).alias("satisfaccion_media"),
    )
    .withColumn("tasa_resolucion_pct", when(col("expedientes_recibidos") > 0, round((col("expedientes_resueltos") / col("expedientes_recibidos")) * 100, 2)).otherwise(0.0))
    .withColumn("ratio_incidencias_pct", when(col("expedientes_recibidos") > 0, round((col("incidencias_abiertas") / col("expedientes_recibidos")) * 100, 2)).otherwise(0.0))
)

# -----------------------------------------------------------------------------
# 10. Resumen ejecutivo anual. Se usa dim_calendario para obtener anio.
# -----------------------------------------------------------------------------
trusted_cal = trusted.join(cal, trusted["mes"] == cal["cal_mes"], "left")

resumen = (
    trusted_cal.groupBy("anio")
    .agg(
        countDistinct("oficina_id").alias("oficinas_analizadas"),
        countDistinct("provincia").alias("provincias_analizadas"),
        spark_sum("expedientes_recibidos").alias("expedientes_recibidos_total"),
        spark_sum("expedientes_resueltos").alias("expedientes_resueltos_total"),
        spark_sum("incidencias_abiertas").alias("incidencias_abiertas_total"),
        spark_sum("documentacion_pendiente").alias("documentacion_pendiente_total"),
        round(avg("tiempo_medio_espera_min"), 1).alias("espera_media_global_min"),
        round(avg("satisfaccion_media"), 2).alias("satisfaccion_media_global"),
    )
    .withColumn("tasa_resolucion_global_pct", when(col("expedientes_recibidos_total") > 0, round((col("expedientes_resueltos_total") / col("expedientes_recibidos_total")) * 100, 2)).otherwise(0.0))
    .select(
        "anio",
        "oficinas_analizadas",
        "provincias_analizadas",
        "expedientes_recibidos_total",
        "expedientes_resueltos_total",
        "incidencias_abiertas_total",
        "documentacion_pendiente_total",
        "tasa_resolucion_global_pct",
        "espera_media_global_min",
        "satisfaccion_media_global",
    )
)

kpis_oficina.coalesce(1).write.mode("overwrite").option("header", "true").csv(args["ANALYTICS_OFICINA_PATH"])
kpis_provincia.coalesce(1).write.mode("overwrite").option("header", "true").csv(args["ANALYTICS_PROVINCIA_PATH"])
resumen.coalesce(1).write.mode("overwrite").option("header", "true").csv(args["ANALYTICS_RESUMEN_PATH"])

spark.stop()
