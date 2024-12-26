from src.auditor import Auditor

def test_auditar_acesso(mocker, caplog):
    caplog.set_level("INFO")
    mock_logger = mocker.patch("src.auditor.using_logger")

    auditor = Auditor()
    mock_logger.registrar_acesso = mocker.Mock()

    usuario = "usuario1"
    acao = "login"
    documento = "documento_sensivel"
    ip_origem = "192.168.0.1"

    auditor.auditar_acesso(usuario, documento, acao, ip_origem)
    print(f"[TESTE] Auditoria de acesso concluída: Usuário: {usuario}, Documento: {documento}, Ação: {acao}, IP: {ip_origem}")

    mock_logger.registrar_acesso.assert_called_once_with(usuario, acao, documento, ip_origem)
