# Esquemas esperados tras la catalogación

## Tabla RAW: oficinas_empleo_raw_2025

Columnas esperadas: 16.

| Campo | Tipo lógico recomendado | Comentario |
|---|---|---|
| registro_id | string | Identificador de registro mes-oficina |
| mes | string | Formato `yyyy-MM` |
| oficina_id | string | Clave de oficina |
| oficina | string | Nombre de oficina |
| provincia | string | Puede contener nulos en RAW |
| comunidad_autonoma | string | Territorio |
| zona_operativa | string | Segmentación operativa |
| canal_principal | string | `presencial`, `online`, `telefono` |
| prioridad_media_expedientes | string | `alta`, `media`, `baja` |
| expedientes_recibidos | double/int | Contiene un nulo intencional en RAW |
| expedientes_resueltos | int | Contiene valor negativo y casos mayores que recibidos |
| documentacion_pendiente | int | Métrica operativa |
| incidencias_abiertas | int | Contiene un valor negativo intencional |
| tiempo_medio_espera_min | double | Contiene un nulo intencional |
| nivel_servicio | string | Contiene categoría inválida `excelente` |
| satisfaccion_media | double | Debe estar entre 1 y 5; hay un valor fuera de rango |

## Tabla dim_oficinas_empleo

Columnas esperadas: 8. Debe usarse después para corregir provincia, comunidad autónoma y zona operativa.

## Tabla dim_calendario_2025

Columnas esperadas: 6. Debe usarse después para enriquecer el análisis mensual y trimestral.

## Revisión técnica

Si Glue infiere algún tipo como `string` en una columna numérica, no bloquea el proyecto. Para Data Quality puede ser más cómodo usar la tabla generada por crawler si infiere tipos numéricos. Para Athena se podrá crear una tabla externa controlada en el bloque SQL.
