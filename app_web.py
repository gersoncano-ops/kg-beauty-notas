import streamlit as st
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime

st.set_page_config(page_title="K&G Beauty - Notas", page_icon="🌸", layout="centered")

# Estilo visual femenino para la app en el celular
st.markdown("""
    <style>
    .stApp { background-color: #fff5f7; }
    h1 { color: #883c52 !important; text-align: center; font-family: 'Georgia', serif; }
    .stButton>button {
        background-color: #9e4760;
        color: white;
        border-radius: 20px;
        border: none;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover { background-color: #7d3348; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("✨ K&G Skincare & Beauty ✨")
st.caption("Generador de Notas de Venta")

if "productos" not in st.session_state:
    st.session_state.productos = []

# --- Datos de la Clienta ---
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        numero = st.text_input("N° Nota", value="001")
    with col2:
        celular = st.text_input("N° de Celular", placeholder="Ej. 70012345")
    cliente = st.text_input("Nombre de la Clienta", placeholder="Ej. María Pérez")

# --- Agregar Productos ---
with st.container(border=True):
    st.subheader("🌸 Agregar Producto")
    c1, c2 = st.columns([1, 2])
    with c1:
        cant = st.number_input("Cant.", min_value=1, value=1, step=1)
    with c2:
        precio = st.number_input("Precio (Bs)", min_value=0.0, value=50.0, step=5.0)
    desc = st.text_input("Crema / Tratamiento", placeholder="Ej. Sérum Ácido Hialurónico")

    if st.button("+ Añadir a la Nota"):
        if desc.strip():
            subtotal = cant * precio
            st.session_state.productos.append({
                "cant": int(cant),
                "desc": desc.strip(),
                "precio": f"{precio:.2f}",
                "subtotal": f"{subtotal:.2f}"
            })
            st.success(f"Agregado: {cant}x {desc}")
        else:
            st.warning("Escribe el nombre del producto.")

# --- Lista de productos agregados ---
if st.session_state.productos:
    st.markdown("### 🛍️ Resumen de la Nota")
    total = 0.0
    for idx, item in enumerate(st.session_state.productos):
        col_txt, col_del = st.columns([4, 1])
        col_txt.write(f"**{item['cant']}x** {item['desc']} — **Bs. {item['subtotal']}**")
        if col_del.button("🗑️", key=f"del_{idx}"):
            st.session_state.productos.pop(idx)
            st.rerun()
        total += float(item["subtotal"])

    st.markdown(f"#### Total a Pagar: **Bs. {total:.2f}**")

    # Generar PDF en memoria
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("plantilla.html")
    html_renderizado = template.render(
        numero=numero or "001",
        cliente=cliente or "Clienta Especial",
        celular=celular or "Sin registrar",
        fecha=datetime.now().strftime("%d/%m/%Y"),
        productos=st.session_state.productos,
        total=f"{total:.2f}"
    )
    pdf_bytes = HTML(string=html_renderizado).write_pdf()

    st.download_button(
        label="📄 Descargar Nota de Venta PDF",
        data=pdf_bytes,
        file_name=f"Nota_KG_{numero or '001'}.pdf",
        mime="application/pdf"
    )

    if st.button("🔄 Limpiar todo para nueva venta"):
        st.session_state.productos = []
        st.rerun()