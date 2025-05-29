from agente_controle import AgenteControle
from agente_entrega import AgenteEntrega
import random

class Simulacao:
    def __init__(self, mapa_dimensao=4):
        self.agente_controle = AgenteControle(mapa_dimensao)
        self.agente_entrega = AgenteEntrega(mapa_dimensao)
        self.mapa_dimensao = mapa_dimensao
        
        # Mapeamento de string para função heurística, pra facilitar a chamada.
        self.heuristica_map = {
            'manhattan': self.agente_entrega._heuristica_manhattan,
            'euclidiana': self.agente_entrega._heuristica_euclidiana,
            'obstaculos': self.agente_entrega._heuristica_obstaculos 
        }

    def _gerar_posicao_aleatoria(self, mapa_base):
        """Gera uma posição aleatória que não seja um obstáculo."""
        tentativas = 0
        # Limite de tentativas para não travar se o mapa estiver muito cheio.
        max_tentativas = self.mapa_dimensao * self.mapa_dimensao * 2 
        while tentativas < max_tentativas:
            r = random.randint(0, self.mapa_dimensao - 1)
            c = random.randint(0, self.mapa_dimensao - 1)
            if mapa_base[r][c] != 1: # 1 é obstáculo
                return (r, c)
            tentativas += 1
        return None # Falhou em achar uma posição válida.


    def executar_simulacao(self, algoritmo_escolhido, tipo_cenario="padrao", cenario_trafego=False, heuristica_a_star='manhattan'):
        """ Orquestra uma única simulação de entrega. """
        print(f"\n--- Iniciando Simulação ---")
        print(f"Algoritmo: {algoritmo_escolhido.upper()}, Cenário: {tipo_cenario.replace('_', ' ').title()}, Tráfego: {'Sim' if cenario_trafego else 'Não'}")
        if algoritmo_escolhido == 'a_star':
            print(f"Heurística A*: {heuristica_a_star.title()}")

        num_obstaculos_aleatorios = 5 
        mapa_config = self.agente_controle.gerar_mapa_cenario(tipo_cenario, num_obstaculos_aleatorios)
        
        inicio = self._gerar_posicao_aleatoria(mapa_config)
        destino = self._gerar_posicao_aleatoria(mapa_config)
        
        # Se não conseguiu gerar posições válidas, retorna um resultado "falho".
        if inicio is None or destino is None:
            print("Não foi possível gerar início/destino válidos. Mapa muito congestionado.")
            return { "algoritmo": algoritmo_escolhido, "cenario_mapa": tipo_cenario, "cenario_trafego": cenario_trafego,
                     "caminho_encontrado": False, "passos_totais": 0, "nos_expandidos": 0, "tempo_execucao": 0.0,
                     "heuristica": heuristica_a_star if algoritmo_escolhido == 'a_star' else 'N/A' }

        while inicio == destino: # Garante que início e destino sejam diferentes.
            destino = self._gerar_posicao_aleatoria(mapa_config)
            if destino is None: 
                print("Não foi possível gerar um destino distinto. Mapa muito congestionado.")
                return { "algoritmo": algoritmo_escolhido, "cenario_mapa": tipo_cenario, "cenario_trafego": cenario_trafego,
                         "caminho_encontrado": False, "passos_totais": 0, "nos_expandidos": 0, "tempo_execucao": 0.0,
                         "heuristica": heuristica_a_star if algoritmo_escolhido == 'a_star' else 'N/A' }

        alertas_transito = self.agente_controle.gerar_alertas_transito(mapa_config) if cenario_trafego else {}

        print(f"Início: {inicio}, Destino: {destino}")
        self.agente_controle.print_mapa(inicio, destino, mapa_display_base=mapa_config)

        caminho, passos, nos_expandidos, tempo_execucao = None, 0, 0, 0.0

        if algoritmo_escolhido == 'a_star':
            heuristica_func = self.heuristica_map.get(heuristica_a_star)
            if heuristica_func is None: return None # Heurística inválida
            caminho, passos, nos_expandidos, tempo_execucao = \
                self.agente_entrega.buscar_caminho_a_star(inicio, destino, mapa_config, alertas_transito, heuristica_func)
        elif algoritmo_escolhido == 'bfs':
            caminho, passos, nos_expandidos, tempo_execucao = \
                self.agente_entrega.buscar_caminho_bfs(inicio, destino, mapa_config, alertas_transito)
        else:
            print("Algoritmo não reconhecido.")
            return None

        if caminho:
            print(f"Caminho: {caminho}, Passos: {passos}, Nós Exp.: {nos_expandidos}, Tempo: {tempo_execucao:.6f}s")
            self.agente_controle.print_mapa(inicio, destino, caminho, mapa_display_base=mapa_config)
        else:
            print(f"Nenhum caminho encontrado. Nós Exp.: {nos_expandidos}, Tempo: {tempo_execucao:.6f}s")
            self.agente_controle.print_mapa(inicio, destino, mapa_display_base=mapa_config)

        # Retorna um dicionário com os dados da simulação.
        return {
            "algoritmo": algoritmo_escolhido, "cenario_mapa": tipo_cenario, "cenario_trafego": cenario_trafego,
            "caminho_encontrado": bool(caminho), "passos_totais": passos, "nos_expandidos": nos_expandidos,
            "tempo_execucao": tempo_execucao, "heuristica": heuristica_a_star if algoritmo_escolhido == 'a_star' else 'N/A'
        }