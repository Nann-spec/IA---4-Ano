from graph.search_algorithms import bfs
from graph.structure import Graph
from input_output.reader import Reader


def main():
    # Inicializa o grafo
    graph = Graph()
    reader = Reader()

    # Define o caminho do arquivo de entrada
    file_path = "example_cities.txt"

    print(f"Carregando grafo de: {file_path}")
    if reader.read_input(graph, file_path):
        print("Grafo carregado com sucesso!\n")

        # Visualizacao do grafo
        graph.print_graph()

        # Exemplo de busca
        start_node = "ARAD"
        end_node = "BUCHAREST"

        print(f"Buscando caminho (BFS) de {start_node} para {end_node}...")
        visited_order, path = bfs(graph, start_node, end_node)

        if path:
            print(f"Caminho encontrado: {' -> '.join(path)}")
        else:
            print("Nenhum caminho encontrado.")
    else:
        print("Falha ao carregar o grafo.")


if __name__ == "__main__":
    main()
