from src.alert_service import AlertService
from src.anomaly_detector import AnomalyDetector

def test_fluxo_envio_alerta_anomalia(mocker, caplog):
    caplog.set_level("INFO")

    # Mockando dependências externas
    mock_alert_service = mocker.patch.object(AlertService, "enviar_alerta")
    mock_anomaly_detector = mocker.patch.object(AnomalyDetector, "_validar_geolocalizacao")
    mock_anomaly_detector.return_value = False

    alert_service = AlertService(sender="sender@test.com", recipient="recipient@test.com")
    anomaly_detector = AnomalyDetector()

    usuario = "usuario2"
    acao = "download"
    documento = "doc789"
    localizacao_atual = (51.5074, -0.1278)  # Londres

    if not anomaly_detector._validar_geolocalizacao(usuario, localizacao_atual, []):
        alert_service.enviar_alerta(usuario, f"Anomalia detectada na ação {acao} do documento {documento}")
        print(f"[TESTE] Alerta gerado para anomalia na geolocalização de {usuario}: Documento: {documento}, Ação: {acao}, Localização: {localizacao_atual}")

    mock_anomaly_detector.assert_called_once_with(usuario, localizacao_atual, [])
    mock_alert_service.assert_called_once_with(usuario, "Anomalia detectada na ação download do documento doc789")
