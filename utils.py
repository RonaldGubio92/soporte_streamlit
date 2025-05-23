import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración del correo
smtp_servidor = "mail.crait.com.ec"
smtp_puerto = 465
correo_origen = "r.gubio@crait.com.ec"
contrasena = "PpK{EA(uI9Zs"
def enviar_email(destinatario, asunto, cuerpo):
    try:
        # Crear el mensaje MIME
        msg = MIMEMultipart()
        msg['From'] = correo_origen
        msg['To'] = destinatario
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo, 'plain'))

        # Conectarse al servidor SMTP usando SSL
        servidor = smtplib.SMTP_SSL(smtp_servidor, smtp_puerto)
        servidor.ehlo()
        servidor.login(correo_origen, contrasena)

        # Enviar el correo
        servidor.sendmail(correo_origen, destinatario, msg.as_string())
        servidor.quit()
        print("Correo enviado exitosamente a:", destinatario)
        return True  # Confirmación de envío exitoso
    except Exception as e:
        print(f"Error al enviar email: {e}")
        return False  # Envío fallido
