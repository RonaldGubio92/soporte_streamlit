import streamlit as st
from datetime import datetime
import os

# --- Estilo CSS personalizado ---
st.markdown("""
    <style>
        .main {
            background-color: #f4f6f9;
        }
        .stTextInput > div > div > input {
            border: 1px solid #ccc;
            padding: 10px;
        }
        .stTextArea textarea {
            border: 1px solid #ccc;
            padding: 10px;
        }
        .titulo-principal {
            font-size: 30px;
            font-weight: bold;
            color: #003366;
        }
        .separador {
            border-top: 1px solid #ccc;
            margin-top: 25px;
            margin-bottom: 25px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Título principal ---
st.markdown('<div class="titulo-principal">🛠️ Registro de Incidente de Soporte Técnico</div>', unsafe_allow_html=True)
st.caption("Por favor, completa el siguiente formulario para registrar tu solicitud.")

# --- Formulario con diseño por columnas ---
with st.form("form_incidente"):

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("👤 Nombre completo", placeholder="Ej. Juan Pérez")
        departamento = st.selectbox("🏢 Departamento", ["Sistemas", "Contabilidad", "Ventas", "Logística", "Otro"])
        prioridad = st.radio("⚠️ Nivel de prioridad", ["Baja", "Media", "Alta"], horizontal=True)

    with col2:
        correo = st.text_input("📧 Correo electrónico", placeholder="Ej. juan@example.com")
        fecha = st.date_input("📅 Fecha del incidente", value=datetime.today())

    st.markdown('<div class="separador"></div>', unsafe_allow_html=True)

    descripcion = st.text_area("📝 Descripción del incidente", height=150, placeholder="Describe el problema con el mayor detalle posible...")

    archivo = st.file_uploader("📎 Adjuntar evidencia (opcional)", type=["png", "jpg", "jpeg", "pdf", "docx", "xlsx"])

    st.markdown('<div class="separador"></div>', unsafe_allow_html=True)

    enviar = st.form_submit_button("🚀 Enviar solicitud")

# --- Procesamiento al enviar ---
if enviar:
    if not nombre or not correo or not descripcion:
        st.error("❌ Por favor completa los campos obligatorios.")
    else:
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.success("✅ ¡Solicitud enviada con éxito!")

        with st.expander("📄 Ver resumen del incidente"):
            st.write(f"**📅 Fecha y hora de envío:** {fecha_hora}")
            st.write(f"**👤 Nombre:** {nombre}")
            st.write(f"**📧 Correo:** {correo}")
            st.write(f"**🏢 Departamento:** {departamento}")
            st.write(f"**⚠️ Prioridad:** {prioridad}")
            st.write(f"**📝 Descripción:** {descripcion}")
            st.write(f"**📁 Fecha del incidente:** {fecha}")

            if archivo:
                carpeta_destino = "adjuntos"
                os.makedirs(carpeta_destino, exist_ok=True)
                ruta_archivo = os.path.join(carpeta_destino, archivo.name)
                with open(ruta_archivo, "wb") as f:
                    f.write(archivo.read())
                st.info(f"📎 Archivo guardado en: `{ruta_archivo}`")
                if archivo.type.startswith("image/"):
                    st.image(ruta_archivo, caption="Vista previa del archivo", use_column_width=True)
                else:
                    st.download_button("⬇️ Descargar archivo", data=open(ruta_archivo, "rb"), file_name=archivo.name)

