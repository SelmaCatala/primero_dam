import sqlite3
from sqlite3 import Connection


NOMBRE_BASE_DATOS = "gestion_incidencias.db"


def obtener_conexion() -> Connection:
    """
    Abre y devuelve una conexión con la base de datos SQLite.
    """
    conexion = sqlite3.connect(NOMBRE_BASE_DATOS)

    # Activa la comprobación de las claves foráneas.
    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion


def inicializar_base_datos() -> None:
    """
    Crea las tablas de la aplicación si todavía no existen.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tecnicos (
            identificador INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            activo INTEGER NOT NULL DEFAULT 1
                CHECK (activo IN (0, 1))
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS incidencias (
            identificador INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            creada_por TEXT NOT NULL,
            estado TEXT NOT NULL,
            identificador_tecnico INTEGER,
            FOREIGN KEY (identificador_tecnico)
                REFERENCES tecnicos(identificador)
        )
        """
    )

    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    inicializar_base_datos()
    print("Base de datos inicializada correctamente.")