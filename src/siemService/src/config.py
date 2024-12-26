import os
from dotenv import load_dotenv

#Carregar as variáveis do ambiente arquiv.env
load_dotenv()

class ConfigError(Exception):
    #Exceções personalizadas para erros de configuração
    def __init__(self, mensagem, tipo_erro="GENÉRICO"):
        super().__init__(mensagem)
        self.tipo_erro = tipo_erro

    def __str__(self):
        return f"[Erro de Configuração - {self.tipo_erro}] {self.args[0]}"

class Config:
    # Diretório de logs
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    LIMITE_TENTATIVAS = int(os.getenv("LIMITE_TENTATIVAS", 5))
    PERIODO_ANALISE = int(os.getenv("PERIODO_ANALISE", 60))  # em segundos

    # Configurações de e-mail
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

    #Parâmetros de taxas
    TAXA_REQUISICOES_LIMITE = int(os.getenv("TAXA_REQUISICOES_LIMITE", 3))
    LATENCIA_LIMITE = int(os.getenv("LATENCIA_LIMITE", 500))
    TIMEOUT_LIMITE = int(os.getenv("TIMEOUT_LIMITE", 10))
    PADRAO_PREVISOES = int(os.getenv("PADRAO_PREVISOES", 5))
    DISTANCIA_LIMITE = int(os.getenv("DISTANCIA_LIMITE", 10))

    @classmethod
    def configurar_diretorio_logs(cls):
        #Configura o diretório de logs, criando caso não exista
        if not os.path.exists(cls.LOG_DIR):
            try:
                os.makedirs(cls.LOG_DIR)
                print(f"Diretório de logs criado em: {cls.LOG_DIR}")
            except OSError as e:
                raise ConfigError(f"Erro ao criar diretório de logs: {e}",
                    tipo_erro="ERRO_DIRETÓRIO_LOG")

# Cria o diretório de logs no momento de importação
Config.configurar_diretorio_logs()