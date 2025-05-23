import streamlit as st
from auth import login
from ticket import create_ticket
from dashboard import mostrar_dashboard
from usuarios import gestionar_usuarios
from db import get_admin_email
import os
import base64
from estadisticas import mostrar_dashboard_estadistico


def base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

st.set_page_config(page_title="Mesa de Ayuda", layout="wide")



# Aplica estilos personalizados a los botones sin afectar la barra superior de Streamlit
st.markdown("""
    <style>
        /* Aplica estilos a los inputs */
        .stTextInput > div > div > input {
            border-radius: 4px;
            padding: 10px;
        }
        /* Aplica estilos a los botones principales */
        .stButton > button, .stButton button {
            background-color: #997b74 !important;
            color: white !important;
            padding: 10px 16px !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            width: 100% !important;
            margin-top: 10px !important;
        }
        .stButton > button:hover, .stButton button:hover {
            background-color: #45a049 !important;
        }
    </style>
""", unsafe_allow_html=True)




#logotipo de la marca 
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.markdown(f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{base64_image(logo_path)}" width="150">
        </div>
    """, unsafe_allow_html=True)



#st.title("📌 Mesa de Ayuda")

# Estado de sesión
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = None

# Inicio de sesión
if not st.session_state['logged_in']:
    login()
else:
    user = st.session_state['usuario']
    st.sidebar.title(f"👤 Bienvenido:  {user['nombre']}")

    # Menú lateral dinámico y dar permisos según rol
    if user['rol'] == 'admin':
        opcion = st.sidebar.radio("Opciones", ["Crear Ticket", "Ver Tickets", "Gestionar Usuarios", "Dashboard Estadístico", "Cerrar Sesión"])
    else:
        opcion = st.sidebar.radio("Opciones", ["Crear Ticket", "Ver Tickets", "Cerrar Sesión"])

    # Crear ticket
    if opcion == "Crear Ticket":
        st.subheader("🆕 Crear nuevo ticket")
        st.info(f"Ticket creado por: {user['nombre']} ({user['rol']}, {user.get('departamento', 'Sin departamento')})")

        titulo = st.text_input("Título del ticket")
        descripcion = st.text_area("Descripción del problema")

        if st.button("Crear Ticket"):
            if titulo and descripcion:
                ticket_id = create_ticket(
                    titulo, descripcion,
                    user['id'], user['email'], get_admin_email()
                )
                if ticket_id:
                    st.success(f"✅ Ticket #{ticket_id} creado exitosamente")
                else:
                    st.error("❌ Error al crear el ticket")
            else:
                st.warning("⚠️ Todos los campos son obligatorios")

    # Ver dashboard de tickets
    elif opcion == "Ver Tickets":
        mostrar_dashboard(user)

    # Gestión de usuarios (solo admin)
    elif opcion == "Gestionar Usuarios":
        gestionar_usuarios()
    #Gestión de estadísticas (solo admin)
    elif opcion == "Dashboard Estadístico":
        mostrar_dashboard_estadistico()

    # Cerrar sesión
    elif opcion == "Cerrar Sesión":
        st.session_state['logged_in'] = False
        st.session_state['usuario'] = None
        st.rerun()
