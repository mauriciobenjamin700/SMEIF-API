from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from decouple import config
EMAIL_USERNAME = config("EMAIL_USERNAME")


def generate_email_body_with_password(password: str) -> str:
    """
    Gera o corpo do email com a senha

    - Args:
        - password (str): Senha a ser enviada por email

    - Returns:
        - str: Corpo do email
    """

    html = f"""
    <html>
    <body>
        <p>Este e-mail foi gerado automaticamente para recuperar sua senha, recomendamos que acesse com a senha a baixo e a substitua por uma senha nova e segura.</p>
        <p>Sua nova senha é: <span style="color: blue;">{password}</span></p>
    </body>
    </html>
    """

    return html


def generate_email(to_email: str, subject: str, body: str) -> MIMEMultipart:
    """
    Formata conteúdo para formar um email

    - Args:
        - to_email (str): Email do destinatário
        - subject (str): Assunto do email
        - body (str): Corpo do email

    - Returns:
        - MIMEMultipart: Email formatado para envio
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject
    #msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(body, 'html'))
    return msg