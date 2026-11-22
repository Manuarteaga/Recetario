import json
import os
import streamlit as st

st.set_page_config(
    page_title="RecetarioScore | Mi Recetario en Google Sheets",
    page_icon="🍳",
    layout="wide",
)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1P3xFRxy3sAcyTppBdhncn2c_XIxHsbOmaVIeQ6_45KQ/edit"
SHEET_TAB = "Hoja 1"
COLUMNAS_ESPERADAS = ["titulo", "categoría", "tiempo", "raciones", "ingredientes", "pasos"]

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
        .stApp {
            background-color: #090d16;
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }
        .block-container {
            padding-top: 0.75rem;
            padding-bottom: 1.5rem;
            max-width: 1200px;
        }
        header[data-testid="stHeader"] {
            display: none;
        }
        div[data-testid="stExpander"] {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(51, 65, 85, 0.7);
            border-radius: 14px;
            margin-bottom: 12px;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #10b981 0%, #0d9488 100%);
            color: #090d16;
            font-weight: 700;
            border: none;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def obtener_cliente_sheets():
    """Conecta con Google Sheets usando st.secrets['gcp_service_account'] si está configurado."""
    if "gcp_service_account" not in st.secrets:
        return None
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        gc = gspread.authorize(creds)
        sh = gc.open_by_url(SHEET_URL)
        return sh.worksheet(SHEET_TAB)
    except Exception as e:
        st.warning(f"No se pudo conectar con la cuenta de servicio de Google Sheets: {e}")
        return None


def cargar_recetas():
    ws = obtener_cliente_sheets()
    if ws is not None:
        try:
            registros = ws.get_all_records(expected_headers=COLUMNAS_ESPERADAS)
            recetas_limpias = []
            for r in registros:
                if str(r.get("titulo", "")).strip():
                    recetas_limpias.append({
                        "titulo": str(r.get("titulo", "")).strip(),
                        "categoria": str(r.get("categoría", "General")).strip() or "General",
                        "tiempo": str(r.get("tiempo", "")).strip(),
                        "raciones": str(r.get("raciones", "")).strip(),
                        "ingredientes": str(r.get("ingredientes", "")).strip(),
                        "pasos": str(r.get("pasos", "")).strip(),
                    })
            return recetas_limpias, True
        except Exception as e:
            st.error(f"Error leyendo la hoja '{SHEET_TAB}': {e}")

    # Respaldo local en sesión si aún no se han configurado los Secrets
    if "recetas_locales" not in st.session_state:
        st.session_state["recetas_locales"] = [
            {
                "titulo": "Roscón de reyes",
                "categoria": "Postres",
                "tiempo": "3 h (con levados)",
                "raciones": "8",
                "ingredientes": "500 g harina de fuerza\n120 g azúcar\n100 ml leche tibia\n25 g levadura fresca\n2 huevos\n80 g mantequilla\n2 cdas agua de azahar\nRalladura de 1 naranja y 1 limón",
                "pasos": "1. Disolver la levadura en la leche tibia con una cucharada de azúcar.\n2. Mezclar la harina, el resto del azúcar, las ralladuras, los huevos y el agua de azahar.\n3. Amasar e incorporar la mantequilla en pomada hasta lograr una masa lisa.\n4. Dejar levar 2 horas, dar forma de roscón, decorar con fruta escarchada y azúcar humedecido.\n5. Hornear a 180 °C durante 20-25 minutos.",
            }
        ]
    return st.session_state["recetas_locales"], False


recetas, conectado_sheets = cargar_recetas()

# Panel plegable para subir una nueva receta directamente al Google Sheets
with st.expander("➕ Añadir nueva receta al Google Sheets", expanded=False):
    if not conectado_sheets:
        st.info(
            "Modo vista previa activo. Para guardar permanentemente en tu Google Sheets, añade `[gcp_service_account]` en **Settings → Secrets** de Streamlit Cloud y comparte la hoja con el correo de la cuenta de servicio."
        )

    with st.form("form_nueva_receta", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns([2.2, 1.2, 1, 0.8])
        with c1:
            titulo_in = st.text_input("Título de la receta *", placeholder="Ej. Tortilla de patatas jugosa")
        with c2:
            categorias_existentes = sorted(
                list({r["categoria"] for r in recetas if r["categoria"]} | {
                    "Entrantes", "Primeros", "Segundos", "Carnes", "Pescados", "Arroces y Pastas", "Postres", "Desayunos"
                })
            )
            cat_sel = st.selectbox("Categoría", options=categorias_existentes + ["Otra..."])
            cat_otra = st.text_input("Si elegiste 'Otra...', escríbela:", placeholder="Ej. Panadería")
        with c3:
            tiempo_in = st.text_input("Tiempo", placeholder="Ej. 35 min")
        with c4:
            raciones_in = st.text_input("Raciones", placeholder="Ej. 4")

        col_ing, col_pasos = st.columns(2)
        with col_ing:
            ingredientes_in = st.text_area(
                "Ingredientes (uno por línea)",
                height=150,
                placeholder="6 huevos\n700 g patatas\n1 cebolla dulce\nAceite de oliva virgen extra\nSal al gusto",
            )
        with col_pasos:
            pasos_in = st.text_area(
                "Pasos de elaboración (uno por línea)",
                height=150,
                placeholder="1. Pelar y cortar las patatas en láminas finas.\n2. Pochar a fuego medio-bajo con la cebolla.\n3. Batir los huevos, mezclar y cuajar 2 minutos por cada lado.",
            )

        submitted = st.form_submit_button("💾 Guardar receta en el Recetario", type="primary", use_container_width=True)

        if submitted:
            if not titulo_in.strip():
                st.error("El título de la receta es obligatorio.")
            else:
                categoria_final = cat_otra.strip() if (cat_sel == "Otra..." and cat_otra.strip()) else (
                    cat_otra.strip() if cat_sel == "Otra..." else cat_sel
                )
                fila_nueva = [
                    titulo_in.strip(),
                    categoria_final or "General",
                    tiempo_in.strip(),
                    raciones_in.strip(),
                    ingredientes_in.strip(),
                    pasos_in.strip(),
                ]

                ws = obtener_cliente_sheets()
                if ws is not None:
                    try:
                        ws.append_row(fila_nueva, value_input_option="USER_ENTERED")
                        st.success(f"✅ Receta **{titulo_in.strip()}** guardada en tu Google Sheets.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al escribir en Google Sheets: {e}")
                else:
                    st.session_state["recetas_locales"].append({
                        "titulo": fila_nueva[0],
                        "categoria": fila_nueva[1],
                        "tiempo": fila_nueva[2],
                        "raciones": fila_nueva[3],
                        "ingredientes": fila_nueva[4],
                        "pasos": fila_nueva[5],
                    })
                    st.success(f"✅ Receta **{titulo_in.strip()}** añadida a la vista previa.")
                    st.rerun()

# Renderizar la interfaz HTML interactiva del recetario
html_file_path = os.path.join(os.path.dirname(__file__), "index.html")

if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_code = f.read()

    recetas_json = json.dumps(recetas, ensure_ascii=False)
    estado_json = json.dumps({
        "conectado": conectado_sheets,
        "sheet_url": SHEET_URL,
    })

    inyector = f"""
    <script>
        window.RECETAS_DATA = {recetas_json};
        window.SHEET_META = {estado_json};
        if (typeof inicializarRecetario === "function") {{
            inicializarRecetario();
        }}
    </script>
    </body>
    """

    html_final = html_code.replace("</body>", inyector)
    st.components.v1.html(html_final, height=1150, scrolling=True)
else:
    st.error("No se encuentra el archivo 'index.html'. Súbelo a GitHub junto con 'app.py'.")
