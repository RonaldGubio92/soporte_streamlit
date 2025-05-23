import pymssql
from datetime import datetime

def connect_db():
    return pymssql.connect(
        server=st.secrets["database"]["server"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        database=st.secrets["database"]["database"]
    )

def get_user(usuario, password):
    conn = connect_db()
    cursor = conn.cursor(as_dict=True)  # cursor devuelve dicts para mayor comodidad
    cursor.execute("""
        SELECT * FROM Usuarios 
        WHERE usuario = %s AND password = %s AND estado = 'activo'
    """, (usuario, password))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'id': row['id_usuario'],
            'nombre': row['nombre'],
            'rol': row['rol'],
            'email': row['email'],
            'departamento': row['departamento'],
            'estado': row['estado']
        }
    return None

def get_admin_email():
    conn = connect_db()
    cursor = conn.cursor(as_dict=True)
    cursor.execute("SELECT TOP 1 email FROM Usuarios WHERE rol = 'admin'")
    row = cursor.fetchone()
    conn.close()
    return row['email'] if row else None

def get_all_tickets(filtro, usuario):
    conn = connect_db()
    cursor = conn.cursor(as_dict=True)

    where = ""
    params = []

    if usuario['rol'] == 'usuario':
        where += " WHERE T.id_usuario = %s"
        params.append(usuario['id'])

    if filtro == "Abiertos":
        where += " AND" if where else " WHERE"
        where += " T.estado = 'abierto'"
    elif filtro == "Cerrados":
        where += " AND" if where else " WHERE"
        where += " T.estado = 'cerrado'"

    query = f"""
        SELECT T.id_ticket, T.titulo, T.descripcion, T.estado, U.nombre, U.departamento, T.fecha_creacion
        FROM Tickets T
        JOIN Usuarios U ON T.id_usuario = U.id_usuario
        {where}
        ORDER BY T.id_ticket DESC
    """
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            'id': row['id_ticket'],
            'titulo': row['titulo'],
            'descripcion': row['descripcion'],
            'estado': row['estado'],
            'nombre': row['nombre'],
            'departamento': row['departamento'],
            'fecha': row['fecha_creacion'].strftime('%Y-%m-%d %H:%M')
        }
        for row in rows
    ]

def close_ticket(id_ticket):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Tickets SET estado = 'cerrado', fecha_cierre = %s WHERE id_ticket = %s",
        (datetime.now(), id_ticket)
    )
    conn.commit()
    conn.close()

def get_ticket_info(ticket_id):
    conn = connect_db()
    cursor = conn.cursor(as_dict=True)
    cursor.execute("""
        SELECT T.id_ticket, T.titulo, T.descripcion, U.nombre as nombre_usuario, U.email as email_usuario
        FROM Tickets T
        JOIN Usuarios U ON T.id_usuario = U.id_usuario
        WHERE T.id_ticket = %s
    """, (ticket_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'id_ticket': row['id_ticket'],
            'titulo': row['titulo'],
            'descripcion': row['descripcion'],
            'nombre_usuario': row['nombre_usuario'],
            'email_usuario': row['email_usuario']
        }
    return None
