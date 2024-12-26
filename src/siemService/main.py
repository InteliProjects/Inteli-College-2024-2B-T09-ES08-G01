# main.py
import sys
import os
import time
from src.logger import LoggerService
from src.geolocalizador import Geolocalizador
from src.alert_service import AlertService
from src.anomaly_detector import AnomalyDetector
from src.auditor import Auditor
from src.config import Config
from src.data import usuarios, acoes, documentos, localizacoes

# Adicionando o diretório src ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'siemService', 'src')))

# Configuração do sistema
conf = Config()
logger_service = LoggerService()
geolocalizador = Geolocalizador()
alert_service = AlertService(sender=conf.EMAIL_SENDER, recipient=conf.EMAIL_RECIPIENT)
anomaly_detector = AnomalyDetector()
auditor = Auditor()

def main():
    # Simula acessos e verifica anomalias
    for usuario in usuarios:
        for acao, documento in zip(acoes, documentos):
            # Registrar o acesso
            logger_service.registrar_acesso(usuario="user123", documento="doc456", acao="acesso")

            # Obter a localização fictícia atual do usuário
            cidades = localizacoes.get(usuario, [])
            if cidades:
                for cidade in cidades:
                    coordenadas = geolocalizador.obter_coordenadas(cidade)
                    if coordenadas:
                        latitude_atual, longitude_atual = coordenadas

                        # Validar se a localização atual do usuário está entre as localizações possíveis
                        if anomaly_detector._validar_geolocalizacao(usuario, localizacao_atual=(latitude_atual, longitude_atual)):
                            logger_service.registrar_acesso(usuario, documento, acao="acesso", ip_origem="desconhecido")
                            print(f"Acesso do usuário {usuario} à ação {acao} do documento {documento} registrado com sucesso. Localização: {cidade} (Lat: {latitude_atual}, Lon: {longitude_atual})")
                        else:
                            logger_service.registrar_acesso(usuario, documento, acao="erro", ip_origem="desconhecido")
                            print(f"Anomalia detectada para o usuário {usuario} na ação {acao} do documento {documento}. Localização: {cidade} (Lat: {latitude_atual}, Lon: {longitude_atual})")

            # Simular algum evento, como latência ou timeout
            if acao == "download":
                latencia = 2.5
                timeout = True
                anomaly_detector.detectar_anomalias(usuario, latencia=latencia, timeout=timeout)

            # Simular comportamento previsível (para acionar alertas)
            evento = "download"
            anomaly_detector.detectar_anomalias(usuario, evento=evento)

            # Simula o tempo de espera entre as ações
            time.sleep(1)

    # Teste de auditoria - Acesso e alerta de atividade anômala
    for usuario in usuarios:
        acao = "login"
        documento = "documento1"
        auditor.auditar_acesso(usuario, acao, documento)

    # Enviar um alerta de exemplo
    alert_service.enviar_alerta("usuario1", "Alerta de exemplo")

    logger_service.registrar_acesso("usuario1", "documento_exemplo", acao="informacao", ip_origem="desconhecido")
    print("Execução completa.")

if __name__ == "__main__":
    main()
