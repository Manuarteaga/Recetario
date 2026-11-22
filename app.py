import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración pensada para móvil
st.set_page_config(page_title="Mis Recetas", page_icon="🍳", layout="centered")

# Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def cargar_recetas():
    # ttl=0 evita que la caché muestre datos viejos tras añadir una receta
    return conn.read(ttl=0).dropna(how="all")

st.title("🍳 Mi Recetario")

tab_ver, tab_nueva = st.tabs(["📖 Consultar Recetas", "➕ Añadir Receta"])

# --- PESTAÑA 1: CONSULTAR ---
with tab_ver:
    df = cargar_recetas()
    
    if df.empty:
        st.info("Aún no tienes recetas guardadas. ¡Añade la primera en la otra pestaña!")
    else:
        # Buscador y filtro por categoría
        col1, col2 = st.columns([2, 1])
        with col1:
            busqueda = st.text_input("🔍 Buscar por nombre o ingrediente", placeholder="Ej: pollo, calabacín...")
        with col2:
            categorias = ["Todas"] + sorted(df["categoria"].dropna().unique().tolist())
            cat_seleccionada = st.selectbox("Categoría", categorias)

        # Aplicar filtros
        df_filtrado = df.copy()
        if cat_seleccionada != "Todas":
            df_filtrado = df_filtrado[df_filtrado["categoria"] == cat_seleccionada]
        if busqueda:
            mask = (
                df_filtrado["titulo"].str.contains(busqueda, case=False, na=False) |
                df_filtrado["ingredientes"].str.contains(busqueda, case=False, na=False)
            )
            df_filtrado = df_filtrado[mask]

        if df_filtrado.empty:
            st.warning("No hay recetas que coincidan con tu búsqueda.")
        else:
            receta_elegida = st.selectbox("Selecciona una receta:", df_filtrado["titulo"].tolist())
            datos = df_filtrado[df_filtrado["titulo"] == receta_elegida].iloc[0]

            st.divider()
            st.subheader(datos["titulo"])
            
            # Métricas rápidas
            m1, m2, m3 = st.columns(3)
            m1.metric("Categoría", datos["categoria"])
            m2.metric("Tiempo", f"{int(datos['tiempo'])} min")
            raciones_base = int(datos["raciones"]) if pd.notna(datos["raciones"]) else 2
            raciones_deseadas = m3.number_input("Raciones", min_value=1, max_value=20, value=raciones_base)

            if pd.notna(datos["imagen_url"]) and str(datos["imagen_url"]).startswith("http"):
                st.image(datos["imagen_url"], use_container_width=True)

            # Mostrar ingredientes (con aviso de multiplicador si cambian las raciones)
            st.markdown("### 🛒 Ingredientes")
            if raciones_deseadas != raciones_base:
                factor = round(raciones_deseadas / raciones_base, 2)
                st.caption(f"💡 Multiplica las cantidades originales por **x{factor}** (base: {raciones_base} pers.)")
            
            for linea in str(datos["ingredientes"]).split("\n"):
                if linea.strip():
                    st.checkbox(linea.strip(), key=f"ing_{receta_elegida}_{linea}")

            st.markdown("### 👨‍🍳 Preparación")
            st.write(datos["pasos"])

# --- PESTAÑA 2: AÑADIR ---
with tab_nueva:
    with st.form("form_receta", clear_on_submit=True):
        titulo = st.text_input("Nombre de la receta *")
        c1, c2, c3 = st.columns(3)
        categoria = c1.selectbox("Categoría", ["Plato principal", "Cena rápida", "Desayuno", "Postre", "Salsa/Guarnición"])
        tiempo = c2.number_input("Tiempo (min)", min_value=1, value=30, step=5)
        raciones = c3.number_input("Raciones base", min_value=1, value=2)
        
        ingredientes = st.text_area("Ingredientes (uno por línea) *", height=150, placeholder="200g de arroz\n1 pechuga de pollo\nAceite de oliva")
        pasos = st.text_area("Pasos de elaboración *", height=200, placeholder="1. Cortar el pollo...\n2. Sofreír...")
        imagen_url = st.text_input("URL de imagen (opcional)", placeholder="https://...")

        enviado = st.form_submit_button("Guardar receta", use_container_width=True)

        if enviado:
            if not titulo or not ingredientes or not pasos:
                st.error("Por favor, rellena al menos el título, los ingredientes y los pasos.")
            else:
                nueva_fila = pd.DataFrame([{
                    "titulo": titulo,
                    "categoria": categoria,
                    "tiempo": tiempo,
                    "raciones": raciones,
                    "ingredientes": ingredientes,
                    "pasos": pasos,
                    "imagen_url": imagen_url
                }])
                df_actualizado = pd.concat([cargar_recetas(), nueva_fila], ignore_index=True)
                conn.update(data=df_actualizado)
                st.success(f"¡'{titulo}' guardada correctamente!")
                st.rerun()
