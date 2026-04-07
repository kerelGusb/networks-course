import socket
import base64
import ssl
import uuid

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

sender_email = "dorovskih811@gmail.com"
password = input("input sender password: ")
email_receiver = input("input receiver email: ")
image_path = input("path to image (input '-' if no image): ")

def send(sock, command):
    sock.send((command + "\r\n").encode())


if image_path == "-":
    message = """Subject: some random subject
    
    test mail from smtp client"""
    
else:
    with open(image_path, "rb") as f:
        image_data = f.read()

    image_base64 = base64.b64encode(image_data).decode()

    boundary = str(uuid.uuid4())

    message = f"""Subject: mail with image
    MIME-Version: 1.0
    Content-Type: multipart/mixed; boundary={boundary}

    --{boundary}
    Content-Type: text/plain

    random text

    --{boundary}
    Content-Type: image/jpeg
    Content-Transfer-Encoding: base64
    Content-Disposition: attachment; filename="image.jpg"

    {image_base64}

    --{boundary}--
    """


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SMTP_SERVER, SMTP_PORT))
client_socket.recv(1024)

send(client_socket, "EHLO localhost")
client_socket.recv(1024)

send(client_socket, "STARTTLS")
client_socket.recv(1024)

context = ssl.create_default_context()
client_socket = context.wrap_socket(client_socket, server_hostname=SMTP_SERVER)

send(client_socket, "EHLO localhost")
client_socket.recv(1024)

send(client_socket, "AUTH LOGIN")
client_socket.recv(1024)

send(client_socket, base64.b64encode(sender_email.encode()).decode())
client_socket.recv(1024)

send(client_socket, base64.b64encode(password.encode()).decode())
client_socket.recv(1024)

send(client_socket, f"MAIL FROM:<{sender_email}>")
client_socket.recv(1024)

send(client_socket, f"RCPT TO:<{email_receiver}>")
client_socket.recv(1024)

send(client_socket, "DATA")
client_socket.recv(1024)

send(client_socket, message + "\r\n.")
client_socket.recv(1024)

send(client_socket, "QUIT")

client_socket.close()