import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtp_server = "smtp.gmail.com"
port = 587
email_sender = "dorovskih811@gmail.com"
password = input("input sender password: ")
email_receiver = input("input receiver email: ")

message = MIMEMultipart()
message["From"] = email_sender
message["To"] = email_receiver
message["Subject"] = "test"

print("Choose message format:")
print("1 - txt")
print("2 - html")
message_type = int(input(": "))
print(message_type)
if message_type == 1:
    message_text = """some message"""

    message.attach(MIMEText(message_text, "plain"))

elif message_type == 2:
    message_text = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        <p>some message in html format</p>
    </body>
    </html>"""
    
    message.attach(MIMEText(message_text, "html"))
else:
    print("invalid option")
    exit(0)

try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(email_sender, password)
    
    server.send_message(message)
    server.quit()
    
    print("Письмо отправлено!")
    
except Exception as ошибка:
    print(f"Ошибка: {ошибка}")