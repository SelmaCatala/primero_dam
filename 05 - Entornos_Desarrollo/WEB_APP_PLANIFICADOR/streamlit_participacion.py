import streamlit as st
import time
import datetime

st.set_page_config(
    page_title="Planificador Diario de Entrenamiento",
    page_icon="💪",
    layout="wide"
)

st.title("Planificador Diario de Entrenamiento")
st.header("Datos del usuario")
st.subheader("Esta app sirve para crear una rutina diaria de entrenamiento.")

st.code("import datetime", language="python")

nombre = st.text_input("¿Cómo te llamas?")
edad = st.number_input("¿Cuál es tu edad?", min_value=1, max_value=120)

objetivo = st.selectbox(
    "Elige tu objetivo",
    ["Fuerza", "Resistencia", "Flexibilidad"]
)

ejercicios = st.multiselect(
    "Elige ejercicios",
    ["Cardio", "Pesas", "Yoga", "Pilates", "HIIT"]
)

intensidad = st.slider("Intensidad", 1, 10)

fecha = st.date_input("Fecha de la rutina")

if "contador" not in st.session_state:
    st.session_state.contador = 0

if st.button("Iniciar rutina"):
    st.session_state.contador = st.session_state.contador + 1
    st.success(f"Rutinas registradas: {st.session_state.contador}")

    progreso = st.progress(0)

    for i in range(0, 101, 10):
        time.sleep(0.1)
        progreso.progress(i)

st.header("Multimedia")

st.image(
    "https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg",
    caption="Entrenamiento",
    width=400
)

st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

st.video("https://www.youtube.com/watch?v=ml6cT4AZdqI")

col1, col2 = st.columns(2)

with col1:
    st.info(f"Nombre: {nombre}")
    st.info(f"Edad: {edad}")
    st.info(f"Objetivo: {objetivo}")
    st.info(f"Intensidad: {intensidad}")

with col2:
    if objetivo == "Fuerza":
        st.warning("Consejo: descansa entre series.")
    elif objetivo == "Resistencia":
        st.warning("Consejo: hidrátate bien.")
    else:
        st.warning("Consejo: estira despacio.")

with st.expander("Consejos adicionales"):
    st.write("Calienta antes de empezar.")
    st.write("Bebe agua.")
    st.write("Estira al terminar.")

st.success("¡Rutina planificada con éxito!")