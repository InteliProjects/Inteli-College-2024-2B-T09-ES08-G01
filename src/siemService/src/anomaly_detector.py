# src/anomaly_detector.py
import time
from collections import defaultdict, deque
import math
from math import radians
from . import alert_service
from . import config
import numpy as np


AlertService = alert_service.AlertService
conf = config.Config()
alert_service = AlertService()

class AnomalyDetector:
    def __init__(self):
        self.tentativas_acesso = defaultdict(list)
        self.requisicoes = defaultdict(deque)
        self.latencias = defaultdict(list)
        self.deadlocks_timeouts = defaultdict(int)
        self.padroes_uso = defaultdict(list)
        self.geolocalizacoes_historicas = defaultdict(set)

    def _atualizar_tentativas_acesso(self, usuario: str):
        #Atualiza as tentativas de acesso recentes para o usuário
        agora = time.time()
        self.tentativas_acesso[usuario].append(agora)
        self.tentativas_acesso[usuario] = [
            t for t in self.tentativas_acesso[usuario] if agora - t <= conf.PERIODO_ANALISE
        ]

    def _verificar_tentativas_acesso(self, usuario: str) -> bool:
        #Verifica se o limite de tentativas foi ultrapassado
        if len(self.tentativas_acesso[usuario]) > conf.LIMITE_TENTATIVAS:
            alert_service.enviar_alerta(usuario, "Tentativas de acesso excedidas")
            return True
        return False

    def _atualizar_taxa_requisicoes(self, usuario: str):
        #Atualiza o histórico de timestamps de requisições do usuário
        agora = time.time()
        self.requisicoes[usuario].append(agora)
        while self.requisicoes[usuario] and agora - self.requisicoes[usuario][0] > 1:
            self.requisicoes[usuario].popleft()

    def _verificar_taxa_requisicoes(self, usuario: str) -> bool:
        #Verifica se a taxa de requisições excedeu o limite
        if len(self.requisicoes[usuario]) > conf.TAXA_REQUISICOES_LIMITE:
            alert_service.enviar_alerta(usuario, "Taxa de requisições muito alta")
            return True
        return False

    def _verificar_latencia(self, usuario: str, latencia: float) -> bool:
        #Verifica se a latência excede o limite permitido
        if latencia > conf.LATENCIA_LIMITE:
            alert_service.enviar_alerta(usuario, f"Latência alta detectada: {latencia:.2f}s")
            return True
        return False

    def _verificar_timeout(self, usuario: str, timeout: bool) -> bool:
        #Verifica ocorrências de timeouts ou deadlocks
        if timeout:
            self.deadlocks_timeouts[usuario] += 1
            if self.deadlocks_timeouts[usuario] > conf.TIMEOUT_LIMITE:
                alert_service.enviar_alerta(usuario, "Deadlock ou timeout detectado")
                return True
        return False

    def _verificar_comportamento_previsivel(self, usuario: str, evento: str) -> bool:
        #Detecta quando um usuário deixa de ter um comportamento repetitivo (pouco desvio) e começa a ter um comportamento imprevisível (alto desvio).
        
        # Adiciona o evento à lista de eventos do usuário
        self.padroes_uso[usuario].append(evento)

        # Define o número mínimo de eventos para começar a análise
        PADRAO_PREVISOES = 5
        
        # Se o número de eventos do usuário for maior ou igual ao número de previsões
        if len(self.padroes_uso[usuario]) >= PADRAO_PREVISOES:
            eventos_recentes = self.padroes_uso[usuario][-PADRAO_PREVISOES:]  # Pega os últimos PADRAO_PREVISOES eventos
            
            # Verifica se todos os eventos recentes são iguais 
            if len(set(eventos_recentes)) == 1:  # Mesmo evento repetido
                alert_service.enviar_alerta(usuario, "Comportamento previsível anômalo")
                return True  # Comportamento previsível detectado

            # Converte os eventos para valores numéricos para calcular o desvio padrão
            eventos_numericos = [hash(evento) % 100 for evento in eventos_recentes]  # Transforma os eventos em números
            desvio_padrao = np.std(eventos_numericos)  # Calcula o desvio padrão dos eventos recentes

            # Se o desvio padrão for alto, o comportamento é considerado imprevisível
            if desvio_padrao > 20:  
                alert_service.enviar_alerta(usuario, "Comportamento imprevisível detectado!")
                return True  # Comportamento imprevisível detectado
        
        # Caso não tenha sido detectado comportamento previsível ou imprevisível
        return False
    
    def _calcular_distancia(self, lat1, lon1, lat2, lon2) -> float:
        #Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine.
    
        R = 6371  # Raio da Terra em km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(radians(lat1)) * math.cos(radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distancia = R * c
        return distancia

    def _validar_geolocalizacao(self, usuario: str, localizacao_atual: tuple, localizacoes_validas: list) -> bool:
        latitude_atual, longitude_atual = localizacao_atual

        # Inicializa o histórico de localizações do usuário se não existir
        if usuario not in self.geolocalizacoes_historicas:
            self.geolocalizacoes_historicas[usuario] = set()

        # Verifica se a localização atual já foi registrada no histórico
        if localizacao_atual in self.geolocalizacoes_historicas[usuario]:
            return False  # Se já estiver registrada, não é uma anomalia

        # Verifica se a localização atual é próxima a qualquer localização confiável do histórico
        locais_confiaveis = self.geolocalizacoes_historicas[usuario]
        for lat_conf, lon_conf in locais_confiaveis:
            if self._calcular_distancia(latitude_atual, longitude_atual, lat_conf, lon_conf) <= conf.DISTANCIA_LIMITE:
                return False
        
        # Verifica se a localização atual está dentro de algum local válido
        for lat_valida, lon_valida in localizacoes_validas:
            if self._calcular_distancia(latitude_atual, longitude_atual, lat_valida, lon_valida) <= conf.DISTANCIA_LIMITE:
                self.geolocalizacoes_historicas[usuario].add(localizacao_atual)  # Adiciona a nova localização ao histórico
                return False

        # Se não for uma localização confiável nem válida, é uma anomalia
        self.geolocalizacoes_historicas[usuario].add(localizacao_atual)  # Adiciona a nova localização ao histórico
        alert_service.enviar_alerta(
            usuario,
            f"Geolocalização suspeita detectada: {localizacao_atual}. Locais confiáveis: {locais_confiaveis}"
        )
        return True

    def detectar_anomalias(
        self, usuario: str, latencia: float = None, timeout: bool = False, evento: str = None, localizacao_atual: tuple = None,
    ) -> bool:
        #Detecta anomalias de diversas categorias e aciona alertas

        self._atualizar_tentativas_acesso(usuario)
        if self._verificar_tentativas_acesso(usuario):
            return True

        self._atualizar_taxa_requisicoes(usuario)
        if self._verificar_taxa_requisicoes(usuario):
            return True

        if latencia is not None and self._verificar_latencia(usuario, latencia):
            return True

        if timeout and self._verificar_timeout(usuario, timeout):
            return True

        if evento is not None and self._verificar_comportamento_previsivel(usuario, evento):
            return True
        
        if localizacao_atual is not None and self._validar_geolocalizacao(usuario, localizacao_atual):
            return True

        return False
