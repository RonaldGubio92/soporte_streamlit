import pyodbc
from datetime import datetime

def connect_db():
    return pyodbc.connect(
        'DRIVER={SQL Server};SERVER=SQL5105.site4now.net;DATABASE=db_a56ecc_enedb;UID=db_a56ecc_enedb_admin;PWD=enedPassword524152'
    )

def get_user(usuario, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Usuarios 
        WHERE usuario = ? AND password = ? AND estado = 'activo'
    """, (usuario, password))
    row = cursor.fetchone()
    if row:
        return {
            'id': row.id_usuario,
            'nombre': row.nombre,
            'rol': row.rol,
            'email': row.email,
            'departamento': row.departamento,
            'estado': row.estado
        }
    return None



def get_admin_email():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 email FROM Usuarios WHERE rol = 'admin'")
    row = cursor.fetchone()
    return row.email if row else None

def get_all_tickets(filtro, usuario):
    conn = connect_db()
    cursor = conn.cursor()
    
    where = ""
    params = []

    # Solo filtrar por usuario si NO es admin y quieres que los técnicos vean solo sus tickets
    # Si quieres que los técnicos vean todos los tickets abiertos, elimina este filtro:
    
    # if usuario['rol'] == 'tecnico':
    #     where += " WHERE T.id_usuario = ?"
    #     params.append(usuario['id'])

    if usuario['rol'] == 'usuario':
        where += " WHERE T.id_usuario = ?"
        params.append(usuario['id'])

    if filtro == "Abiertos":
        where += " AND" if where else " WHERE"
        where += " T.estado = 'abierto'"
    elif filtro == "Cerrados":
        where += " AND" if where else " WHERE"
        where += " T.estado = 'cerrado'"

    query = f"""
        SELECT T.id_ticket, T.titulo, T.descripcion, T.estado, U.nombre, u.departamento, t.fecha_creacion
        FROM Tickets T
        JOIN Usuarios U ON T.id_usuario = U.id_usuario
        {where}
        ORDER BY T.id_ticket DESC
    """
    cursor.execute(query, params)
    rows = cursor.fetchall()

    return [
        {'id': row.id_ticket, 
         'titulo': row.titulo, 
         'descripcion': row.descripcion,
         'estado': row.estado, 
         'nombre': row.nombre ,
        'departamento': row.departamento, 
         'fecha': row.fecha_creacion.strftime('%Y-%m-%d %H:%M')}
        for row in rows
    ]

def close_ticket(id_ticket):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Tickets SET estado = 'cerrado', fecha_cierre = ? WHERE id_ticket = ?",
        (datetime.now(), id_ticket)
    )
    conn.commit()
    conn.close()



def get_ticket_info(ticket_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT T.id_ticket, T.titulo, T.descripcion, U.nombre as nombre_usuario, U.email as email_usuario
        FROM Tickets T
        JOIN Usuarios U ON T.id_usuario = U.id_usuario
        WHERE T.id_ticket = ?
    """, (ticket_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        # Ajusta los índices si el orden de los SELECT cambia
        return {
            'id_ticket': row[0],
            'titulo': row[1],
            'descripcion': row[2],
            'nombre_usuario': row[3],
            'email_usuario': row[4]
        }
    return None