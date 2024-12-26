import logging
import os
import re
from colorama import Fore, Style
from pathlib import Path
from dotenv import load_dotenv
from . import config
from datetime import datetime

Config = config.Config

# Carrega as variáveis de ambiente do .env
load_dotenv()

class LoggerService:
    def __init__(self):
        self.configurar_logger()

    def configurar_logger(self):
        #Configura o logger com base nas variáveis de ambiente
        log_dir = Path(Config.LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)  

        # Parâmetros do logger, com valores padrão se as variáveis de ambiente não forem definidas
        log_filename = os.getenv("LOG_FILENAME", "access_log.log")
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()

        # Configuração básica do logger
        logging.basicConfig(
            filename=log_dir / log_filename,
            level=getattr(logging, log_level, logging.INFO),
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        logging.debug("Logger configurado com sucesso.")

    def validar_ip(self, ip: str) -> bool:
        ip_regex = r'^(\d{1,3}\.){3}\d{1,3}$'
        return re.match(ip_regex, ip) is not None

    def registrar_acesso(self, usuario: str, documento: str, acao: str = "acesso", ip_origem: str = "desconhecido"):
        #Registra um acesso no log

        if not usuario or not documento:
            mensagem_erro = "Campos obrigatórios ausentes. Forneça os seguintes dados: 'usuario' e 'documento'."
            logging.error(mensagem_erro)
            raise ValueError(mensagem_erro)

        if ip_origem != "desconhecido" and not self.validar_ip(ip_origem):
            logging.error("IP de origem inválido.")
            raise ValueError("O formato do IP de origem é inválido.")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "tipo": acao.upper(),
            "timestamp": timestamp,
            "usuario": usuario,
            "documento": documento,
            "ip_origem": ip_origem
        }

        try:
            logging.info(log_entry)

            log_formatado = (
                        f"[{log_entry['tipo']}] {log_entry['timestamp']} - "
                        f"Usuário: {log_entry['usuario']}, Documento: {log_entry['documento']}, "
                        f"IP de Origem: {log_entry['ip_origem']}"
                    )

            # Aplicar cores com base no tipo de ação
            if acao.lower() == "acesso":
                print(Fore.GREEN + f"Log de acesso registrado: {log_formatado}" + Style.RESET_ALL)
            elif acao.lower() == "erro":
                print(Fore.RED + f"Erro no acesso: {log_formatado}" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"Ação registrada: {log_formatado}" + Style.RESET_ALL)

        except Exception as e:
            logging.error(f"Falha ao registrar o log de acesso: {e}")
            raise


    def registrar_modificacao_documento(self, usuario: str, documento: str, descricao_modificacao: str, ip_origem: str = "desconhecido"):
        #Registra uma modificação de documento no log.

        if not usuario or not documento or not descricao_modificacao:
            logging.error("Tentativa de registro de modificação com informações incompletas.")
            raise ValueError("Os campos 'usuario', 'documento' e 'descricao_modificacao' são obrigatórios.")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = (
            f"[MODIFICAÇÃO] Timestamp: {timestamp}, Usuário: {usuario}, "
            f"Documento: {documento}, Descrição: {descricao_modificacao}, IP de Origem: {ip_origem}"
        )

        try:
            logging.info(log_entry)
            print(f"Log de modificação registrado: {log_entry}")
        except Exception as e:
            logging.error(f"Falha ao registrar o log de modificação: {e}")
            raise


