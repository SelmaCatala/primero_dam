# Modelo de datos recomendado en Power BI

## Tablas a importar

1. `kpis_mensuales_por_oficina_2025`
   - Tabla principal del dashboard.
   - Granularidad: una fila por mes y oficina.
   - Uso: KPIs, tendencias, ranking de oficinas, filtros territoriales.

2. `kpis_mensuales_por_provincia_2025`
   - Tabla agregada por mes y provincia.
   - Uso: validacion y visuales territoriales agregados.
   - No es imprescindible si todo se calcula desde la tabla de oficina, pero aporta evidencia analitica.

3. `resumen_ejecutivo_2025`
   - Una fila de resumen anual.
   - Uso: contraste de valores globales.

4. `oficinas_empleo_trusted_2025`
   - Tabla limpia de detalle.
   - Uso: analisis de riesgo operativo por oficina y validacion final.

## Relaciones recomendadas

Para mantener el modelo sencillo en laboratorio, se puede trabajar con tablas independientes y medidas sobre la tabla `kpis_mensuales_por_oficina_2025`.

Si se crean relaciones, usar:

- `kpis_mensuales_por_oficina_2025[mes]` -> `kpis_mensuales_por_provincia_2025[mes]` no es recomendable como relacion directa porque genera muchos-a-muchos.
- Es mejor crear una dimension calendario en Power BI o usar `dim_calendario_2025.csv` si se importa desde `01_raw`.
- Para defensa academica, es suficiente explicar que la capa analytics ya viene preparada desde AWS.

## Columnas calculadas utiles

En la tabla `kpis_mensuales_por_oficina_2025`:

```DAX
Anio = VALUE(LEFT('kpis_mensuales_por_oficina_2025'[mes], 4))
Mes Numero = VALUE(RIGHT('kpis_mensuales_por_oficina_2025'[mes], 2))
Mes Orden = 'kpis_mensuales_por_oficina_2025'[Anio] * 100 + 'kpis_mensuales_por_oficina_2025'[Mes Numero]
Mes Nombre = FORMAT(DATE('kpis_mensuales_por_oficina_2025'[Anio], 'kpis_mensuales_por_oficina_2025'[Mes Numero], 1), "MMM")
```

Ordenar `Mes Nombre` por `Mes Orden` si se usa en graficos temporales.

## Recomendacion de rendimiento

Usar preferentemente la capa `analytics/` para graficos. Evitar construir visuales pesados sobre `raw/`, porque el dato raw contiene errores intencionales y no debe ser la fuente de negocio.
