import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Rouuse Beauty - Notas", page_icon="🌸", layout="centered")

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

def limpiar_texto(texto):
    return str(texto).encode("latin-1", "replace").decode("latin-1")

def crear_pdf_estetico(numero, cliente, celular, fecha, productos, total):
    pdf = FPDF(orientation="P", unit="mm", format="Letter")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Fondo suave y tarjeta principal blanca con borde rosa
    pdf.set_fill_color(255, 251, 252)
    pdf.rect(0, 0, 216, 279, style="F")
    
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(243, 213, 220)
    pdf.set_line_width(0.6)
    pdf.rect(12, 12, 192, 255, style="DF", round_corners=True, corner_radius=6)

    # Encabezado Marca
    pdf.set_xy(20, 22)
    pdf.set_font("Times", "B", 26)
    pdf.set_text_color(136, 60, 82)
    pdf.cell(100, 10, "K & G", new_x="LMARGIN", new_y="NEXT")

    pdf.set_x(20)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(197, 139, 153)
    pdf.cell(100, 5, "SKINCARE & BEAUTY BOUTIQUE")

    # Insignia N° de Nota
    pdf.set_fill_color(253, 242, 245)
    pdf.set_draw_color(241, 203, 213)
    pdf.rect(135, 22, 60, 11, style="DF", round_corners=True, corner_radius=5)
    pdf.set_xy(135, 23)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(158, 71, 96)
    pdf.cell(60, 9, limpiar_texto(f"Nota de Venta Nro. {numero}"), align="C")

    # Línea divisoria
    pdf.set_draw_color(248, 228, 233)
    pdf.line(20, 42, 196, 42)

    # Caja de Datos Clienta
    pdf.set_fill_color(253, 248, 249)
    pdf.set_draw_color(247, 230, 234)
    pdf.rect(20, 48, 176, 22, style="DF", round_corners=True, corner_radius=4)

    pdf.set_xy(25, 52)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(136, 60, 82)
    pdf.cell(18, 6, "Clienta:")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(92, 67, 74)
    pdf.cell(85, 6, limpiar_texto(cliente))

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(136, 60, 82)
    pdf.cell(15, 6, "Fecha:")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(92, 67, 74)
    pdf.cell(45, 6, limpiar_texto(fecha), align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.set_x(25)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(136, 60, 82)
    pdf.cell(18, 6, "Celular:")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(92, 67, 74)
    pdf.cell(85, 6, limpiar_texto(celular))

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(136, 60, 82)
    pdf.cell(15, 6, "Lugar:")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(92, 67, 74)
    pdf.cell(45, 6, "La Paz, Bolivia", align="R", new_x="LMARGIN", new_y="NEXT")

    # Cabecera Tabla
    pdf.set_xy(20, 78)
    pdf.set_fill_color(249, 235, 239)
    pdf.set_text_color(136, 60, 82)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(18, 10, "CANT.", fill=True, align="C")
    pdf.cell(98, 10, "PRODUCTO / TRATAMIENTO", fill=True, align="L")
    pdf.cell(30, 10, "P. UNIT.", fill=True, align="R")
    pdf.cell(30, 10, "SUBTOTAL", fill=True, align="R", new_x="LMARGIN", new_y="NEXT")

    # Filas de Productos
    pdf.set_font("Helvetica", "", 10)
    for item in productos:
        pdf.set_x(20)
        pdf.set_text_color(74, 53, 59)
        pdf.cell(18, 10, str(item["cant"]), border="B", align="C")
        pdf.cell(98, 10, limpiar_texto(item["desc"][:48]), border="B", align="L")
        pdf.cell(30, 10, f"Bs. {item['precio']}", border="B", align="R")
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(136, 60, 82)
        pdf.cell(30, 10, f"Bs. {item['subtotal']}", border="B", align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)

    # Caja Total
    pdf.ln(10)
    y_total = pdf.get_y()
    pdf.set_fill_color(158, 71, 96)
    pdf.rect(126, y_total, 70, 12, style="F", round_corners=True, corner_radius=4)
    pdf.set_xy(126, y_total)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(70, 12, f"TOTAL: Bs. {total}", align="C", new_x="LMARGIN", new_y="NEXT")

    # Pie de página
    pdf.set_y(242)
    pdf.set_font("Times", "I", 12)
    pdf.set_text_color(158, 71, 96)
    pdf.cell(0, 6, "Gracias por confiar el cuidado de tu piel en nosotros", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(176, 137, 147)
    pdf.cell(0, 5, "K&G BEAUTY  -  PRODUCTOS ORIGINALES", align="C")

    return bytes(pdf.output())

# --- INTERFAZ WEB ---
st.title("✨ K&G Skincare & Beauty ✨")
st.caption("Generador de Notas de Venta")

if "productos" not in st.session_state:
    st.session_state.productos = []

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        numero = st.text_input("N° Nota", value="001")
    with col2:
        celular = st.text_input("N° de Celular", placeholder="Ej. 70012345")
    cliente = st.text_input("Nombre de la Clienta", placeholder="Ej. María Pérez")

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

    pdf_bytes = crear_pdf_estetico(
        numero=numero or "001",
        cliente=cliente or "Clienta Especial",
        celular=celular or "Sin registrar",
        fecha=datetime.now().strftime("%d/%m/%Y"),
        productos=st.session_state.productos,
        total=f"{total:.2f}"
    )

    st.download_button(
        label="📄 Descargar Nota de Venta PDF",
        data=pdf_bytes,
        file_name=f"Nota_KG_{numero or '001'}.pdf",
        mime="application/pdf"
    )

    if st.button("🔄 Limpiar todo para nueva venta"):
        st.session_state.productos = []
        st.rerun()
