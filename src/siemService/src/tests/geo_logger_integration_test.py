from .. import logger
from .. import geolocalizador

LoggerService = logger.LoggerService
Geolocalizador = geolocalizador.Geolocalizador

def test_geolocalizacao_e_registro(mocker, caplog):
    caplog.set_level("INFO")

    # Mockando dependências externas
    mock_geolocalizador = mocker.patch.object(Geolocalizador, "obter_localizacao")
    mock_geolocalizador.return_value = {"city": "São Paulo", "latitude": -23.5505, "longitude": -46.6333}
    
    mock_logger = mocker.patch.object(LoggerService, "registrar_acesso")

    # Configurando serviços
    logger_service = LoggerService()
    geolocalizador = Geolocalizador()

    # Dados simulados
    usuario = "usuario3"
    documento = "doc456"
    acao = "editar"
    ip_origem = "192.168.1.1"

    # Fluxo
    localizacao = geolocalizador.obter_localizacao(ip_origem)
    print(f"[TESTE] Localização obtida para o IP '{ip_origem}': {localizacao}")
    logger_service.registrar_acesso(usuario, documento, acao, ip_origem)
    print(f"[TESTE] Acesso registrado para {usuario}: Documento: {documento}, Ação: {acao}, IP: {ip_origem}")

    # Verificações
    mock_geolocalizador.assert_called_once_with(ip_origem)
    mock_logger.assert_called_once_with(usuario, documento, acao, ip_origem)
