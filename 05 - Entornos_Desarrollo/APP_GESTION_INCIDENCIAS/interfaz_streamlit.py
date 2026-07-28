import streamlit as st

from db import inicializar_base_datos
from servicio import ServicioIncidencias

def aplicar_estilos() -> None:
    """
    Aplica estilos visuales personalizados a la interfaz.
    """
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f5f7fb;
        }

        [data-testid="stSidebar"] {
            background-color: #172033;
        }

        [data-testid="stSidebar"] * {
            color: white;
        }

        [data-testid="stSidebar"] label {
            color: white !important;
        }

        .cabecera-principal {
            padding: 28px 32px;
            margin-bottom: 25px;
            border-radius: 16px;
            background: linear-gradient(
                120deg,
                #1f4e78,
                #2878b5
            );
            color: white;
            box-shadow: 0 8px 22px rgba(0, 0, 0, 0.12);
        }

        .cabecera-principal h1 {
            margin: 0;
            color: white;
            font-size: 2.3rem;
        }

        .cabecera-principal p {
            margin-top: 8px;
            margin-bottom: 0;
            font-size: 1.05rem;
            color: #eaf4ff;
        }

        .tarjeta-informativa {
            padding: 18px;
            margin-bottom: 15px;
            border-radius: 14px;
            background-color: white;
            border: 1px solid #dfe5ee;
            box-shadow: 0 4px 14px rgba(31, 78, 120, 0.08);
        }

        div[data-testid="stMetric"] {
            padding: 18px;
            border-radius: 14px;
            background-color: white;
            border: 1px solid #dfe5ee;
            box-shadow: 0 4px 14px rgba(31, 78, 120, 0.08);
        }

        div[data-testid="stForm"] {
            padding: 22px;
            border-radius: 14px;
            background-color: white;
            border: 1px solid #dfe5ee;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            border: none;
            border-radius: 9px;
            background-color: #1f4e78;
            color: white;
            font-weight: 600;
            padding: 0.55rem 1.2rem;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            background-color: #2878b5;
            color: white;
        }

        .pie-pagina {
            margin-top: 45px;
            padding-top: 18px;
            border-top: 1px solid #d9dee7;
            text-align: center;
            color: #667085;
            font-size: 0.85rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def mostrar_cabecera(
        titulo: str,
        descripcion: str,
) -> None:
    """
    Muestra una cabecera visual para cada sección.
    """
    st.markdown(
        f"""
        <div class="cabecera-principal">
            <h1>{titulo}</h1>
            <p>{descripcion}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def mostrar_pie_pagina() -> None:
    """
    Muestra el pie de página de la aplicación.
    """
    st.markdown(
        """
        <div class="pie-pagina">
            Gestión de incidencias · Python · SQLite · Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )

def mostrar_inicio(
    servicio: ServicioIncidencias,
) -> None:
    """
    Muestra la página principal de la aplicación.
    """
    mostrar_cabecera(
        titulo="🛠️ Gestión de incidencias",
        descripcion=(
            "Panel principal para administrar técnicos "
            "e incidencias internas."
        ),
    )

    st.write(
        "Esta interfaz permite trabajar con técnicos e incidencias "
        "utilizando la misma base de datos y las mismas reglas de negocio "
        "del proyecto."
    )

    tecnicos = servicio.obtener_todos_los_tecnicos()
    incidencias = servicio.obtener_todas_las_incidencias()
    incidencias_abiertas = servicio.obtener_incidencias_abiertas()

    total_tecnicos = len(tecnicos)
    total_incidencias = len(incidencias)
    total_abiertas = len(incidencias_abiertas)
    total_cerradas = sum(
        1
        for incidencia in incidencias
        if incidencia.estado.value == "CERRADA"
    )
    total_en_progreso = sum(
        1
        for incidencia in incidencias
        if incidencia.estado.value == "EN_PROGRESO"
    )

    columna_1, columna_2, columna_3, columna_4 = st.columns(4)

    with columna_1:
        st.metric(
            label="Técnicos",
            value=total_tecnicos,
        )

    with columna_2:
        st.metric(
            label="Incidencias",
            value=total_incidencias,
        )

    with columna_3:
        st.metric(
            label="Abiertas",
            value=total_abiertas,
        )

    with columna_4:
        st.metric(
            label="Cerradas",
            value=total_cerradas,
        )

    st.markdown(
        """
        <div class="tarjeta-informativa">
            <strong>¿Qué puedes hacer?</strong>
            <p>
                Utiliza el menú lateral para registrar técnicos,
                crear incidencias, consultar registros, realizar
                asignaciones y cerrar incidencias.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )




def mostrar_registro_tecnico(
    servicio: ServicioIncidencias,
) -> None:
    """
    Muestra el formulario para registrar técnicos.
    """
    mostrar_cabecera(
        titulo="👨‍💻 Registrar técnico",
        descripcion="Añade un nuevo técnico al sistema.",
    )

    st.write(
        "Introduce el nombre y el correo del nuevo técnico."
    )

    with st.form("formulario_tecnico"):
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo")

        enviar = st.form_submit_button(
            "Registrar técnico"
        )

    if enviar:
        try:
            tecnico = servicio.registrar_tecnico(
                nombre=nombre,
                correo=correo,
            )

            st.success(
                f"Técnico registrado correctamente con ID "
                f"{tecnico.identificador}."
            )

        except ValueError as error:
            st.error(str(error))


def mostrar_creacion_incidencia(
    servicio: ServicioIncidencias,
) -> None:
    """
    Muestra el formulario para crear incidencias.
    """
    mostrar_cabecera(
        titulo="📝 Crear incidencia",
        descripcion="Registra una nueva incidencia interna.",
    )

    st.write(
        "Introduce los datos necesarios para registrar una incidencia."
    )

    with st.form("formulario_incidencia"):
        titulo = st.text_input("Título")

        descripcion = st.text_area(
            "Descripción"
        )

        creada_por = st.text_input(
            "Correo de la persona creadora"
        )

        enviar = st.form_submit_button(
            "Crear incidencia"
        )

    if enviar:
        try:
            incidencia = servicio.crear_incidencia(
                titulo=titulo,
                descripcion=descripcion,
                creada_por=creada_por,
            )

            st.success(
                f"Incidencia creada correctamente con ID "
                f"{incidencia.identificador}."
            )

        except ValueError as error:
            st.error(str(error))


def convertir_tecnicos_en_filas(
    tecnicos: list,
) -> list[dict]:
    """
    Convierte los técnicos en una lista de diccionarios.

    Streamlit utiliza estos diccionarios para crear la tabla.
    """
    filas = []

    for tecnico in tecnicos:
        estado = "Activo" if tecnico.activo else "Inactivo"

        fila = {
            "Identificador": tecnico.identificador,
            "Nombre": tecnico.nombre,
            "Correo": tecnico.correo,
            "Estado": estado,
        }

        filas.append(fila)

    return filas


def mostrar_tecnicos(
    servicio: ServicioIncidencias,
) -> None:
    """
    Muestra todos los técnicos registrados.
    """
    mostrar_cabecera(
        titulo="👥 Técnicos registrados",
        descripcion="Consulta el personal técnico disponible.",
    )

    tecnicos = servicio.obtener_todos_los_tecnicos()

    if not tecnicos:
        st.warning(
            "Todavía no hay técnicos registrados."
        )
        return

    filas = convertir_tecnicos_en_filas(
        tecnicos
    )

    st.dataframe(
        filas,
        width="stretch",
        hide_index=True,
    )

    st.caption(
        f"Total de técnicos registrados: {len(tecnicos)}"
    )


def convertir_incidencias_en_filas(
    incidencias: list,
) -> list[dict]:
    """
    Convierte las incidencias en una lista de diccionarios.
    """
    filas = []

    for incidencia in incidencias:
        identificador_tecnico = (
            incidencia.identificador_tecnico
        )

        if identificador_tecnico is None:
            tecnico = "Sin asignar"
        else:
            tecnico = str(identificador_tecnico)

        fila = {
            "Identificador": incidencia.identificador,
            "Título": incidencia.titulo,
            "Descripción": incidencia.descripcion,
            "Creada por": incidencia.creada_por,
            "Estado": incidencia.estado.value,
            "Técnico": tecnico,
        }

        filas.append(fila)

    return filas


def mostrar_incidencias(
    servicio: ServicioIncidencias,
) -> None:
    """
    Muestra las incidencias registradas.
    """
    mostrar_cabecera(
        titulo="📋 Incidencias registradas",
        descripcion="Consulta y filtra las incidencias del sistema.",
    )

    tipo_listado = st.radio(
        "Selecciona las incidencias que deseas consultar",
        (
            "Todas",
            "Solo abiertas",
        ),
        horizontal=True,
    )

    if tipo_listado == "Todas":
        incidencias = (
            servicio.obtener_todas_las_incidencias()
        )
    else:
        incidencias = (
            servicio.obtener_incidencias_abiertas()
        )

    if not incidencias:
        st.warning(
            "No hay incidencias para mostrar."
        )
        return

    filas = convertir_incidencias_en_filas(
        incidencias
    )

    st.dataframe(
        filas,
        width="stretch",
        hide_index=True,
    )

    st.caption(
        f"Total de incidencias mostradas: {len(incidencias)}"
    )


def mostrar_asignacion_incidencia(
    servicio: ServicioIncidencias,
) -> None:
    """
    Permite asignar una incidencia abierta
    a un técnico activo.
    """
    mostrar_cabecera(
        titulo="🔗 Asignar incidencia",
        descripcion="Asigna una incidencia abierta a un técnico activo.",
    )

    st.write(
        "Selecciona una incidencia abierta y el técnico "
        "que se encargará de resolverla."
    )

    incidencias = servicio.obtener_incidencias_abiertas()

    tecnicos = [
        tecnico
        for tecnico in servicio.obtener_todos_los_tecnicos()
        if tecnico.activo
    ]

    if not incidencias:
        st.warning(
            "No hay incidencias abiertas disponibles para asignar."
        )
        return

    if not tecnicos:
        st.warning(
            "No hay técnicos activos disponibles."
        )
        return

    with st.form("formulario_asignacion"):
        incidencia_seleccionada = st.selectbox(
            "Incidencia",
            options=incidencias,
            format_func=lambda incidencia: (
                f"ID {incidencia.identificador} - "
                f"{incidencia.titulo}"
            ),
        )

        tecnico_seleccionado = st.selectbox(
            "Técnico",
            options=tecnicos,
            format_func=lambda tecnico: (
                f"ID {tecnico.identificador} - "
                f"{tecnico.nombre}"
            ),
        )

        enviar = st.form_submit_button(
            "Asignar incidencia"
        )

    if enviar:
        try:
            servicio.asignar_incidencia(
                identificador_incidencia=(
                    incidencia_seleccionada.identificador
                ),
                identificador_tecnico=(
                    tecnico_seleccionado.identificador
                ),
            )

            st.success(
                f"La incidencia "
                f"{incidencia_seleccionada.identificador} "
                f"se ha asignado correctamente a "
                f"{tecnico_seleccionado.nombre}."
            )

        except ValueError as error:
            st.error(str(error))


def mostrar_cierre_incidencia(
    servicio: ServicioIncidencias,
) -> None:
    """
    Permite cerrar una incidencia que tenga
    un técnico asignado y no esté cerrada.
    """
    mostrar_cabecera(
        titulo="✅ Cerrar incidencia",
        descripcion="Finaliza una incidencia que ya tenga técnico asignado.",
    )

    st.write(
        "Selecciona una incidencia en progreso para cerrarla."
    )

    todas_las_incidencias = (
        servicio.obtener_todas_las_incidencias()
    )

    incidencias_disponibles = [
        incidencia
        for incidencia in todas_las_incidencias
        if incidencia.estado.value != "CERRADA"
        and incidencia.identificador_tecnico is not None
    ]

    if not incidencias_disponibles:
        st.warning(
            "No hay incidencias disponibles para cerrar."
        )
        return

    with st.form("formulario_cierre"):
        incidencia_seleccionada = st.selectbox(
            "Incidencia",
            options=incidencias_disponibles,
            format_func=lambda incidencia: (
                f"ID {incidencia.identificador} - "
                f"{incidencia.titulo} - "
                f"Técnico {incidencia.identificador_tecnico}"
            ),
        )

        enviar = st.form_submit_button(
            "Cerrar incidencia"
        )

    if enviar:
        try:
            servicio.cerrar_incidencia(
                identificador_incidencia=(
                    incidencia_seleccionada.identificador
                )
            )

            st.success(
                f"La incidencia "
                f"{incidencia_seleccionada.identificador} "
                f"se ha cerrado correctamente."
            )

        except ValueError as error:
            st.error(str(error))


def main() -> None:
    """
    Inicializa la base de datos y muestra la interfaz web.
    """
    st.set_page_config(
        page_title="Gestión de incidencias",
        page_icon="🛠️",
        layout="wide",
    )

    aplicar_estilos()
    inicializar_base_datos()

    servicio = ServicioIncidencias()

    st.sidebar.title("🛠️ Menú")

    opcion = st.sidebar.radio(
        "Selecciona una opción",
        (
            "🏠 Inicio",
            "👨‍💻 Registrar técnico",
            "📝 Crear incidencia",
            "👥 Ver técnicos",
            "📋 Ver incidencias",
            "🔗 Asignar incidencia",
            "✅ Cerrar incidencia",
        ),
    )

    if opcion == "🏠 Inicio":
        mostrar_inicio(servicio)

    elif opcion == "👨‍💻 Registrar técnico":
        mostrar_registro_tecnico(servicio)

    elif opcion == "📝 Crear incidencia":
        mostrar_creacion_incidencia(servicio)

    elif opcion == "👥 Ver técnicos":
        mostrar_tecnicos(servicio)

    elif opcion == "📋 Ver incidencias":
        mostrar_incidencias(servicio)

    elif opcion == "🔗 Asignar incidencia":
        mostrar_asignacion_incidencia(servicio)

    elif opcion == "✅ Cerrar incidencia":
        mostrar_cierre_incidencia(servicio)

    mostrar_pie_pagina()


if __name__ == "__main__":
    main()