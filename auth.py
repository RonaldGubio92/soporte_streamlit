import streamlit as st
from db import get_user

def login():
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        user = get_user(usuario, password)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['usuario'] = user
            st.rerun()
        else:
            st.error("Credenciales incorrectas o usuario inactivo.")
