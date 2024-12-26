from src.geolocalizador import Geolocalizador

def test_obter_coordenadas(caplog):
    geolocalizador = Geolocalizador()

    caplog.set_level("INFO")

    localizacao = geolocalizador.obter_coordenadas("São Paulo")
    assert localizacao == (-23.5505, -46.6333)
    print(f"[TESTE] Geolocalização válida detectada: {localizacao}")

    localizacao_invalida = geolocalizador.obter_coordenadas("Cidade Inexistente")
    assert localizacao_invalida is None
    print("[TESTE] Cidade inválida não encontrada corretamente")
