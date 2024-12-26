class Geolocalizador:
    def __init__(self):
        # Dados mockados das cidades com suas respectivas coordenadas (latitude, longitude)
        self.localizacoes = {
            "são paulo": (-23.5505, -46.6333),
            "rio de janeiro": (-22.9068, -43.1729),
            "belo horizonte": (-19.9191, -43.9386),
            "salvador": (-12.9714, -38.5014),
            "fortaleza": (-3.7172, -38.5437),
            "curitiba": (-25.4296, -49.2711),
            "porto alegre": (-30.0346, -51.2177),
            "florianópolis": (-27.5954, -48.5480)
        }

    def obter_localizacao(self, cidade):
        # Retorna as coordenadas associadas à cidade
        return self.obter_coordenadas(cidade)

    def obter_coordenadas(self, cidade):
        cidade = cidade.strip().lower()  # Limpa espaços e converte para minúsculas
        if cidade in self.localizacoes:
            return self.localizacoes[cidade]
        else:
            print(f"Cidade '{cidade}' não encontrada.")
            return None
