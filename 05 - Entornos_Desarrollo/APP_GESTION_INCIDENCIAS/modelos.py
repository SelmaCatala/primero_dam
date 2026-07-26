from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EstadoIncidencia(Enum):
    ABIERTA = "ABIERTA"
    EN_PROGRESO = "EN_PROGRESO"
    CERRADA = "CERRADA"


@dataclass
class Tecnico:
    identificador: Optional[int]
    nombre: str
    correo: str
    activo: bool = True


@dataclass
class Incidencia:
    identificador: Optional[int]
    titulo: str
    descripcion: str
    creada_por: str
    estado: EstadoIncidencia
    identificador_tecnico: Optional[int] = None