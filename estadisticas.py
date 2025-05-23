import streamlit as st
import pandas as pd
import plotly.express as px
from db import connect_db

def cargar_tickets():
    conn = connect_db()
    query = """
        SELECT T.id_ticket, T.titulo, T.estado, T.fecha_creacion, T.fecha_cierre, U.nombre as usuario, U.departamento
        FROM Tickets T
        JOIN Usuarios U ON T.id_usuario = U.id_usuario
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def calcular_tiempo_respuesta(row):
    if pd.notnull(row['fecha_cierre']):
        return (row['fecha_cierre'] - row['fecha_creacion']).total_seconds() / 3600  # horas
    return None

def mostrar_dashboard_estadistico():
    st.title("📊 Dashboard Estadístico de Tickets")

    df = cargar_tickets()
    if df.empty:
        st.info("No hay datos de tickets para mostrar.")
        return

    # Convertir fechas a datetime si es necesario
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])

    # Filtros por fecha y departamento
    st.sidebar.header("Filtros")
    min_fecha = df['fecha_creacion'].min().date()
    max_fecha = df['fecha_creacion'].max().date()
    fecha_inicio = st.sidebar.date_input(
        "Fecha desde",
        value=min_fecha,
        min_value=min_fecha,
        max_value=max_fecha
    )
    fecha_fin = st.sidebar.date_input(
        "Fecha hasta",
        value=max_fecha,
        min_value=min_fecha,
        max_value=max_fecha
    )
    departamentos = df['departamento'].unique()
    departamento_sel = st.sidebar.multiselect(
        "Departamento",
        options=departamentos,
        default=list(departamentos)
    )

    # Aplicar filtros
    mask = (
        (df['fecha_creacion'].dt.date >= fecha_inicio) &
        (df['fecha_creacion'].dt.date <= fecha_fin) &
        (df['departamento'].isin(departamento_sel))
    )
    df = df[mask]
    df['fecha_cierre'] = pd.to_datetime(df['fecha_cierre'])

    # 1. Tickets por estado (Gráfico de barras con colores personalizados)
    st.subheader("Tickets por Estado")
    estado_counts = df['estado'].value_counts().reset_index()
    estado_counts.columns = ['Estado', 'Cantidad']
    colores_estado = {
        'abierto': "#65a6d4",   # azul
        'cerrado': "#90d490",   # verde
        'en proceso': '#ff7f0e',# naranja
        # Agrega más estados y colores si tienes más
    }
    fig_estado = px.bar(
        estado_counts,
        x='Estado',
        y='Cantidad',
        color='Estado',
        color_discrete_map=colores_estado,
        text='Cantidad'
    )
    fig_estado.update_layout(showlegend=False)
    st.plotly_chart(fig_estado, use_container_width=True)

    # 2. Tiempo de respuesta promedio (solo tickets cerrados)
    st.subheader("Tiempo de Respuesta Promedio (horas)")
    df['tiempo_respuesta'] = df.apply(calcular_tiempo_respuesta, axis=1)
    df_cerrados = df[df['estado'] == 'cerrado'].dropna(subset=['tiempo_respuesta'])
    if not df_cerrados.empty:
        st.metric("Promedio de respuesta (cerrados)", f"{df_cerrados['tiempo_respuesta'].mean():.2f} horas")
        st.metric("Mediana de respuesta (cerrados)", f"{df_cerrados['tiempo_respuesta'].median():.2f} horas")
        # Puedes agregar un gráfico de líneas si lo deseas:
        # st.line_chart(df_cerrados[['fecha_cierre', 'tiempo_respuesta']].set_index('fecha_cierre'))
    else:
        st.info("No hay tickets cerrados para calcular tiempos de respuesta.")

    # 3. Tickets por departamento (Gráfico de barras agrupado por estado y colores personalizados)
    st.subheader("Tickets por Departamento")
    dept_estado_counts = df.groupby(['departamento', 'estado']).size().reset_index(name='Cantidad')
    fig_dept = px.bar(
        dept_estado_counts,
        x='departamento',
        y='Cantidad',
        color='estado',
        barmode='group',
        color_discrete_map=colores_estado,
        text='Cantidad'
    )
    fig_dept.update_layout(showlegend=True)
    st.plotly_chart(fig_dept, use_container_width=True)

    # 4. Tabla simple de tickets
    st.subheader("Detalle de Tickets")
    st.dataframe(df[['id_ticket', 'titulo', 'usuario', 'departamento', 'estado', 'fecha_creacion', 'fecha_cierre', 'tiempo_respuesta']])

if __name__ == "__main__":
    mostrar_dashboard_estadistico()