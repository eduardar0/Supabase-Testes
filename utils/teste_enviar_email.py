import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

from data.connect import supabase as bd

texto = "TEXTO TESTE"  # Botar um Lorem pra testes
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

# HTML com identidade visual GOV INSIGHTS
html_content = f"""
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #ff0000;
            color: #333;
            margin: 0;
            padding: 40px 0;
        }}
        .email-container {{
            max-width: 480px;
            margin: 0 auto;
            background-color: #f3ffff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .logo-container {{
            background-color: #f0f7ff;
            padding: 15px 30px;
            display: flex;
            align-items: center;
        }}
        .logo {{
            width: 80px;  
            height: auto;
        }}
        .content {{
            padding: 30px;
            text-align: left;
        }}
        .title {{
            font-size: 20px;
            color: #1a365d;
            font-weight: bold;
            margin-bottom: 20px;
        }}
        .alert {{
            background-color: #f0f7ff;
            border-left: 5px solid #3182ce;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
        }}
        .variacao {{
            color: #e53e3e;
            font-weight: bold;
            font-size: 18px;
        }}
        .button {{
            display: block;
            width: fit-content;
            margin: 25px auto 0 auto;
            background-color: #3182ce;
            color: white !important;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            text-decoration: none;
        }}
        .footer {{
            font-size: 12px;
            color: #aaa;
            text-align: center;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="logo-container">
            <img src="cid:logo_gov_insights" alt="GOV INSIGHTS" class="logo">
        </div>
        <div class="content">
            <div class="title">Alerta de Variação Econômica</div>
            <div class="alert">
                <p>Série monitorada: <strong>{serie['codigo_serie']}</strong></p>
                <p>Alteração detectada: <span class="variacao">{serie['variacao'] if 'variacao' in serie else 'N/A'}</span></p>
            </div>
            <p>Este alerta foi gerado automaticamente pelo GOV INSIGHTS com base no monitoramento contínuo.</p>
            <ul>
                <li>Consulte detalhes no painel de análise</li>
                <li>Compare com outras séries</li>
                <li>Realize exportação de dados</li>
                <li><strong>Ação recomendada:</strong> em até 48h</li>
            </ul>
            <a href="https://painel.govinsights.com.br/analise?serie={serie['codigo_serie']}" class="button">Ver análise completa</a>
        </div>
        <div class="footer">
            GOV INSIGHTS • SQUAD 10<br>
            Este é um e-mail automático, não responda.<br>
            <a href="https://govinsights.com.br/unsubscribe?email={serie['email_usuario']}" style="color: #888;">Cancelar inscrição</a>
        </div>
    </div>
</body>
</html>
"""

# Criar a mensagem
mensagem = MIMEMultipart()
mensagem['Subject'] = f"Alerta da Série #{serie['codigo_serie']}"
mensagem['From'] = 'govinsightstests@gmail.com'  # Remetente (precisa estar validado na Brevo)
mensagem['To'] = "itsgflyan@gmail.com"
# Email do destinatário

# Corpo da mensagem (HTML estilizado com imagem embutida)
corpo = MIMEText(html_content, 'html')
mensagem.attach(corpo)

# Adicionar imagem do logo (imagem local que será embutida no HTML)
logo_path = 'assets/icon.png'
if os.path.exists(logo_path):
    with open(logo_path, 'rb') as img:
        logo = MIMEImage(img.read())
        logo.add_header('Content-ID', '<logo_gov_insights>')
        mensagem.attach(logo)

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
