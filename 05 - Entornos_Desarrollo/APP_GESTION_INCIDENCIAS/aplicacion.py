import os

# Importamos el nombre de la base de datos y la función que crea las tablas.
from db import NOMBRE_BASE_DATOS, inicializar_base_datos

# Importamos la capa de servicio.
from servicio import ServicioIncidencias


def mostrar_separador() -> None:
    """
    Imprime una línea para separar visualmente cada bloque.
    """
    print("\n" + "=" * 70 + "\n")


def preparar_base_datos() -> None:
    """
    Crea la base de datos si todavía no existe.
    """

    if not os.path.exists(NOMBRE_BASE_DATOS):
        inicializar_base_datos()
        print("Base de datos creada correctamente.")
    else:
        print("La base de datos ya existe.")


def main() -> None:
    """
    Ejecuta una demostración completa de la aplicación.
    """

    # Paso 1: preparar SQLite.
    preparar_base_datos()
    mostrar_separador()

    # Paso 2: crear la capa de servicio.
    servicio = ServicioIncidencias()

    # Paso 3: registrar técnicos.
    print("REGISTRO DE TÉCNICOS")

    tecnico_1 = servicio.registrar_tecnico(
        "Ana García",
        "ana@empresa.com",
    )

    tecnico_2 = servicio.registrar_tecnico(
        "Luis Pérez",
        "luis@empresa.com",
    )

    print(tecnico_1)
    print(tecnico_2)

    mostrar_separador()

    # Paso 4: consultar técnicos.
    print("LISTADO DE TÉCNICOS")

    for tecnico in servicio.obtener_todos_los_tecnicos():
        print(tecnico)

    mostrar_separador()

    # Paso 5: crear incidencias.
    print("CREACIÓN DE INCIDENCIAS")

    incidencia_1 = servicio.crear_incidencia(
        titulo="Fallo en la red",
        descripcion="No hay conexión a Internet en la planta baja.",
        creada_por="usuario1@empresa.com",
    )

    incidencia_2 = servicio.crear_incidencia(
        titulo="Teclado averiado",
        descripcion="Varias teclas no responden.",
        creada_por="usuario2@empresa.com",
    )

    print(incidencia_1)
    print(incidencia_2)

    mostrar_separador()

    # Paso 6: consultar incidencias abiertas.
    print("INCIDENCIAS ABIERTAS")

    for incidencia in servicio.obtener_incidencias_abiertas():
        print(incidencia)

    mostrar_separador()

    # Paso 7: asignar un técnico.
    print("ASIGNACIÓN DE INCIDENCIA")

    servicio.asignar_incidencia(
        identificador_incidencia=incidencia_1.identificador,
        identificador_tecnico=tecnico_1.identificador,
    )

    incidencia_actualizada = (
        servicio.obtener_incidencia_por_identificador(
            incidencia_1.identificador
        )
    )

    print(incidencia_actualizada)

    mostrar_separador()

    # Paso 8: cerrar la incidencia asignada.
    print("CIERRE DE INCIDENCIA")

    servicio.cerrar_incidencia(
        incidencia_1.identificador
    )

    incidencia_cerrada = (
        servicio.obtener_incidencia_por_identificador(
            incidencia_1.identificador
        )
    )

    print(incidencia_cerrada)

    mostrar_separador()

    # Paso 9: mostrar todas las incidencias.
    print("LISTADO FINAL DE INCIDENCIAS")

    for incidencia in servicio.obtener_todas_las_incidencias():
        print(incidencia)


if __name__ == "__main__":
    main()