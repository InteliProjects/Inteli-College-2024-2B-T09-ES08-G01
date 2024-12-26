import pytest
from src.anomaly_detector import AnomalyDetector

@pytest.fixture
def detector():
    # Criação de uma instância do detector e definição do estado inicial
    detector = AnomalyDetector()
    detector.geolocalizacoes_historicas = {}
    return detector

def test_validar_geolocalizacao_valida(detector, caplog):
    caplog.set_level("INFO")
    usuario = 'usuario1'
    localizacao_atual = (40.7128, -74.0060)  # Nova York
    localizacoes_validas = [(40.7128, -74.0060), (34.0522, -118.2437)]  # Locais válidos

    resultado = detector._validar_geolocalizacao(usuario, localizacao_atual, localizacoes_validas)
    print(f"[TESTE] Geolocalização válida para {usuario}: {localizacao_atual}")
    assert not resultado

def test_validar_geolocalizacao_suspeita(detector):
    # Testando geolocalização suspeita
    usuario = 'usuario1'
    localizacao_atual = (37.7749, -122.4194)  # São Francisco (não válida)
    localizacoes_validas = [(40.7128, -74.0060), (34.0522, -118.2437)]  # Locais válidos

    # Chamando o método para validar a geolocalização
    resultado = detector._validar_geolocalizacao(usuario, localizacao_atual, localizacoes_validas)

    # Verificando se a localização foi marcada como suspeita
    assert resultado  # Deve ser uma anomalia (True)

def test_validar_geolocalizacao_com_historico_confiavel(detector):
    # Testando uma geolocalização já no histórico confiável
    usuario = 'usuario1'
    localizacao_atual = (40.7128, -74.0060)  # Nova York (válida)
    localizacoes_validas = [(40.7128, -74.0060), (34.0522, -118.2437)]  # Locais válidos

    # Adicionando uma geolocalização confiável no histórico
    detector.geolocalizacoes_historicas[usuario] = {(40.7128, -74.0060)}

    # Chamando o método para validar a geolocalização
    resultado = detector._validar_geolocalizacao(usuario, localizacao_atual, localizacoes_validas)

    # Verificando se a geolocalização confiável foi reconhecida como válida
    assert not resultado  # Não deve ser uma anomalia (False)

