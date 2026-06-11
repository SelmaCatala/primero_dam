import streamlit as st

st.set_page_config(
    page_title="Ciudades del mundo",
    page_icon="🌍",
    layout="wide"
)

st.title("Ciudades del mundo")
st.subheader("Imágenes y descripción")

col1, col2, col3 = st.columns(3)

with col1:
    st.image(
        "https://commons.wikimedia.org/wiki/Special:FilePath/Tour%20Eiffel%20-%20night%20%282016%29.jpg",
        caption="París",
        width=250
    )
    with st.expander("París"):
        st.write("Capital de Francia")

with col2:
    st.image(
        "https://commons.wikimedia.org/wiki/Special:FilePath/Statue%20of%20Liberty%207.jpg",
        caption="New York",
        width=250
    )
    with st.expander("New York"):
        st.write("La ciudad de los rascacielos")

with col3:
    st.image(
        "https://commons.wikimedia.org/wiki/Special:FilePath/Gondola-Venice-Italy.jpg",
        caption="Venecia",
        width=250
    )
    with st.expander("Venecia"):
        st.write("La ciudad de los canales")