import os


class Reader:
    def __init__(self):
        pass

    def read_input(self, graph, file_name=""):
        """
        Le o arquivo de entrada e preenche o grafo.
        O arquivo segue o padrao:
        # VERTICES
        V1
        V2
        ...
        # EDGES
        V1 V2 peso
        ...
        """
        if not os.path.exists(file_name):
            print(f"Erro: Arquivo {file_name} nao encontrado.")
            return False

        current_section = None

        try:
            with open(file_name, "r") as file:
                for line in file:
                    line = line.strip()

                    # Ignora linhas vazias
                    if not line:
                        continue

                    # Verifica demarcadores
                    if line.startswith("#"):
                        if "VERTICES" in line:
                            current_section = "VERTICES"
                        elif "EDGES" in line:
                            current_section = "EDGES"
                        continue

                    # Processa de acordo com a secao atual
                    if current_section == "VERTICES":
                        graph.put_vertex(line)
                    elif current_section == "EDGES":
                        parts = line.split()
                        if len(parts) == 3:
                            u, v, weight = parts
                            # Converte peso para float ou int se possivel
                            try:
                                weight = float(weight)
                                if weight.is_integer():
                                    weight = int(weight)
                            except ValueError:
                                pass

                            graph.put_edge(u, v, weight)
                        else:
                            print(f"Aviso: Linha de aresta invalida ignorada: {line}")

            return True

        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False
