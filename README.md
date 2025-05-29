# Otimizando Entregas Urbanas com IA 🚚💨

Este projeto simula um sistema multiagente para otimização de rotas de entrega em um ambiente urbano representado por um mapa 4x4. O objetivo é demonstrar como a Inteligência Artificial, através de algoritmos de busca e heurísticas, pode ser aplicada para encontrar caminhos eficientes em cenários com obstáculos e condições de tráfego variáveis.

Este trabalho foi desenvolvido na disciplina de Inteligência Artificial do curso de Engenharia de Software.

## ✨ Funcionalidades

* **Sistema Multiagente:**
    * `AgenteDeControle`: Responsável por gerar o mapa, posicionar obstáculos e criar alertas de tráfego.
    * `AgenteDeEntrega`: Encarregado de encontrar o melhor caminho do ponto de partida ao destino.
* **Ambiente Dinâmico:**
    * Mapa em grade 4x4.
    * Suporte a obstáculos fixos e aleatórios.
    * Geração de alertas de tráfego aleatórios que alteram o custo do percurso.
* **Algoritmos de Busca:**
    * **A\*** (A-Star): Algoritmo de busca heurística.
    * **BFS** (Busca em Largura): Algoritmo de busca não heurística para comparação.
* **Heurísticas para A\***:
    * Distância de Manhattan.
    * Distância Euclidiana.
    * Heurística customizada baseada na contagem de obstáculos próximos.
* **Simulação e Análise:**
    * Execução de múltiplos cenários para testar a robustez e eficiência dos algoritmos.
    * Coleta de métricas de desempenho: passos totais, nós expandidos e tempo de execução.
    * Visualização textual do mapa, incluindo a posição do agente, destino, obstáculos, tráfego e o caminho encontrado.

## 📂 Estrutura do Projeto

O projeto está organizado nos seguintes arquivos Python:

* `main.py`: Script principal para executar as simulações e exibir os resultados consolidados.
* `simulacao.py`: Contém a classe `Simulacao` que orquestra a interação entre os agentes, a configuração dos cenários e a execução das buscas.
* `agente_entrega.py`: Define a classe `AgenteEntrega`, implementando os algoritmos de busca A* e BFS, bem como as funções heurísticas.
* `agente_controle.py`: Define a classe `AgenteControle`, responsável pela geração do mapa, obstáculos e alertas de tráfego, além da visualização do mapa.

## 🛠️ Tecnologias Utilizadas

* Python 3.11.9
* Bibliotecas padrão do Python: `random`, `math`, `heapq`, `collections.deque`, `time`.

## 🚀 Como Executar

1.  **Pré-requisitos:**
    * Certifique-se de ter o Python instalado em seu sistema.

2.  **Rodando a Simulação:**
    Abra um terminal ou prompt de comando, navegue até o diretório raiz do projeto e execute o script `main.py`:
    ```bash
    python main.py
    ```

3.  **O que esperar:**
    * O script executará uma série de simulações para diferentes cenários, algoritmos e heurísticas.
    * Para cada simulação, o estado inicial do mapa, a posição do agente (A) e do destino (D), os obstáculos (#) e o tráfego (T) serão impressos.
    * Se um caminho for encontrado, ele será marcado com asteriscos (\*) no mapa.
    * Detalhes como o caminho encontrado, número de passos, nós expandidos e tempo de execução serão exibidos para cada simulação.
    * Ao final de todas as simulações, uma tabela de resumo consolidada será apresentada, comparando os resultados.

## 📊 Entendendo a Saída

### Símbolos do Mapa:

* `.`: Célula vazia / Caminho livre
* `#`: Obstáculo
* `A`: Posição atual do Agente de Entrega
* `D`: Posição do Destino
* `T`: Célula com alerta de tráfego (custo maior para A*)
* `*`: Célula pertencente ao caminho encontrado
* `AT`: Agente em uma célula com tráfego
* `DT`: Destino em uma célula com tráfego
* `AO`/`DO`: Agente/Destino em uma célula de obstáculo (situação de erro/debug, não deveria ocorrer em operações normais com geração válida de posições).

### Tabela de Resumo:

A tabela final apresentará as seguintes colunas:

* `Algoritmo`: Algoritmo de busca utilizado (ex: `a_star`, `bfs`).
* `Heurística`: Heurística utilizada com o A* (ex: `manhattan`, `euclidiana`, `obstaculos`, ou `N/A` para BFS).
* `Cenário`: Tipo de mapa e configuração (ex: `sem obstaculos`, `padrao`, `obstaculos aleatorios`).
* `Tráfego?`: Indica se alertas de tráfego estavam ativos (`Sim` ou `Não`).
* `Caminho?`: Indica se um caminho foi encontrado (`Sim` ou `Não`).
* `Passos`: Número de passos no caminho encontrado (comprimento do caminho).
* `Nós Exp.`: Número de nós que o algoritmo de busca expandiu para encontrar a solução (métrica de eficiência computacional).
* `Tempo (s)`: Tempo de execução do algoritmo de busca em segundos.
