# Gestión de incidencias en Python

Proyecto práctico de **Entornos de Desarrollo (1.º DAM)** para gestionar técnicos e incidencias internas mediante Python, SQLite y una arquitectura por capas.

## Funcionalidades

La aplicación permite:

- registrar técnicos;
- consultar todos los técnicos;
- crear incidencias;
- consultar todas las incidencias;
- consultar incidencias abiertas;
- buscar una incidencia por identificador;
- asignar una incidencia a un técnico;
- cerrar una incidencia;
- utilizar un menú interactivo de consola;
- comprobar reglas de negocio mediante pruebas manuales.

## Arquitectura

```text
aplicacion.py / menu.py
          ↓
     servicio.py
          ↓
    repositorio.py
          ↓
        db.py
          ↓
        SQLite
```

`modelos.py` define los objetos utilizados por todas las capas.

## Estructura del proyecto

```text
PythonProject3/
│
├── modelos.py
├── db.py
├── repositorio.py
├── servicio.py
├── aplicacion.py
├── menu.py
├── pruebas_reglas.py
├── .gitignore
└── README.md
```

## Archivos principales

### `modelos.py`

Define:

- `EstadoIncidencia`;
- `Tecnico`;
- `Incidencia`.

### `db.py`

Se encarga de:

- abrir la conexión con SQLite;
- crear las tablas `tecnicos` e `incidencias`;
- activar las claves foráneas.

### `repositorio.py`

Contiene:

- `RepositorioTecnicos`;
- `RepositorioIncidencias`.

Esta capa ejecuta las consultas SQL y convierte las filas de SQLite en objetos de Python.

### `servicio.py`

Contiene la lógica de negocio y las validaciones.

### `aplicacion.py`

Ejecuta una demostración automática y completa del funcionamiento del proyecto.

### `menu.py`

Proporciona una interfaz interactiva de consola.

Permite:

- registrar técnicos;
- listar técnicos;
- crear incidencias;
- listar todas las incidencias;
- listar incidencias abiertas;
- buscar incidencias por identificador;
- asignar incidencias a técnicos;
- cerrar incidencias;
- salir de la aplicación.

### `pruebas_reglas.py`

Comprueba que se bloquean operaciones incorrectas.

## Reglas de negocio

La aplicación comprueba que:

- el nombre del técnico no esté vacío;
- el correo del técnico no esté vacío;
- el correo del técnico contenga `@`;
- el título de la incidencia no esté vacío;
- el correo de la persona creadora contenga `@`;
- no se pueda asignar una incidencia inexistente;
- no se pueda asignar un técnico inexistente;
- no se pueda asignar una incidencia a un técnico inactivo;
- no se pueda asignar una incidencia cerrada;
- no se pueda cerrar una incidencia inexistente;
- no se pueda cerrar una incidencia ya cerrada;
- no se pueda cerrar una incidencia sin técnico asignado.

## Estados de una incidencia

```text
ABIERTA
EN_PROGRESO
CERRADA
```

## Requisitos

- Python 3.12 o compatible.
- PyCharm u otro editor de Python.
- Git, si se desea utilizar control de versiones.

No es necesario instalar XAMPP, MySQL ni phpMyAdmin, porque el proyecto utiliza SQLite.

## Cómo ejecutar la aplicación automática

Desde PyCharm:

1. Abrir `aplicacion.py`.
2. Hacer clic derecho dentro del archivo.
3. Seleccionar `Run 'aplicacion'`.

También puede ejecutarse desde la terminal:

```bash
python aplicacion.py
```

La aplicación automática:

1. prepara la base de datos;
2. registra técnicos;
3. crea incidencias;
4. lista los datos;
5. asigna un técnico;
6. cierra una incidencia;
7. muestra el resultado final.

## Cómo ejecutar el menú interactivo

Desde PyCharm:

1. Abrir `menu.py`.
2. Hacer clic derecho dentro del archivo.
3. Seleccionar `Run 'menu'`.

También puede ejecutarse desde la terminal:

```bash
python menu.py
```

El menú permite elegir entre las siguientes opciones:

```text
1. Registrar técnico
2. Listar técnicos
3. Crear incidencia
4. Listar todas las incidencias
5. Listar incidencias abiertas
6. Buscar incidencia por identificador
7. Asignar incidencia a un técnico
8. Cerrar incidencia
0. Salir
```

## Cómo ejecutar las pruebas

Desde PyCharm:

1. Abrir `pruebas_reglas.py`.
2. Hacer clic derecho dentro del archivo.
3. Seleccionar `Run 'pruebas_reglas'`.

También puede ejecutarse desde la terminal:

```bash
python pruebas_reglas.py
```

Las pruebas comprueban:

- título vacío;
- correo incorrecto;
- incidencia inexistente;
- técnico inexistente;
- cierre sin técnico;
- doble cierre.

## Base de datos

La base de datos se crea automáticamente con el nombre:

```text
gestion_incidencias.db
```

Este archivo no se incluye en Git porque se genera durante la ejecución.

## Archivos ignorados por Git

El archivo `.gitignore` excluye:

```text
.venv/
__pycache__/
.idea/
gestion_incidencias.db
```

## Historial inicial de Git

Primer commit:

```text
Crear aplicación de gestión de incidencias por capas
```

Segundo commit:

```text
Añadir pruebas de reglas de negocio
```

Tercer commit:

```text
Añadir documentación del proyecto
```

Cuarto commit:

```text
Añadir menú interactivo de consola
```

## Autoría

Proyecto académico desarrollado para practicar:

- Python,
- programación orientada a objetos;
- SQLite;
- arquitectura por capas;
- patrón servicio-repositorio;
- pruebas de reglas de negocio;
- interfaces de consola;
- Git y GitHub Desktop.
