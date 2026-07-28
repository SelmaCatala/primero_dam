# Gestión de incidencias en Python

Proyecto práctico de **Entornos de Desarrollo (1.º DAM)** para gestionar técnicos e incidencias internas mediante Python, SQLite, Streamlit y una arquitectura por capas.

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
- utilizar una demostración automática;
- utilizar un menú interactivo de consola;
- utilizar una interfaz web con Streamlit;
- comprobar reglas de negocio mediante pruebas manuales.

## Arquitectura

```text
aplicacion.py / menu.py / interfaz_streamlit.py
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
├── interfaz_streamlit.py
├── pruebas_reglas.py
├── requerimientos.txt
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

### `interfaz_streamlit.py`

Proporciona una interfaz web creada con Streamlit.

Permite:

- consultar indicadores generales;
- registrar técnicos mediante formularios;
- crear incidencias;
- mostrar técnicos en una tabla;
- mostrar todas las incidencias;
- filtrar las incidencias abiertas;
- asignar incidencias a técnicos;
- cerrar incidencias;
- mostrar mensajes de confirmación;
- mostrar los errores generados por las reglas de negocio.

### `pruebas_reglas.py`

Comprueba que se bloquean operaciones incorrectas.

### `requerimientos.txt`

Contiene las dependencias externas necesarias para ejecutar la interfaz web.

Su contenido actual es:

```text
streamlit
```

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
- Streamlit, para ejecutar la interfaz web.

No es necesario instalar XAMPP, MySQL ni phpMyAdmin, porque el proyecto utiliza SQLite.

## Instalación de dependencias

Antes de ejecutar la interfaz web, se deben instalar las dependencias indicadas en `requerimientos.txt`.

Desde la terminal:

```bash
python -m pip install -r requirements.txt
```

También puede instalarse Streamlit directamente:

```bash
python -m pip install streamlit
```

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

## Cómo ejecutar la interfaz web con Streamlit

Desde la terminal de PyCharm:

```bash
python -m streamlit run interfaz_streamlit.py
```

Streamlit iniciará un servidor local y abrirá la aplicación en el navegador.

La dirección habitual es:

```text
http://localhost:8501
```

Para detener el servidor, debe pulsarse:

```text
Ctrl + C
```

La interfaz web incluye las siguientes secciones:

```text
Inicio
Registrar técnico
Crear incidencia
Ver técnicos
Ver incidencias
Asignar incidencia
Cerrar incidencia
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

La interfaz automática, el menú de consola y la interfaz de Streamlit utilizan la misma base de datos.

## Archivos ignorados por Git

El archivo `.gitignore` excluye:

```text
.venv/
__pycache__/
.idea/
gestion_incidencias.db
```

## Seguridad y limitaciones

Esta aplicación es un proyecto académico diseñado para ejecutarse localmente.

Incluye validaciones de reglas de negocio y consultas a una base de datos SQLite. Sin embargo, no incorpora:

- autenticación de usuarios;
- contraseñas;
- permisos por roles;
- cifrado de la base de datos;
- auditoría de operaciones;
- protección avanzada de datos personales.

El archivo `gestion_incidencias.db` se excluye del repositorio mediante `.gitignore` para evitar publicar los datos generados durante las pruebas.

Para utilizar la aplicación en un entorno real sería necesario añadir autenticación, control de permisos, validaciones más completas, registro de actividad y medidas adicionales de protección de datos.

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

Quinto commit:

```text
Actualizar README con el menú interactivo
```

Sexto commit:

```text
Añadir interfaz web con Streamlit
```

## Autoría

Proyecto académico desarrollado para practicar:

- Python;
- programación orientada a objetos;
- SQLite;
- arquitectura por capas;
- patrón servicio-repositorio;
- reglas de negocio;
- pruebas manuales;
- interfaces de consola;
- desarrollo de interfaces web con Streamlit;
- gestión de dependencias;
- Git y GitHub Desktop.