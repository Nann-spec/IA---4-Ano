# **8-Puzzle Solver**

Este projeto é uma implementação do clássico jogo **8-Puzzle** (quebra-cabeça de 8 peças), utilizando diversos algoritmos de busca de Inteligência Artificial para encontrar a solução otimizada.

---

## **Como Executar**

### **Pré-requisitos**
*   **Python 3.x** instalado.
*   A biblioteca `tkinter` (nativa do Python na maioria das instalações).

### **Execução**
No terminal, navegue até a pasta `puzzle_8` e execute o comando:

```bash
python .\main_puzzle.py
```

---

## **Organização dos Arquivos**

O projeto está estruturado de forma modular para separar a interface, a lógica do jogo e os algoritmos de busca:

*   **`main_puzzle.py`**: Ponto de entrada da aplicação. Inicializa a janela principal do Tkinter e a classe de interface.
*   **`puzzle_interface.py`**: Gerencia toda a interface gráfica. Inclui a criação dos grids, captura de inputs, animações de busca e exibição de resultados no terminal interno.
*   **`puzzle_logic.py`**: Contém a classe `PuzzleState`, que define as regras do jogo, geração de estados vizinhos, cálculo de distância de Manhattan e a lógica de verificação de **solubilidade**.
*   **`puzzle_graph.py`**: Implementa a classe `PuzzleGraph`, que adapta a lógica do puzzle para ser consumida pelos algoritmos de busca, incluindo as funções de heurística.
*   **`search_algorithms.py`**: Implementação pura dos algoritmos de busca (BFS, DFS, A*, etc.), permitindo que sejam testados ou usados de forma independente da interface.

---

## **Algoritmos Implementados**

O solver permite escolher entre diversos algoritmos de busca, cada um com comportamentos distintos:

1.  **Busca em Largura (BFS)**: Garante o caminho mais curto, mas consome muita memória.
2.  **Busca em Profundidade (DFS)**: Explora caminhos profundos, não garante a melhor solução e pode entrar em loops sem controle de estados visitados.
3.  **Busca em Profundidade Limitada (DLS)**: DFS com um limite máximo de profundidade definido pelo usuário.
4.  **Busca de Custo Uniforme (UCS)**: Busca baseada no custo acumulado (neste caso, cada movimento custa 1).
5.  **Busca A\* (A-Star)**: Busca informada que utiliza a **Distância de Manhattan** como heurística. É geralmente a mais eficiente.
6.  **IDA\* (Iterative Deepening A\*)**: Versão do A* que economiza memória utilizando profundidade iterativa.
7.  **Busca Gananciosa (Greedy)**: Foca apenas na heurística para decidir o próximo passo, sendo muito rápida mas nem sempre ótima.

---

## **Funcionalidades Especiais**

*   **Objetivo Dinâmico**: Diferente de implementações padrão, este programa permite que o usuário defina o estado final (objetivo) desejado. A interface valida automaticamente se o objetivo proposto é alcançável a partir do estado inicial.
*   **Animação da Busca**: A interface mostra em tempo real os estados que o algoritmo está explorando antes de mostrar a solução final.
*   **Terminal Integrado**: Exibe o passo a passo da solução em formato ASCII, facilitando o acompanhamento técnico do algoritmo.
*   **Validação de Solubilidade**: O programa utiliza cálculos de inversões para avisar o usuário imediatamente se um tabuleiro não possui solução para o objetivo definido.

---

## **Tecnologias Utilizadas**
*   **Linguagem**: Python 3
*   **Interface**: Tkinter
*   **Paradigma**: Orientação a Objetos
