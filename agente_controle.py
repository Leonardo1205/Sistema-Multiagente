import random

class AgenteControle:
    def __init__(self, mapa_dimensao=4):
        self.mapa_dimensao = mapa_dimensao
        self.mapa_base = self._criar_mapa_padrao() 
        self.alertas_transito = {} 

    def _criar_mapa_padrao(self):
        """Mapa 4x4 com um obstáculo fixo em (1,1)."""
        return [
            [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]
        ]

    def gerar_mapa_cenario(self, tipo_cenario="padrao", num_obstaculos=0):
        """ Configura o mapa_base para diferentes cenários. """
        if tipo_cenario == "sem_obstaculos":
            self.mapa_base = [[0 for _ in range(self.mapa_dimensao)] for _ in range(self.mapa_dimensao)]
        elif tipo_cenario == "obstaculos_aleatorios":
            self.mapa_base = [[0 for _ in range(self.mapa_dimensao)] for _ in range(self.mapa_dimensao)]
            # Evita ter mais obstáculos que células (menos 2, pra início/fim).
            max_obs = self.mapa_dimensao * self.mapa_dimensao - 2
            num_obstaculos = min(num_obstaculos, max_obs if max_obs > 0 else 0)
            
            celulas_disponiveis = [(r, c) for r in range(self.mapa_dimensao) for c in range(self.mapa_dimensao)]
            if num_obstaculos > 0 and len(celulas_disponiveis) >= num_obstaculos:
                obstaculos_pos = random.sample(celulas_disponiveis, num_obstaculos)
                for r_obs, c_obs in obstaculos_pos:
                    self.mapa_base[r_obs][c_obs] = 1 
        else: 
            self.mapa_base = self._criar_mapa_padrao()
        return self.mapa_base


    def gerar_alertas_transito(self, mapa_atual):
        """ Gera 1 ou 2 alertas de tráfego em células válidas (não obstáculos). """
        self.alertas_transito = {} 
        num_celulas_transito = random.randint(1, 2)
        
        celulas_validas = [(r, c) for r in range(self.mapa_dimensao) for c in range(self.mapa_dimensao) if mapa_atual[r][c] != 1]

        num_celulas_transito = min(num_celulas_transito, len(celulas_validas))

        if num_celulas_transito > 0:
            celulas_com_transito = random.sample(celulas_validas, num_celulas_transito)
            for x, y in celulas_com_transito:
                self.alertas_transito[(x, y)] = 5 # Custo de tráfego
        return self.alertas_transito

    def get_mapa_atual_estado(self):
        """ Retorna uma cópia do mapa base. """
        return [row[:] for row in self.mapa_base] 

    def print_mapa(self, agente_pos, destino_pos, caminho=None, mapa_display_base=None):
        """ Imprime o mapa no console com agente, destino, obstáculos, tráfego e caminho. """
        mapa_display = [row[:] for row in (mapa_display_base if mapa_display_base else self.mapa_base)]

        # A ordem de "pintura" é importante para a sobreposição correta dos símbolos.
        for (x, y), _ in self.alertas_transito.items():
            if mapa_display[x][y] == 0: mapa_display[x][y] = 'T' 

        if caminho:
            for x, y in caminho:
                if (x,y) != agente_pos and (x,y) != destino_pos and mapa_display[x][y] == 0:
                    mapa_display[x][y] = '*' 

        # Marcar destino e agente por último para garantir que apareçam.
        if str(mapa_display[destino_pos[0]][destino_pos[1]]) == 'T': mapa_display[destino_pos[0]][destino_pos[1]] = 'DT'
        elif mapa_display[destino_pos[0]][destino_pos[1]] == 1: mapa_display[destino_pos[0]][destino_pos[1]] = 'DO'
        else: mapa_display[destino_pos[0]][destino_pos[1]] = 'D' 

        if str(mapa_display[agente_pos[0]][agente_pos[1]]) == 'T': mapa_display[agente_pos[0]][agente_pos[1]] = 'AT'
        elif mapa_display[agente_pos[0]][agente_pos[1]] == 1: mapa_display[agente_pos[0]][agente_pos[1]] = 'AO'
        elif (agente_pos[0], agente_pos[1]) != (destino_pos[0], destino_pos[1]): 
            mapa_display[agente_pos[0]][agente_pos[1]] = 'A'

        print("\n--- Mapa Atual ---")
        for r_val in mapa_display:
            row_str = [str(cell) if cell not in [0,1] else ('.' if cell == 0 else '#') for cell in r_val]
            print(" ".join(row_str))
        print("------------------")