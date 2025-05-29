from simulacao import Simulacao

# Script principal para rodar as simulações.
def main():
    sim = Simulacao(mapa_dimensao=4)
    todos_resultados = []

    # Cenário 1: Mapa Limpo
    print("\n##### Cenário: Mapa SEM Obstáculos, SEM Tráfego #####")
    todos_resultados.append(sim.executar_simulacao('a_star', tipo_cenario='sem_obstaculos', cenario_trafego=False, heuristica_a_star='manhattan'))
    todos_resultados.append(sim.executar_simulacao('a_star', tipo_cenario='sem_obstaculos', cenario_trafego=False, heuristica_a_star='euclidiana'))
    todos_resultados.append(sim.executar_simulacao('bfs', tipo_cenario='sem_obstaculos', cenario_trafego=False))

    # Cenário 2: Obstáculo Padrão, Sem Tráfego
    print("\n##### Cenário: Mapa PADRÃO (com 1 obstáculo fixo), SEM Tráfego #####")
    todos_resultados.append(sim.executar_simulacao('a_star', tipo_cenario='padrao', cenario_trafego=False, heuristica_a_star='manhattan'))
    todos_resultados.append(sim.executar_simulacao('a_star', tipo_cenario='padrao', cenario_trafego=False, heuristica_a_star='euclidiana'))
    todos_resultados.append(sim.executar_simulacao('bfs', tipo_cenario='padrao', cenario_trafego=False))

    # Cenário 3: Obstáculo Padrão, Com Tráfego
    print("\n##### Cenário: Mapa PADRÃO (com 1 obstáculo fixo), COM Tráfego #####")
    todos_resultados.append(sim.executar_simulacao('a_star', tipo_cenario='padrao', cenario_trafego=True, heuristica_a_star='manhattan'))
    todos_resultados.append(sim.executar_simulacao('a_star', tipo_cenario='padrao', cenario_trafego=True, heuristica_a_star='euclidiana'))
    todos_resultados.append(sim.executar_simulacao('bfs', tipo_cenario='padrao', cenario_trafego=True))

    # Cenário 4: Obstáculos Aleatórios, Sem Tráfego
    print("\n##### Cenário: Mapa com OBSTÁCULOS ALEATÓRIOS (5), SEM Tráfego #####")
    todos_resultados.append(sim.executar_simulacao('a_star', tipo_cenario='obstaculos_aleatorios', cenario_trafego=False, heuristica_a_star='manhattan'))
    todos_resultados.append(sim.executar_simulacao('a_star', tipo_cenario='obstaculos_aleatorios', cenario_trafego=False, heuristica_a_star='euclidiana'))
    todos_resultados.append(sim.executar_simulacao('a_star', tipo_cenario='obstaculos_aleatorios', cenario_trafego=False, heuristica_a_star='obstaculos'))
    todos_resultados.append(sim.executar_simulacao('bfs', tipo_cenario='obstaculos_aleatorios', cenario_trafego=False))

    # Cenário 5: Obstáculos Aleatórios, Com Tráfego
    print("\n##### Cenário: Mapa com OBSTÁCULOS ALEATÓRIOS (5), COM Tráfego #####")
    todos_resultados.append(sim.executar_simulacao('a_star', tipo_cenario='obstaculos_aleatorios', cenario_trafego=True, heuristica_a_star='manhattan'))
    todos_resultados.append(sim.executar_simulacao('a_star', tipo_cenario='obstaculos_aleatorios', cenario_trafego=True, heuristica_a_star='euclidiana'))
    todos_resultados.append(sim.executar_simulacao('a_star', tipo_cenario='obstaculos_aleatorios', cenario_trafego=True, heuristica_a_star='obstaculos'))
    todos_resultados.append(sim.executar_simulacao('bfs', tipo_cenario='obstaculos_aleatorios', cenario_trafego=True))

    # Imprime a tabela de resumo dos resultados.
    print("\n\n--- Resumo de Todos os Resultados ---")
    print("{:<12} | {:<10} | {:<8} | {:<10} | {:<6} | {:<10} | {:<8} | {:<6}".format(
        "Algoritmo", "Heurística", "Cenário", "Tráfego?", "Caminho?", "Passos", "Nós Exp.", "Tempo (s)"
    ))
    print("-" * 90)
    for res in todos_resultados:
        print("{:<12} | {:<10} | {:<8} | {:<10} | {:<6} | {:<10} | {:<8} | {:<.6f}".format(
            res['algoritmo'],
            res['heuristica'],
            res['cenario_mapa'].replace('_', ' '),
            'Sim' if res['cenario_trafego'] else 'Não',
            'Sim' if res['caminho_encontrado'] else 'Não',
            res['passos_totais'],
            res['nos_expandidos'],
            res['tempo_execucao']
        ))

if __name__ == "__main__":
    main()