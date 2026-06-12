# Mapeo de nombres de tablas en Athena y ficheros CSV

Durante la ejecución del laboratorio, AWS Glue generó nombres de tablas basados en los prefijos de S3.

| Capa | Fichero CSV canónico | Ruta S3 | Tabla usada en Athena durante el laboratorio |
|---|---|---|---|
| RAW | oficinas_empleo_operativo_raw_2025.csv | raw/oficinas/ | oficinas |
| TRUSTED | oficinas_empleo_trusted_2025.csv | trusted/oficinas/ | trusted_oficinas |
| ANALYTICS oficina | kpis_mensuales_por_oficina_2025.csv | analytics/kpis_oficina/ | analytics_kpis_oficina |
| ANALYTICS provincia | kpis_mensuales_por_provincia_2025.csv | analytics/kpis_provincia/ | analytics_kpis_provincia |
| ANALYTICS resumen | resumen_ejecutivo_2025.csv | analytics/resumen/ | analytics_resumen |

Los nombres largos con sufijo 2025 se conservan como nombres de ficheros y nombres canónicos documentales. Las consultas SQL incluidas en esta carpeta usan los nombres reales de Athena indicados en la memoria.
