from typing import List, Optional

# Importamos las clases del dominio.
from modelos import EstadoIncidencia, Incidencia, Tecnico

# Importamos los repositorios que acceden a la base de datos.
from repositorio import RepositorioIncidencias, RepositorioTecnicos


class ServicioIncidencias:
    """
    Contiene las reglas de negocio de la aplicación.

    Esta clase coordina los repositorios y decide
    si una operación está permitida o no.
    """

    def __init__(self) -> None:
        """
        Crea los repositorios que utilizará el servicio.
        """
        self.repositorio_tecnicos = RepositorioTecnicos()
        self.repositorio_incidencias = RepositorioIncidencias()

    # ============================================================
    # OPERACIONES RELACIONADAS CON TÉCNICOS
    # ============================================================

    def registrar_tecnico(
        self,
        nombre: str,
        correo: str,
    ) -> Tecnico:
        """
        Registra un técnico nuevo.

        Antes de guardarlo, comprueba que el nombre
        y el correo tengan contenido.
        """

        if not nombre or not nombre.strip():
            raise ValueError(
                "El nombre del técnico no puede estar vacío."
            )

        if not correo or not correo.strip():
            raise ValueError(
                "El correo del técnico no puede estar vacío."
            )

        if "@" not in correo:
            raise ValueError(
                "El correo del técnico debe contener '@'."
            )

        tecnico = Tecnico(
            identificador=None,
            nombre=nombre.strip(),
            correo=correo.strip(),
            activo=True,
        )

        return self.repositorio_tecnicos.crear(tecnico)

    def obtener_todos_los_tecnicos(self) -> List[Tecnico]:
        """
        Devuelve todos los técnicos registrados.
        """
        return self.repositorio_tecnicos.obtener_todos()

    # ============================================================
    # OPERACIONES RELACIONADAS CON INCIDENCIAS
    # ============================================================

    def crear_incidencia(
        self,
        titulo: str,
        descripcion: str,
        creada_por: str,
    ) -> Incidencia:
        """
        Crea una incidencia nueva con estado ABIERTA.

        Aplica las reglas de negocio antes de guardarla.
        """

        # Regla 1: el título no puede estar vacío.
        if not titulo or not titulo.strip():
            raise ValueError(
                "El título de la incidencia no puede estar vacío."
            )

        # Regla 2: el correo del creador debe contener @.
        if not creada_por or "@" not in creada_por:
            raise ValueError(
                "El correo de la persona creadora debe contener '@'."
            )

        incidencia = Incidencia(
            identificador=None,
            titulo=titulo.strip(),
            descripcion=descripcion.strip(),
            creada_por=creada_por.strip(),
            estado=EstadoIncidencia.ABIERTA,
            identificador_tecnico=None,
        )

        return self.repositorio_incidencias.crear(incidencia)

    def asignar_incidencia(
        self,
        identificador_incidencia: int,
        identificador_tecnico: int,
    ) -> None:
        """
        Asigna una incidencia a un técnico.

        Comprueba que ambos existan, que el técnico esté activo
        y que la incidencia no esté cerrada.
        """

        incidencia = (
            self.repositorio_incidencias.obtener_por_identificador(
                identificador_incidencia
            )
        )

        if incidencia is None:
            raise ValueError(
                f"La incidencia {identificador_incidencia} no existe."
            )

        tecnico = self.repositorio_tecnicos.obtener_por_identificador(
            identificador_tecnico
        )

        if tecnico is None:
            raise ValueError(
                f"El técnico {identificador_tecnico} no existe."
            )

        if not tecnico.activo:
            raise ValueError(
                "No se puede asignar la incidencia a un técnico inactivo."
            )

        if incidencia.estado == EstadoIncidencia.CERRADA:
            raise ValueError(
                "No se puede asignar una incidencia cerrada."
            )

        actualizado = self.repositorio_incidencias.asignar_tecnico(
            identificador_incidencia,
            identificador_tecnico,
        )

        if not actualizado:
            raise ValueError(
                "No se ha podido asignar el técnico a la incidencia."
            )

    def cerrar_incidencia(
        self,
        identificador_incidencia: int,
    ) -> None:
        """
        Cierra una incidencia.

        No permite cerrar una incidencia inexistente,
        ya cerrada o sin técnico asignado.
        """

        incidencia = (
            self.repositorio_incidencias.obtener_por_identificador(
                identificador_incidencia
            )
        )

        if incidencia is None:
            raise ValueError(
                f"La incidencia {identificador_incidencia} no existe."
            )

        if incidencia.estado == EstadoIncidencia.CERRADA:
            raise ValueError(
                "La incidencia ya está cerrada."
            )

        if incidencia.identificador_tecnico is None:
            raise ValueError(
                "No se puede cerrar una incidencia sin técnico asignado."
            )

        actualizado = self.repositorio_incidencias.actualizar_estado(
            identificador_incidencia,
            EstadoIncidencia.CERRADA,
        )

        if not actualizado:
            raise ValueError(
                "No se ha podido cerrar la incidencia."
            )

    def obtener_todas_las_incidencias(self) -> List[Incidencia]:
        """
        Devuelve todas las incidencias registradas.
        """
        return self.repositorio_incidencias.obtener_todas()

    def obtener_incidencias_abiertas(self) -> List[Incidencia]:
        """
        Devuelve únicamente las incidencias con estado ABIERTA.
        """
        return self.repositorio_incidencias.obtener_abiertas()

    def obtener_incidencia_por_identificador(
        self,
        identificador_incidencia: int,
    ) -> Optional[Incidencia]:
        """
        Devuelve una incidencia concreta o None si no existe.
        """
        return self.repositorio_incidencias.obtener_por_identificador(
            identificador_incidencia
        )