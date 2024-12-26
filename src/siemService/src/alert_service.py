# src/alert_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from . import config 

conf = config.Config()

class AlertService:
    #Serviço de envio de alertas
    def __init__(self, sender=conf.EMAIL_SENDER, recipient=conf.EMAIL_RECIPIENT):
        self.sender = sender
        self.recipient = recipient

    def enviar_alerta(self, usuario, motivo):
        #Envia um alerta sobre uma atividade anômala detectada

        mensagem = self._formatar_mensagem(usuario, motivo)

        try:
            self._enviar_email(mensagem)
            print(f"Alerta enviado com sucesso para {self.recipient}.")
        except Exception as e:
            print(f"Erro ao enviar alerta: {e}")

    def _formatar_mensagem(self, usuario, motivo):
        #Formata a mensagem do alerta

        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Subject'] = f"Alerta de Anomalia - Usuário: {usuario}"

        corpo = (
            f"Uma atividade suspeita foi detectada:\n\n"
            f"- Usuário: {usuario}\n"
            f"- Motivo: {motivo}\n\n"
            "Por favor, verifique o sistema imediatamente."
        )
        msg.attach(MIMEText(corpo, 'plain'))
        return msg

    def _enviar_email(self, mensagem):
        #Envia um e-mail usando as configurações SMTP

        with smtplib.SMTP(conf.SMTP_SERVER, conf.SMTP_PORT) as server:
            server.starttls()
            server.login(self.sender, conf.EMAIL_PASSWORD)
            server.send_message(mensagem)


