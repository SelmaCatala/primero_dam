## Estructura del proyecto

> **Showcase_U**: carpeta principal que contiene todos los archivos y directorios necesarios para el funcionamiento del proyecto.

### Estructura interna

```text
Showcase_U/
│
├── assets/
│   ├── css/
│   │   └── Carpeta que contiene los archivos de estilos CSS utilizados en la web.
│   │
│   └── img/
│       └── Carpeta que contiene las imágenes utilizadas en el proyecto.
│
├── config/
│   └── db.php
│       └── Archivo de configuración encargado de la conexión con la base de datos.
│
├── public/
│   ├── index.php
│   │   └── Página principal pública del proyecto.
│   │
│   └── insertar.php
│       └── Archivo encargado de gestionar la inserción de datos en la base de datos.
│
├── index.php
│   └── Archivo principal de entrada del proyecto.
│
└── showcase_u_create_database.sql
    └── Script SQL utilizado para la creación de la base de datos y sus tablas.
```

### Descripción de carpetas y archivos

- **`assets/`**: contiene los recursos estáticos utilizados en la web.
  - **`css/`**: almacena los archivos de estilos CSS.
  - **`img/`**: almacena las imágenes usadas en el proyecto.

- **`config/`**: contiene los archivos de configuración del proyecto.
  - **`db.php`**: archivo encargado de realizar la conexión con la base de datos.

- **`public/`**: contiene los archivos públicos accesibles desde el navegador.
  - **`index.php`**: página principal pública del proyecto.
  - **`insertar.php`**: archivo encargado de insertar datos en la base de datos.

- **`index.php`**: archivo principal de inicio del proyecto.

- **`showcase_u_create_database.sql`**: archivo SQL empleado para crear la base de datos y sus tablas.
