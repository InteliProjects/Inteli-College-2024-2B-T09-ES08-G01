from src.logger import LoggerService

def test_registrar_acesso(mocker):
    mock_logging = mocker.patch("src.logger.logging.info")
    logger_service = LoggerService()

    logger_service.registrar_acesso(
        usuario="usuario1",
        documento="documento1",
        acao="acesso",
        ip_origem="127.0.0.1"
    )

    mock_logging.assert_called_once_with({
        "tipo": "ACESSO",
        "timestamp": mocker.ANY,
        "usuario": "usuario1",
        "documento": "documento1",
        "ip_origem": "127.0.0.1"
    })
