import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from data.connect import supabase as bd

texto = "TEXTO TESTE"
posicao = 1

# Pegar série específica do Supabase
seriesBD = bd.table("series").select("*").execute()
seriesBD = seriesBD.data
serie = seriesBD[posicao]

# Configuração SMTP da Brevo
smtp_server = "smtp-relay.brevo.com"
smtp_port = 587
smtp_login = "905867001@smtp-brevo.com"  # Login SMTP da Brevo
smtp_password = "h92HcFkdMgUwVySJ"        # Sua SMTP Key

# Criar a mensagem
mensagem = MIMEMultipart()
mensagem['Subject'] = f"Alerta da Série {serie['codigo_serie']}"
mensagem['From'] = 'govinsightstests@gmail.com'  # Remetente (precisa estar validado na Brevo)
mensagem['To'] = serie["email_usuario"]

# Corpo da mensagem (pode ser HTML ou plain text)
corpo = MIMEText(texto, 'html')
mensagem.attach(corpo)

# Enviar o e-mail
try:
    servidor = smtplib.SMTP(smtp_server, smtp_port)
    servidor.starttls()
    servidor.login(smtp_login, smtp_password)
    servidor.sendmail(mensagem['From'], [mensagem['To']], mensagem.as_string())
    print("E-mail enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar e-mail: {e}")
finally:
    servidor.quit()
