import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.modules.rundeck import Rundeck  # Importa a classe Rundeck
from src.shared.services.azure_keyvault_service import AzureKeyvaultService  # Importa o serviço Azure Key Vault

class sendEmail:
    def __init__(self) -> None:
        # Inicializa a classe de envio de e-mail
        keyvault = AzureKeyvaultService()
        self.PASSWORDNOREPLY = keyvault.get_kv_secret("PASSWORD-NOREPLY")  # Obtém a senha do Azure Key Vault

    def execute(self) -> None:
        # Inicializa o cliente Rundeck
        rundeck = Rundeck()

        # Obtém informações sobre trabalhos com erros e trabalhos em execução do Rundeck
        jobs_com_erros = rundeck.jobs_status_error()
        jobs_rodando = rundeck.jobs_rodando()

        # Configurações do servidor SMTP do Outlook
        smtp_server = 'smtp.office365.com'
        smtp_port = 587

        # Informações da conta do remetente
        remetente_email = 'emailnoreplay'
        remetente_senha = self.PASSWORDNOREPLY

        # Lista de destinatários (vários e-mails)
        destinatario_email = ['email1', 'email2', 'email3', 'emailn']

        # Criação da mensagem em formato MIME
        mensagem = MIMEMultipart()
        mensagem['From'] = remetente_email
        mensagem['To'] = ', '.join(destinatario_email)
        mensagem['Subject'] = 'Relatório Diário - Jobs do Rundeck'

        # Criação de tabelas em HTML para os trabalhos com erros e em execução
        # As informações são extraídas dos resultados do Rundeck
        # As tabelas são formatadas em HTML para inclusão no e-mail
        # Você pode personalizar o HTML conforme necessário

        tabela_jobs_com_erros = """
        <h2>Jobs com Erros:</h2>
        <table border="2" align="center">
            <tr align="center">
                <th align="center">ID</th>
                <th align="center">Nome</th>
                <th align="center">Link do Erro</th>
                <th align="center">Data de Início</th>
                <th align="center">Data Final</th>
            </tr>
            {linhas_jobs_com_erros}
        </table>
        """

        linhas_jobs_com_erros = ""
        for job in jobs_com_erros:
            linhas_jobs_com_erros += f"""
            <tr align="center">
                <td align="center">{job['ID']}</td>
                <td align="center">{job['NAME']}</td>
                <td align="center"><a href="{job['PERMLINK']}">Erro</a></td>
                <td align="center">{job['DATA_INIT']}</td>
                <td align="center">{job['DATA_END']}</td>
            </tr>
            """

        # Loop para construir a tabela com os jobs rodando
        tabela_jobs_rodando = """
        <h2>Jobs Rodando:</h2>
        <table border="2" align="center">
            <tr align="center">
                <th align="center">ID</th>
                <th align="center">Nome</th>
                <th align="center">Link Execução</th>
                <th align="center">Data de Início</th>
                <th align="center">Tempo de Execução</th>
            </tr>
            {linhas_jobs_rodando}
        </table>
        """

        linhas_jobs_rodando = ""
        for job in jobs_rodando:
            linhas_jobs_rodando += f"""
            <tr align="center">
                <td align="center">{job['ID']}</td>
                <td align="center">{job['NAME']}</td>
                <td align="center"><a href="{job['PERMLINK']}">Execução</a></td>
                <td align="center">{job['DATA']}</td>
                <td align="center">{job['TIME']} m</td>
            </tr>
            """

                # Montagem final do corpo do e-mail em HTML
        corpo_email_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Relatório Diário - Jobs Rundeck</title>
        </head>
        <body>
            <img src="https://tech.oyster.com/public/images/rundeck-logo.png" alt="Rundeck" height="50">
            <h1>Relatório Diário - Jobs do Rundeck</h1>
            <!-- Inserção das tabelas HTML geradas anteriormente -->
            {tabela_jobs_com_erros.format(linhas_jobs_com_erros=linhas_jobs_com_erros)}
            {tabela_jobs_rodando.format(linhas_jobs_rodando=linhas_jobs_rodando)}
        </body>
        </html>
        """

        # Converte o corpo do e-mail para o formato MIMEText (HTML)
        mensagem.attach(MIMEText(corpo_email_html, 'html'))

        # Conexão com o servidor SMTP do Outlook
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Habilita a criptografia TLS
            # Faz o login na conta do Outlook
            server.login(remetente_email, remetente_senha)

            # Envio do e-mail
            server.sendmail(remetente_email, destinatario_email, mensagem.as_string())

            print('E-mail enviado com sucesso!')
        except Exception as e:
            print(f'Erro ao enviar e-mail: {e}')
        finally:
            server.quit()

# Certifique-se de que as configurações de e-mail e as informações do Rundeck sejam configuradas corretamente
# Antes de executar o script.
