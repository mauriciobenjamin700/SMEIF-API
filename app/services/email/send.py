from decouple import config
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP


SMTP_SERVER = config("SMTP_SERVER")
SMTP_PORT = config("SMTP_PORT")
EMAIL_USERNAME = config("EMAIL_USERNAME")
EMAIL_PASSWORD = config("EMAIL_PASSWORD")


def send_email(to_email: str, msg: MIMEMultipart) -> str:
    """
    Envia um email para um email de destino

    - Args:
        - to_email (str): Email do destinatário
        - msg (MIMEMultipart): Email formatado para envio

    - Returns:
        - None
    """
    try:
        """
        Cria uma instância do objeto SMTP e conecta ao servidor SMTP especificado pelo endereço (smtp_server) e porta (smtp_port).
        """
        server = SMTP(SMTP_SERVER, SMTP_PORT)
        """
        Inicia a comunicação TLS (Transport Layer Security) para criptografar a conexão ao servidor SMTP, garantindo a segurança dos dados transmitidos.
        """
        server.starttls()

        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

        """
        Envia o email usando o método sendmail do objeto SMTP.
            from_email: O endereço de email do remetente.
            to_email: O endereço de email do destinatário.
            msg.as_string(): Converte o objeto de mensagem (msg) para uma string f
        """
        server.sendmail(EMAIL_USERNAME, to_email, msg.as_string().encode('utf-8'))
        """
        Encerra a conexão com o servidor SMTP.
        """
        server.quit()

        msg = f"Email enviado com sucesso para {to_email}"

        print(msg)

        return msg
    except Exception as e:
        
        msg = f"Falha ao enviar email: {e}"

        print(msg)

        raise Exception(msg)