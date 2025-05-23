import streamlit as st
import pandas as pd
from db import get_all_tickets, close_ticket
from ticket import reabrir_ticket  # Asegúrate de importar la función

def mostrar_cabeceras():
    col_widths = [0.4, 1, 2, 1.2, 1.2, 1, 1, 1]
    cols = st.columns(col_widths)
    headers = ["ID", "Título", "Descripción", "Estado", "Usuario", "Departamento", "Fecha", ""]
    for col, header in zip(cols, headers):
        col.markdown(f"<b>{header}</b>", unsafe_allow_html=True)

def mostrar_dashboard(usuario):
    st.subheader("Panel de Tickets")

    filtro = st.selectbox("Filtrar por estado", ["Abiertos", "Cerrados", "Todos"])
    tickets = get_all_tickets(filtro, usuario)

    if not tickets:
        st.info("No hay tickets para mostrar.")
        return

    df = pd.DataFrame(tickets)

    for i, row in df.iterrows():
        col_widths = [0.4, 1, 2, 1.2, 1.2, 1, 1, 1]
        cols = st.columns(col_widths)

        cols[0].markdown(f"<div style='font-weight:bold; font-size:16px'>{row['id']}</div>", unsafe_allow_html=True)
        cols[1].markdown(f"<div style='font-weight:bold; font-size:15px'>{row['titulo']}</div>", unsafe_allow_html=True)
        cols[2].markdown(f"<div style='font-size:14px'>{row['descripcion']}</div>", unsafe_allow_html=True)
        cols[3].markdown(f"<div style='font-size:14px'><b>Estado:</b> {row['estado']}</div>", unsafe_allow_html=True)
        cols[4].markdown(f"<div style='font-size:14px'><b>Usuario:</b> {row['nombre']}</div>", unsafe_allow_html=True)
        cols[5].markdown(f"<div style='font-size:14px'><b>Departamento:</b> {row.get('departamento')}</div>", unsafe_allow_html=True)
        cols[6].markdown(f"{row['fecha']}")

        # Botón en la última columna
        if row['estado'] == 'abierto' and usuario['rol'] == 'admin':
            if cols[7].button(f"Cerrar #{row['id']}", key=f"cerrar_{row['id']}"):
                close_ticket(row['id'])
                st.success(f"Ticket #{row['id']} cerrado exitosamente.")
                st.rerun()
        elif row['estado'] == 'cerrado':
            if cols[7].button(f"Reabrir #{row['id']}", key=f"reabrir_{row['id']}"):
                reabrir_ticket(row['id'])
                st.success(f"Ticket #{row['id']} reabierto exitosamente.")
                st.rerun()
        else:
            cols[7].markdown("")  # Dejar vacío si no corresponde mostrar botón