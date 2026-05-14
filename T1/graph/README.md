# **Graph Visualizer & Solver**

Este módulo é uma ferramenta interativa para visualização de grafos e execução de algoritmos de busca, utilizando como exemplo clássico o mapa de cidades da **Romênia**.

---

## **Como Executar**

### **Pré-requisitos**
*   **Python 3.x** instalado.
*   A biblioteca `tkinter` (nativa do Python na maioria das instalações).

### **Execução**
No terminal, navegue até a pasta `graph` e execute o comando:

```bash
python .\graph_interface.py
```

---

## **Organização dos Arquivos**

A estrutura está organizada para separar a lógica de dados, os algoritmos e a visualização:

*   **`graph_interface.py`**: Arquivo principal que lança a interface gráfica. Gerencia o Canvas de desenho, eventos de arrastar nodos e a lógica de animação da busca.
*   **`structure.py`**: Define a classe `Graph`, que implementa um grafo não direcionado ponderado usando uma lista de adjacências.
*   **`search_algorithms.py`**: Implementação dos algoritmos de busca (BFS, DFS, UCS, DLS, A*, etc.). Inclui uma função de heurística baseada na distância euclidiana das coordenadas reais das cidades.
*   **`input_output/reader.py`**: Utilitário para ler a definição do grafo (vértices e arestas) a partir de arquivos de texto.
*   **`utils/constants.py`**: Contém dados estáticos, como as coordenadas de latitude e longitude das cidades da Romênia e configurações da interface.
*   **`example_cities.txt`**: Arquivo de dados que define as conexões e pesos (distâncias) entre as cidades.

---

## **Algoritmos de Busca**

O visualizador permite testar dois tipos de busca:

### **Busca Não Informada**
1.  **BFS (Largura)**: Encontra o caminho com menos arestas.
2.  **DFS (Profundidade)**: Explora o caminho mais longo primeiro.
3.  **UCS (Custo Uniforme)**: Encontra o caminho de menor custo acumulado (Dijkstra).
4.  **DLS (Profundidade Limitada)**: DFS que interrompe a busca em uma profundidade específica.

### **Busca Informada (Heurística)**
5.  **GFS (Gulosa)**: Expande o nodo que parece estar mais perto do objetivo segundo a heurística.
6.  **A\* (A-Estrela)**: Combina o custo real (UCS) com a heurística para encontrar o caminho ótimo de forma eficiente.
7.  **IDA\* (Iterativo A\*)**: Versão do A* que utiliza menos memória através de aprofundamento iterativo.

---

## **Funcionalidades da Interface**

*   **Arrastar Nodos**: Você pode clicar e arrastar as cidades no mapa para reorganizar a visualização conforme desejar.
*   **Animação em Tempo Real**: Ao iniciar uma busca, a interface destaca em **Roxo** o nodo atual sendo explorado e em **Verde Claro** os nodos já visitados.
*   **Destaque do Caminho**: Após a conclusão, o caminho final é traçado em **Vermelho**, com o nodo de origem em **Verde** e o de destino em **Laranja**.
*   **Cálculo de Custo**: O painel lateral exibe o caminho completo encontrado e o custo total da rota (soma dos pesos das arestas).
*   **Layout Geográfico**: Por padrão, o programa posiciona as cidades baseando-se em suas latitudes e longitudes reais, simulando o mapa geográfico.

---

## **Tecnologias Utilizadas**
*   **Linguagem**: Python 3
*   **Interface**: Tkinter (Canvas para desenho dinâmico)
*   **Heurística**: Distância Euclidiana baseada em coordenadas geográficas.
