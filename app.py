import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Configuración de página pensada para móvil
st.set_page_config(
    page_title="Mi Recetario · Primascore Style",
    page_icon="🍳",
    layout="centered",
)


def aplicar_estilo_primascore():
    st.markdown(
        """
    <style>
        /* Importar tipografía Plus Jakarta Sans e Inter */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

        /* Variables de identidad visual Primascore */
        :root {
            --ps-navy: #0B1B36;          /* Azul marino oscuro principal */
            --ps-blue: #1D4ED8;          /* Azul eléctrico corporativo */
            --ps-blue-light: #EFF6FF;    /* Azul muy suave para fondos activos */
            --ps-mint: #10B981;          /* Verde acento / éxito */
            --ps-bg: #F4F7FA;            /* Fondo gris azulado ultra claro */
            --ps-card: #FFFFFF;          /* Blanco puro para tarjetas */
            --ps-border: #E2E8F0;        /* Borde sutil de tarjetas */
            --ps-text-main: #0F172A;     /* Texto principal */
            --ps-text-muted: #64748B;    /* Texto secundario */
        }

        /* Fondo general de la aplicación */
        .stApp {
            background-color: var(--ps-bg);
            font-family: 'Inter', sans-serif;
            color: var(--ps-text-main);
        }

        /* Tipografía de títulos */
        h1, h2, h3, .ps-title {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: var(--ps-navy) !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        /* Cabecera estilo Dashboard Primascore */
        .ps-header {
            background: linear-gradient(135deg, #0B1B36 0%, #163263 100%);
            padding: 1.4rem 1.5rem;
            border-radius: 16px;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(11, 27, 54, 0.15);
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.75rem;
        }
        .ps-header-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.5rem;
            font-weight: 800;
            margin: 0;
            color: #FFFFFF;
            letter-spacing: -0.02em;
        }
        .ps-header-subtitle {
            font-size: 0.85rem;
            color: #94A3B8;
            margin: 0.2rem 0 0 0;
        }
        .ps-badge {
            background-color: rgba(16, 185, 129, 0.15);
            color: #34D399;
            border: 1px solid rgba(52, 211, 153, 0.3);
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            white-space: nowrap;
        }

        /* Tarjetas blancas estilo Primascore */
        .ps-card {
            background-color: var(--ps-card);
            border: 1px solid var(--ps-border);
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
        }

        /* Etiquetas tipo píldora */
        .ps-pill {
            display: inline-block;
            background-color: var(--ps-blue-light);
            color: var(--ps-blue);
            font-weight: 600;
            font-size: 0.78rem;
            padding: 0.3rem 0.75rem;
            border-radius: 999px;
            margin-right: 0.4rem;
            margin-bottom: 0.25rem;
        }
        .ps-pill-green {
            background-color: #ECFDF5;
            color: #059669;
        }

        /* Estilo de las pestañas (Tabs) */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #E2E8F0;
            padding: 4px;
            border-radius: 12px;
            gap: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 9px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            color: var(--ps-text-muted);
            border: none !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: var(--ps-card) !important;
            color: var(--ps-navy) !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        }

        /* Botones principales */
        .stButton > button, .stFormSubmitButton > button {
            background-color: var(--ps-blue) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.65rem 1.25rem !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(29, 78, 216, 0.2);
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover {
            background-color: var(--ps-navy) !important;
            transform: translateY(-1px);
        }

        /* Inputs, Selectbox y Textareas */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div {
            background-color: var(--ps-card) !important;
            border: 1px solid var(--ps-border) !important;
            border-radius: 10px !important;
            color: var(--ps-text-main) !important;
        }
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--ps-blue) !important;
            box-shadow: 0 0 0 2px rgba(29, 78, 216, 0.15) !important;
        }

        /* Checkboxes de ingredientes más limpios y táctiles para móvil */
        .stCheckbox {
            background-color: var(--ps-card);
            padding: 0.6rem 0.9rem;
            border-radius: 10px;
            border: 1px solid var(--ps-border);
            margin-bottom: 0.45rem;
            transition: border-color 0.15s ease;
        }
        .stCheckbox:hover {
            border-color: var(--ps-blue);
        }

        /* Ocultar marca de agua y menú superior de Streamlit para que parezca app nativa */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """,
        unsafe_allow_html=True,
    )


aplicar_estilo_primascore()

# Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)


def cargar_recetas():
    # ttl=0 evita que la caché muestre datos viejos tras añadir una receta
    return conn.read(ttl=0).dropna(how="all")


# Cabecera HTML estilo Primascore
st.markdown(
    """
<div class="ps-header">
    <div>
        <p class="ps-header-title">🍳 Mi Recetario</p>
        <p class="ps-header-subtitle">Colección personal sincronizada</p>
    </div>
    <span class="ps-badge">● Cloud Sync</span>
</div>
""",
    unsafe_allow_html=True,
)

tab_ver, tab_nueva = st.tabs(["📖 Consultar Recetas", "➕ Añadir Receta"])

# --- PESTAÑA 1: CONSULTAR ---
with tab_ver:
    df = cargar_recetas()

    if df.empty:
        st.info("Aún no tienes recetas guardadas. ¡Añade la primera en la pestaña 'Añadir Receta'!")
    else:
        col1, col2 = st.columns([2, 1])
        with col1:
            busqueda = st.text_input(
                "🔍 Buscar por nombre o ingrediente",
                placeholder="Ej: pollo, calabacín...",
            )
        with col2:
            categorias = ["Todas"] + sorted(df["categoria"].dropna().unique().tolist())
            cat_seleccionada = st.selectbox("Categoría", categorias)

        # Aplicar filtros
        df_filtrado = df.copy()
        if cat_seleccionada != "Todas":
            df_filtrado = df_filtrado[df_filtrado["categoria"] == cat_seleccionada]
        if busqueda:
            mask = (
                df_filtrado["titulo"].str.contains(busqueda, case=False, na=False)
                | df_filtrado["ingredientes"].str.contains(busqueda, case=False, na=False)
            )
            df_filtrado = df_filtrado[mask]

        if df_filtrado.empty:
            st.warning("No hay recetas que coincidan con tu búsqueda.")
        else:
            receta_elegida = st.selectbox(
                "Selecciona una receta:", df_filtrado["titulo"].tolist()
            )
            datos = df_filtrado[df_filtrado["titulo"] == receta_elegida].iloc[0]

            tiempo_val = int(datos["tiempo"]) if pd.notna(datos["tiempo"]) else 0
            raciones_base = int(datos["raciones"]) if pd.notna(datos["raciones"]) else 2

            # Ficha superior de la receta con estética de tarjeta Primascore
            st.markdown(
                f"""
            <div class="ps-card">
                <div style="margin-bottom: 0.6rem;">
                    <span class="ps-pill">{datos['categoria']}</span>
                    <span class="ps-pill ps-pill-green">⏱ {tiempo_val} min</span>
                </div>
                <h2 style="margin: 0; font-size: 1.45rem;">{datos['titulo']}</h2>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Selector de raciones
            raciones_deseadas = st.number_input(
                "👥 Ajustar raciones",
                min_value=1,
                max_value=20,
                value=raciones_base,
            )

            if pd.notna(datos["imagen_url"]) and str(datos["imagen_url"]).startswith("http"):
                st.image(datos["imagen_url"], use_container_width=True)

            # Ingredientes con aviso de multiplicador si cambian las raciones
            st.markdown("### 🛒 Ingredientes")
            if raciones_deseadas != raciones_base:
                factor = round(raciones_deseadas / raciones_base, 2)
                st.caption(
                    f"💡 Multiplica las cantidades originales por **x{factor}** (base: {raciones_base} pers.)"
                )

            for idx, linea in enumerate(str(datos["ingredientes"]).split("\n")):
                if linea.strip():
                    st.checkbox(linea.strip(), key=f"ing_{receta_elegida}_{idx}")

            # Tarjeta para los pasos de preparación
            st.markdown("### 👨‍🍳 Preparación")
            pasos_formateados = str(datos["pasos"]).replace("\n", "<br><br>")
            st.markdown(
                f"""
            <div class="ps-card" style="line-height: 1.65; color: #1E293B;">
                {pasos_formateados}
            </div>
            """,
                unsafe_allow_html=True,
            )

# --- PESTAÑA 2: AÑADIR ---
with tab_nueva:
    st.markdown('<div class="ps-card">', unsafe_allow_html=True)
    with st.form("form_receta", clear_on_submit=True):
        titulo = st.text_input("Nombre de la receta *")
        c1, c2, c3 = st.columns(3)
        categoria = c1.selectbox(
            "Categoría",
            ["Plato principal", "Cena rápida", "Desayuno", "Postre", "Salsa/Guarnición"],
        )
        tiempo = c2.number_input("Tiempo (min)", min_value=1, value=30, step=5)
        raciones = c3.number_input("Raciones base", min_value=1, value=2)

        ingredientes = st.text_area(
            "Ingredientes (uno por línea) *",
            height=150,
            placeholder="200g de arroz\n1 pechuga de pollo\nAceite de oliva",
        )
        pasos = st.text_area(
            "Pasos de elaboración *",
            height=200,
            placeholder="1. Cortar el pollo...\n2. Sofreír...",
        )
        imagen_url = st.text_input(
            "URL de imagen (opcional)", placeholder="https://..."
        )

        enviado = st.form_submit_button("Guardar receta", use_container_width=True)

        if enviado:
            if not titulo or not ingredientes or not pasos:
                st.error(
                    "Por favor, rellena al menos el título, los ingredientes y los pasos."
                )
            else:
                nueva_fila = pd.DataFrame(
                    [
                        {
                            "titulo": titulo,
                            "categoria": categoria,
                            "tiempo": tiempo,
                            "raciones": raciones,
                            "ingredientes": ingredientes,
                            "pasos": pasos,
                            "imagen_url": imagen_url,
                        }
                    ]
                )
                df_actualizado = pd.concat(
                    [cargar_recetas(), nueva_fila], ignore_index=True
                )
                conn.update(data=df_actualizado)
                st.success(f"¡'{titulo}' guardada correctamente!")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
