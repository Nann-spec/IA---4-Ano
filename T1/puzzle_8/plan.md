# Planejamento de Implementação: 8-Puzzle Solver

Este documento detalha a estratégia para a implementação do quebra-cabeça de 8 peças (8-Puzzle) integrado ao sistema de algoritmos de busca desenvolvido.

---

## 1. Representação do Grafo (State-Space Graph)
Diferente de mapas estáticos, o grafo do 8-Puzzle é gerado dinamicamente durante a exploração.

- **Nó (Vértice):** Representa uma configuração específica do tabuleiro 3x3.
    - *Formato:* Uma tupla de tuplas, ex: `((1, 2, 3), (4, 0, 5), (6, 7, 8))`, onde `0` é o espaço vazio.
- **Aresta (Arco):** Representa um movimento legal do espaço vazio (Cima, Baixo, Esquerda, Direita).
    - *Custo:* Cada movimento possui peso fixo de **1**.
- **Estado Inicial:** Definido pelo usuário através da interface.
- **Estado Objetivo:** Configuração final desejada (ex: peças ordenadas de 1 a 8).

---

## 2. Montagem do Grafo conforme a Configuração Inicial
O grafo será montado de forma "lazy" (sob demanda) para otimizar o uso de memória.

- **Geração de Vizinhos:** Para cada estado, o sistema identifica a posição do espaço vazio e gera até 4 estados adjacentes possíveis.
- **Verificação de Solubilidade:** Antes de iniciar a busca, o sistema utiliza a contagem de inversões para garantir que o quebra-cabeça pode ser resolvido.
- **Cálculo da Heurística:**
    - O sistema calculará automaticamente a **Distância de Manhattan** (soma das distâncias horizontais e verticais de cada peça até seu destino) para guiar algoritmos como A* e IDA*.

---

## 3. Interface do Puzzle
A interface servirá tanto para entrada de dados quanto para visualização da solução.

- **Configuração Inicial:**
    - Uma grade de entrada 3x3 onde o usuário digita os números de 0 a 8.
    - Botão **"Aleatório"**: Gera uma configuração randômica que seja comprovadamente resolúvel.
- **Controles de Execução:**
    - Menu suspenso para selecionar o algoritmo (A*, IDA*, Greedy, etc.).
    - Botão de execução para iniciar a animação do solver.
- **Visualização:**
    - O tabuleiro será atualizado em tempo real para mostrar os movimentos encontrados pelo algoritmo.

---

## 4. Tecnologias e Bibliotecas
Para manter a integração com o projeto atual e garantir a melhor performance visual:

- **Biblioteca Principal:** `Tkinter` (Python Standard Library).
    - **Vantagens:** Já está sendo utilizada no `graph_interface.py`, facilita a criação da grade 3x3 usando o gerenciador de layout `.grid()`, e é nativa do Python.
- **Lógica de Busca:** Reutilização das funções em `search_algorithms.py` com adaptação para grafos dinâmicos.

---

Este planejamento segue as diretrizes do livro *Artificial Intelligence: A Modern Approach* de Russell & Norvig.
