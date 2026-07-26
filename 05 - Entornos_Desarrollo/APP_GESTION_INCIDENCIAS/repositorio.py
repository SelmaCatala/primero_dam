from sqlite3 import Row
from typing import List, Optional

from db import obtener_conexion
from modelos import EstadoIncidencia, Incidencia, Tecnico


class RepositorioTecnicos:
    def crear(self, tecnico: Tecnico) -> Tecnico:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO tecnicos (nombre, correo, activo)
            VALUES (?, ?, ?)
            """,
            (
                tecnico.nombre,
                tecnico.correo,
                1 if tecnico.activo else 0,
            ),
        )

        conexion.commit()
        identificador = cursor.lastrowid
        conexion.close()

        return Tecnico(
            identificador=identificador,
            nombre=tecnico.nombre,
            correo=tecnico.correo,
            activo=tecnico.activo,
        )

    def obtener_todos(self) -> List[Tecnico]:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM tecnicos")
        filas = cursor.fetchall()

        conexion.close()

        return [self._convertir_fila_en_tecnico(fila) for fila in filas]

    def obtener_por_identificador(
        self,
        identificador_tecnico: int,
    ) -> Optional[Tecnico]:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT *
            FROM tecnicos
            WHERE identificador = ?
            """,
            (identificador_tecnico,),
        )

        fila = cursor.fetchone()
        conexion.close()

        if fila is None:
            return None

        return self._convertir_fila_en_tecnico(fila)

    def _convertir_fila_en_tecnico(self, fila: Row) -> Tecnico:
        return Tecnico(
            identificador=fila[0],
            nombre=fila[1],
            correo=fila[2],
            activo=bool(fila[3]),
        )


class RepositorioIncidencias:
    def crear(self, incidencia: Incidencia) -> Incidencia:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO incidencias (
                titulo,
                descripcion,
                creada_por,
                estado,
                identificador_tecnico
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                incidencia.titulo,
                incidencia.descripcion,
                incidencia.creada_por,
                incidencia.estado.value,
                incidencia.identificador_tecnico,
            ),
        )

        conexion.commit()
        identificador = cursor.lastrowid
        conexion.close()

        return Incidencia(
            identificador=identificador,
            titulo=incidencia.titulo,
            descripcion=incidencia.descripcion,
            creada_por=incidencia.creada_por,
            estado=incidencia.estado,
            identificador_tecnico=incidencia.identificador_tecnico,
        )

    def obtener_todas(self) -> List[Incidencia]:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM incidencias")
        filas = cursor.fetchall()

        conexion.close()

        return [self._convertir_fila_en_incidencia(fila) for fila in filas]

    def obtener_por_identificador(
        self,
        identificador_incidencia: int,
    ) -> Optional[Incidencia]:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT *
            FROM incidencias
            WHERE identificador = ?
            """,
            (identificador_incidencia,),
        )

        fila = cursor.fetchone()
        conexion.close()

        if fila is None:
            return None

        return self._convertir_fila_en_incidencia(fila)

    def actualizar_estado(
        self,
        identificador_incidencia: int,
        estado: EstadoIncidencia,
    ) -> bool:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE incidencias
            SET estado = ?
            WHERE identificador = ?
            """,
            (
                estado.value,
                identificador_incidencia,
            ),
        )

        conexion.commit()
        actualizado = cursor.rowcount > 0
        conexion.close()

        return actualizado

    def asignar_tecnico(
        self,
        identificador_incidencia: int,
        identificador_tecnico: int,
    ) -> bool:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE incidencias
            SET identificador_tecnico = ?,
                estado = ?
            WHERE identificador = ?
            """,
            (
                identificador_tecnico,
                EstadoIncidencia.EN_PROGRESO.value,
                identificador_incidencia,
            ),
        )

        conexion.commit()
        actualizado = cursor.rowcount > 0
        conexion.close()

        return actualizado

    def obtener_abiertas(self) -> List[Incidencia]:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT *
            FROM incidencias
            WHERE estado = ?
            """,
            (EstadoIncidencia.ABIERTA.value,),
        )

        filas = cursor.fetchall()
        conexion.close()

        return [self._convertir_fila_en_incidencia(fila) for fila in filas]

    def _convertir_fila_en_incidencia(self, fila: Row) -> Incidencia:
        return Incidencia(
            identificador=fila[0],
            titulo=fila[1],
            descripcion=fila[2],
            creada_por=fila[3],
            estado=EstadoIncidencia(fila[4]),
            identificador_tecnico=fila[5],
        )