import os

# Importamos la base de datos y el servicio.
from db import NOMBRE_BASE_DATOS, inicializar_base_datos
from servicio import ServicioIncidencias


def mostrar_resultado_correcto(mensaje: str) -> None:
    """
    Muestra que una regla de negocio ha bloqueado
    correctamente una operación no permitida.
    """
    print(f"✅ PRUEBA SUPERADA: {mensaje}")


def mostrar_resultado_incorrecto(mensaje: str) -> None:
    """
    Muestra que una operación incorrecta no fue bloqueada.
    """
    print(f"❌ PRUEBA FALLIDA: {mensaje}")


def preparar_base_datos() -> None:
    """
    Crea la base de datos si todavía no existe.
    """
    if not os.path.exists(NOMBRE_BASE_DATOS):
        inicializar_base_datos()


def probar_titulo_vacio(
    servicio: ServicioIncidencias,
) -> None:
    """
    Comprueba que no se pueda crear una incidencia
    con el título vacío o formado solo por espacios.
    """

    print("\nPRUEBA 1: TÍTULO VACÍO")

    try:
        servicio.crear_incidencia(
            titulo="   ",
            descripcion="El equipo no funciona.",
            creada_por="usuario@empresa.com",
        )

        mostrar_resultado_incorrecto(
            "Se ha permitido crear una incidencia sin título."
        )

    except ValueError as error:
        mostrar_resultado_correcto(str(error))


def probar_correo_incorrecto(
    servicio: ServicioIncidencias,
) -> None:
    """
    Comprueba que no se pueda crear una incidencia
    con un correo que no contenga el carácter @.
    """

    print("\nPRUEBA 2: CORREO INCORRECTO")

    try:
        servicio.crear_incidencia(
            titulo="Fallo de red",
            descripcion="No hay conexión.",
            creada_por="usuario.empresa.com",
        )

        mostrar_resultado_incorrecto(
            "Se ha permitido utilizar un correo sin '@'."
        )

    except ValueError as error:
        mostrar_resultado_correcto(str(error))


def probar_incidencia_inexistente(
    servicio: ServicioIncidencias,
) -> None:
    """
    Comprueba que no se pueda asignar
    una incidencia que no existe.
    """

    print("\nPRUEBA 3: INCIDENCIA INEXISTENTE")

    tecnico = servicio.registrar_tecnico(
        nombre="Técnico de prueba",
        correo="tecnico_prueba@empresa.com",
    )

    try:
        servicio.asignar_incidencia(
            identificador_incidencia=9999,
            identificador_tecnico=tecnico.identificador,
        )

        mostrar_resultado_incorrecto(
            "Se ha permitido asignar una incidencia inexistente."
        )

    except ValueError as error:
        mostrar_resultado_correcto(str(error))


def probar_tecnico_inexistente(
    servicio: ServicioIncidencias,
) -> None:
    """
    Comprueba que no se pueda asignar una incidencia
    a un técnico que no existe.
    """

    print("\nPRUEBA 4: TÉCNICO INEXISTENTE")

    incidencia = servicio.crear_incidencia(
        titulo="Impresora bloqueada",
        descripcion="La impresora no responde.",
        creada_por="empleado@empresa.com",
    )

    try:
        servicio.asignar_incidencia(
            identificador_incidencia=incidencia.identificador,
            identificador_tecnico=9999,
        )

        mostrar_resultado_incorrecto(
            "Se ha permitido asignar un técnico inexistente."
        )

    except ValueError as error:
        mostrar_resultado_correcto(str(error))


def probar_cierre_sin_tecnico(
    servicio: ServicioIncidencias,
) -> None:
    """
    Comprueba que no se pueda cerrar una incidencia
    sin haberle asignado antes un técnico.
    """

    print("\nPRUEBA 5: CIERRE SIN TÉCNICO")

    incidencia = servicio.crear_incidencia(
        titulo="Pantalla azul",
        descripcion="El equipo se reinicia.",
        creada_por="usuario2@empresa.com",
    )

    try:
        servicio.cerrar_incidencia(
            incidencia.identificador
        )

        mostrar_resultado_incorrecto(
            "Se ha permitido cerrar una incidencia sin técnico."
        )

    except ValueError as error:
        mostrar_resultado_correcto(str(error))


def probar_doble_cierre(
    servicio: ServicioIncidencias,
) -> None:
    """
    Comprueba que una incidencia cerrada
    no pueda cerrarse una segunda vez.
    """

    print("\nPRUEBA 6: CERRAR DOS VECES")

    tecnico = servicio.registrar_tecnico(
        nombre="Técnico cierre",
        correo="tecnico_cierre@empresa.com",
    )

    incidencia = servicio.crear_incidencia(
        titulo="Error de acceso",
        descripcion="El usuario no puede iniciar sesión.",
        creada_por="usuario3@empresa.com",
    )

    servicio.asignar_incidencia(
        identificador_incidencia=incidencia.identificador,
        identificador_tecnico=tecnico.identificador,
    )

    servicio.cerrar_incidencia(
        incidencia.identificador
    )

    try:
        servicio.cerrar_incidencia(
            incidencia.identificador
        )

        mostrar_resultado_incorrecto(
            "Se ha permitido cerrar dos veces la misma incidencia."
        )

    except ValueError as error:
        mostrar_resultado_correcto(str(error))


def main() -> None:
    """
    Ejecuta todas las pruebas de reglas de negocio.
    """

    preparar_base_datos()

    servicio = ServicioIncidencias()

    print("=" * 70)
    print("PRUEBAS DE REGLAS DE NEGOCIO")
    print("=" * 70)

    probar_titulo_vacio(servicio)
    probar_correo_incorrecto(servicio)
    probar_incidencia_inexistente(servicio)
    probar_tecnico_inexistente(servicio)
    probar_cierre_sin_tecnico(servicio)
    probar_doble_cierre(servicio)

    print("\n" + "=" * 70)
    print("FIN DE LAS PRUEBAS")
    print("=" * 70)


if __name__ == "__main__":
    main()