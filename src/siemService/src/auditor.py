# src/auditor.py
from . import logger
from . import anomaly_detector

AnomalyDetector = anomaly_detector.AnomalyDetector
using_logger = logger.LoggerService()

class Auditor:
    def __init__(self):
        self.using_logger = logger.LoggerService()
        self.anomaly_detector = AnomalyDetector()

    def _validar_parametros(self, usuario, acao, documento, ip_origem):
        #Valida os parâmetros fornecidos para auditoria
        if not isinstance(usuario, str) or not usuario.strip():
            raise ValueError("Usuário inválido: deve conter um nome de usuário.")
        if not isinstance(acao, str) or not acao.strip():
            raise ValueError("Ação inválida: deve conter uma ação específica.")
        if not isinstance(documento, str) or not documento.strip():
            raise ValueError("Documento inválido: deve conter o nome do documento.")
        if not isinstance(ip_origem, str) or not ip_origem.strip():
            raise ValueError("IP de origem inválido: deve ser um endereço IP válido.")

    def _registrar_log(self, usuario, mensagem, nivel="INFO"):
        #Registra logs estruturados para auditoria
        log_format = f"[AUDITOR] | USUÁRIO: {usuario} | MENSAGEM: {mensagem}"
        if nivel == "INFO":
            print(log_format)  
        elif nivel == "WARNING":
            print(f"⚠️ {log_format}")  
        elif nivel == "ERROR":
            print(f"❌ {log_format}")  

    def auditar_acesso(self, usuario, documento, acao, ip_origem):
        #Registra o acesso a um recurso e verifica atividades anômalas

        try:
            self._validar_parametros(usuario, acao, documento, ip_origem)
            using_logger.registrar_acesso(usuario, acao, documento, ip_origem)
            self._registrar_log(usuario, f"Acesso registrado para ação '{acao}' no documento '{documento}', com origem em '{ip_origem}'.")

            # Verifica por anomalias no comportamento do usuário
            if self.anomaly_detector.detectar_anomalias(usuario, evento=acao):
                self._registrar_log(
                    usuario, 
                    "Atividade anômala detectada durante o acesso.", 
                    nivel="WARNING"
                )
            else:
                self._registrar_log(usuario, "Acesso concluído sem irregularidades.")
        except Exception as e:
            self._registrar_log(usuario, f"Erro ao auditar acesso: {str(e)}", nivel="ERROR")
            raise

