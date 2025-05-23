from db import connect_db
from utils import enviar_email
from db import connect_db, get_ticket_info, get_admin_email



def reabrir_ticket(ticket_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Tickets SET estado = 'abierto' WHERE id_ticket = ?", (ticket_id,))
    conn.commit()
    
    # Obtener información del ticket y usuario para el correo
    ticket_info = get_ticket_info(ticket_id)
    admin_email = get_admin_email()
    usuario_email = ticket_info['email_usuario']
    asunto = f"Ticket #{ticket_id} reabierto"
    mensaje = (
        f"El ticket #{ticket_id} ('{ticket_info['titulo']}') ha sido reabierto por el usuario {ticket_info['nombre_usuario']}."
    )
    
    # Enviar correo al admin y al usuario (uno por uno)
    for destinatario in [admin_email, usuario_email]:
        enviar_email(destinatario, asunto, mensaje)
    
    conn.close()
    return True

def create_ticket(titulo, descripcion, id_usuario, email_usuario, email_admin):
    conn = connect_db()
    cursor = conn.cursor()

    # Insertar ticket
    cursor.execute("""
        INSERT INTO Tickets (titulo, descripcion, id_usuario)
        OUTPUT INSERTED.id_ticket
        VALUES (?, ?, ?)
    """, (titulo, descripcion, id_usuario))
    
    row = cursor.fetchone()
    if not row:
        return None

    ticket_id = row[0]

    # Obtener nombre de usuario y departamento
    cursor.execute("""
        SELECT nombre, departamento FROM Usuarios WHERE id_usuario = ?
    """, (id_usuario,))
    user_row = cursor.fetchone()
    if user_row:
        nombre_usuario, departamento = user_row
    else:
        nombre_usuario, departamento = "Desconocido", "Desconocido"

    conn.commit()
    #Cuerpo de email
    cuerpo = (
        f"Se ha creado un nuevo ticket:\n\n"
        f"Código: {ticket_id}\n"
        f"Título: {titulo}\n"
        f"Descripción: {descripcion}\n"
        f"Usuario: {nombre_usuario}\n"
        f"Departamento: {departamento}"
    )
    enviar_email(email_usuario, "Confirmación de Ticket", cuerpo)
    enviar_email(email_admin, "Nuevo Ticket Creado", cuerpo)    

    return ticket_id
