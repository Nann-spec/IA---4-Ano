"""
Representacao da estrutura do grafo
- Lista de vertices ['u', 'v', ...]
- Lista de adjascencia {'u': [('v1', weight1), ('v2', wight2), ...]}
"""


class Graph:
    def __init__(self) -> None:
        self.vertex_list = []  # Lista com os vertices
        self.adjacency_list = {}  # Lista de adjascencia do grafo

    def put_vertex(self, vertex):
        """
        Insere o vertice lido na lista de vertices e cria a posicao na lista de adjascencia
        """
        if vertex not in self.vertex_list:
            self.vertex_list.append(vertex)  # Insere o vertice na lista
            self.adjacency_list[
                vertex
            ] = []  # Cria uma lista vazia na posicao do novo vertice
            return True  # Retorna flag dizendo que foi inserido com sucesso
        else:
            return False  # Retorna flag dizendo que nao foi inserido com sucesso

    def get_vertices(self):
        """
        Retorna os vertices do grafo
        """
        return self.vertex_list

    def put_edge(self, u, v, weight):
        """
        Insere uma aresta e seu peso no grafo
        """
        if u in self.vertex_list and v in self.vertex_list:
            self.adjacency_list[u].append(
                (v, weight)
            )  # Coloca v e o peso na lista de adjascencia de u
            self.adjacency_list[v].append(
                (u, weight)
            )  # Coloca u e o peso na lista de adjascencia de v
            return True  # Retorna flag dizendo que foi inserido com sucesso
        else:
            return False  # Retorna flag dizendo que nao foi inserido com sucesso

    def get_adjacencies(self):
        """
        Retorna a lista de adjascencia
        """
        return self.adjacency_list

    def print_graph(self):
        """
        Imprime o grafo por completo
        """
        print("Grafo:")
        for vertex, adjacencies in self.adjacency_list.items():
            print(f"Vertice: {vertex} - Adjascencias:")
            for adjacency in adjacencies:
                print(f"{vertex} --{adjacency[1]}--> {adjacency[0]}")
            print()
