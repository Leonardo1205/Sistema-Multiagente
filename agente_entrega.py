import heapq 
import math

class AgenteEntrega:
    def __init__(self, mapa_dimensao):
        self.mapa_dimensao = mapa_dimensao

    def _is_valid(self, r, c, mapa_base):
        """Verifica se (r,c) é uma posição válida no mapa (dentro dos limites e não obstáculo)."""
        return 0 <= r < self.mapa_dimensao and 0 <= c < self.mapa_dimensao and mapa_base[r][c] != 1

    def _get_neighbors(self, r, c, mapa_base):
        """Retorna vizinhos válidos (cima, baixo, esquerda, direita)."""
        neighbors = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Movimentos cardinais
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if self._is_valid(nr, nc, mapa_base):
                neighbors.append((nr, nc))
        return neighbors

    def _heuristica_manhattan(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def _heuristica_euclidiana(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def _heuristica_obstaculos(self, p1, p2, mapa_base):
        """Heurística experimental: conta obstáculos num retângulo entre p1 e p2. Pode não ser admissível."""
        count = 0
        min_r, max_r = min(p1[0], p2[0]), max(p1[0], p2[0])
        min_c, max_c = min(p1[1], p2[1]), max(p1[1], p2[1])
        for r_idx in range(min_r, max_r + 1):
            for c_idx in range(min_c, max_c + 1):
                if mapa_base[r_idx][c_idx] == 1:
                    count += 1
        return count * 2 # Peso arbitrário

    def _reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current) 
        return path[::-1] 

    def buscar_caminho_a_star(self, inicio, destino, mapa_base, alertas_transito, heuristica_func):
        import time
        start_time = time.time()

        # open_set é uma fila de prioridade (min-heap) para os nós a serem visitados.
        open_set = [] 
        came_from = {} 
        
        g_score = { (r,c): float('inf') for r in range(self.mapa_dimensao) for c in range(self.mapa_dimensao) }
        g_score[inicio] = 0

        f_score = { (r,c): float('inf') for r in range(self.mapa_dimensao) for c in range(self.mapa_dimensao) }
        f_score[inicio] = g_score[inicio] + (self._heuristica_obstaculos(inicio, destino, mapa_base) 
                                            if heuristica_func.__name__ == "_heuristica_obstaculos" 
                                            else heuristica_func(inicio, destino))
        
        heapq.heappush(open_set, (f_score[inicio], g_score[inicio], inicio))
        nos_expandidos = 0

        while open_set:
            current_f, current_g_in_heap, current_node = heapq.heappop(open_set)
            
            if current_f > f_score[current_node]: # Otimização: já achamos caminho melhor
                continue
            nos_expandidos += 1

            if current_node == destino:
                path = self._reconstruct_path(came_from, current_node)
                return path, len(path) - 1, nos_expandidos, (time.time() - start_time)

            for neighbor in self._get_neighbors(current_node[0], current_node[1], mapa_base):
                # Custo base do movimento + custo de tráfego (se houver).
                tentative_g_score = g_score[current_node] + 1 + alertas_transito.get(neighbor, 0)

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + (self._heuristica_obstaculos(neighbor, destino, mapa_base)
                                                            if heuristica_func.__name__ == "_heuristica_obstaculos"
                                                            else heuristica_func(neighbor, destino))
                    heapq.heappush(open_set, (f_score[neighbor], g_score[neighbor], neighbor))
        
        return None, 0, nos_expandidos, (time.time() - start_time)

    def buscar_caminho_bfs(self, inicio, destino, mapa_base, alertas_transito):
        import time
        from collections import deque
        start_time = time.time()

        queue = deque([inicio])
        visited = {inicio}
        came_from = {}
        nos_expandidos = 0

        while queue:
            current_node = queue.popleft()
            nos_expandidos += 1

            if current_node == destino:
                path = self._reconstruct_path(came_from, current_node)
                # BFS acha o caminho mais curto em passos, ignora custos de trânsito na escolha.
                return path, len(path) - 1, nos_expandidos, (time.time() - start_time)

            for neighbor in self._get_neighbors(current_node[0], current_node[1], mapa_base):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current_node
                    queue.append(neighbor)
        
        return None, 0, nos_expandidos, (time.time() - start_time)