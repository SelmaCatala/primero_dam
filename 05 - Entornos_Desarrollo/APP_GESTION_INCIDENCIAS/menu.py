from db import inicializar_base_datos
from servicio import ServicioIncidencias


def mostrar_titulo(texto: str) -> None:
    """
    Muestra un título separado con líneas.
    """
    print("\n" + "=" * 60)
    print(texto)
    print("=" * 60)


def pedir_numero(mensaje: str) -> int:
    """
    Solicita un número entero.

    Si la persona escribe letras u otro valor incorrecto,
    vuelve a pedirlo.
    """
    while True:
        texto = input(mensaje).strip()

        try:
            return int(texto)

        except ValueError:
            print("Debes escribir un número entero.")


def mostrar_tecnico(tecnico) -> None:
    """
    Muestra los datos principales de un técnico.
    """
    estado = "Activo" if tecnico.activo else "Inactivo"

    print(
        f"ID: {tecnico.identificador} | "
        f"Nombre: {tecnico.nombre} | "
        f"Correo: {tecnico.correo} | "
        f"Estado: {estado}"
    )


def mostrar_incidencia(incidencia) -> None:
    """
    Muestra los datos principales de una incidencia.
    """
    tecnico = incidencia.identificador_tecnico

    if tecnico is None:
        tecnico = "Sin asignar"

    print(
        f"ID: {incidencia.identificador} | "
        f"Título: {incidencia.titulo} | "
        f"Estado: {incidencia.estado.value} | "
        f"Técnico: {tecnico} | "
        f"Creada por: {incidencia.creada_por}"
    )


def mostrar_menu() -> None:
    """
    Muestra las opciones disponibles.
    """
    mostrar_titulo("GESTIÓN DE INCIDENCIAS")

    print("1. Registrar técnico")
    print("2. Listar técnicos")
    print("3. Crear incidencia")
    print("4. Listar todas las incidencias")
    print("5. Listar incidencias abiertas")
    print("6. Buscar incidencia por identificador")
    print("7. Asignar incidencia a un técnico")
    print("8. Cerrar incidencia")
    print("0. Salir")


def registrar_tecnico(servicio: ServicioIncidencias) -> None:
    """
    Solicita los datos de un técnico y lo registra.
    """
    mostrar_titulo("REGISTRAR TÉCNICO")

    nombre = input("Nombre: ")
    correo = input("Correo: ")

    tecnico = servicio.registrar_tecnico(
        nombre=nombre,
        correo=correo,
    )

    print("\nTécnico registrado correctamente:")
    mostrar_tecnico(tecnico)


def listar_tecnicos(servicio: ServicioIncidencias) -> None:
    """
    Muestra todos los técnicos registrados.
    """
    mostrar_titulo("LISTADO DE TÉCNICOS")

    tecnicos = servicio.obtener_todos_los_tecnicos()

    if not tecnicos:
        print("No hay técnicos registrados.")
        return

    for tecnico in tecnicos:
        mostrar_tecnico(tecnico)


def crear_incidencia(servicio: ServicioIncidencias) -> None:
    """
    Solicita los datos y crea una incidencia.
    """
    mostrar_titulo("CREAR INCIDENCIA")

    titulo = input("Título: ")
    descripcion = input("Descripción: ")
    creada_por = input("Correo de la persona creadora: ")

    incidencia = servicio.crear_incidencia(
        titulo=titulo,
        descripcion=descripcion,
        creada_por=creada_por,
    )

    print("\nIncidencia creada correctamente:")
    mostrar_incidencia(incidencia)


def listar_todas_las_incidencias(
    servicio: ServicioIncidencias,
) -> None:
    """
    Muestra todas las incidencias registradas.
    """
    mostrar_titulo("TODAS LAS INCIDENCIAS")

    incidencias = servicio.obtener_todas_las_incidencias()

    if not incidencias:
        print("No hay incidencias registradas.")
        return

    for incidencia in incidencias:
        mostrar_incidencia(incidencia)


def listar_incidencias_abiertas(
    servicio: ServicioIncidencias,
) -> None:
    """
    Muestra únicamente las incidencias abiertas.
    """
    mostrar_titulo("INCIDENCIAS ABIERTAS")

    incidencias = servicio.obtener_incidencias_abiertas()

    if not incidencias:
        print("No hay incidencias abiertas.")
        return

    for incidencia in incidencias:
        mostrar_incidencia(incidencia)


def buscar_incidencia(
    servicio: ServicioIncidencias,
) -> None:
    """
    Busca una incidencia mediante su identificador.
    """
    mostrar_titulo("BUSCAR INCIDENCIA")

    identificador = pedir_numero(
        "Identificador de la incidencia: "
    )

    incidencia = servicio.obtener_incidencia_por_identificador(
        identificador
    )

    if incidencia is None:
        print(
            f"No existe ninguna incidencia con ID {identificador}."
        )
        return

    mostrar_incidencia(incidencia)

    print(f"Descripción: {incidencia.descripcion}")


def asignar_incidencia(
    servicio: ServicioIncidencias,
) -> None:
    """
    Asigna una incidencia a un técnico.
    """
    mostrar_titulo("ASIGNAR INCIDENCIA")

    identificador_incidencia = pedir_numero(
        "Identificador de la incidencia: "
    )

    identificador_tecnico = pedir_numero(
        "Identificador del técnico: "
    )

    servicio.asignar_incidencia(
        identificador_incidencia=identificador_incidencia,
        identificador_tecnico=identificador_tecnico,
    )

    print("Incidencia asignada correctamente.")


def cerrar_incidencia(
    servicio: ServicioIncidencias,
) -> None:
    """
    Cierra una incidencia.
    """
    mostrar_titulo("CERRAR INCIDENCIA")

    identificador_incidencia = pedir_numero(
        "Identificador de la incidencia: "
    )

    servicio.cerrar_incidencia(
        identificador_incidencia=identificador_incidencia
    )

    print("Incidencia cerrada correctamente.")


def ejecutar_opcion(
    opcion: str,
    servicio: ServicioIncidencias,
) -> bool:
    """
    Ejecuta la opción elegida.

    Devuelve False cuando la persona desea salir.
    """
    if opcion == "1":
        registrar_tecnico(servicio)

    elif opcion == "2":
        listar_tecnicos(servicio)

    elif opcion == "3":
        crear_incidencia(servicio)

    elif opcion == "4":
        listar_todas_las_incidencias(servicio)

    elif opcion == "5":
        listar_incidencias_abiertas(servicio)

    elif opcion == "6":
        buscar_incidencia(servicio)

    elif opcion == "7":
        asignar_incidencia(servicio)

    elif opcion == "8":
        cerrar_incidencia(servicio)

    elif opcion == "0":
        print("\nAplicación finalizada.")
        return False

    else:
        print("\nOpción incorrecta. Elige una opción del menú.")

    return True


def main() -> None:
    """
    Inicializa la base de datos y mantiene el menú activo.
    """
    inicializar_base_datos()

    servicio = ServicioIncidencias()
    continuar = True

    while continuar:
        mostrar_menu()

        opcion = input("\nElige una opción: ").strip()

        try:
            continuar = ejecutar_opcion(
                opcion,
                servicio,
            )

        except ValueError as error:
            print(f"\nNo se pudo realizar la operación: {error}")

        except Exception as error:
            print(f"\nSe ha producido un error inesperado: {error}")

        if continuar:
            input("\nPulsa Intro para volver al menú...")


if __name__ == "__main__":
    main()