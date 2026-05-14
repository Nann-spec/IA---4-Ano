import math
import tkinter as tk
from tkinter import messagebox

from graph.search_algorithms import a_star, bfs, dfs, dls, greedy_search, ida_star, ucs
from graph.structure import Graph
from input_output.reader import Reader
from utils.constants import HEIGHT, HEIGHT_CANVAS, ROMANIA_LAT_LON, WIDTH, WIDTH_CANVAS


class GraphInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Grafo - Cidades")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")

        self.graph = Graph()
        self.reader = Reader()
        self.node_positions = {}
        self.node_radius = 20

        # Atributos para controle de animação e arrasto
        self.dragged_node = None
        self.current_highlight_path = None
        self.animation_visited = []
        self.animation_current = None
        self.animation_queue = []
        self.is_animating = False

        # Carregar dados
        self.load_data()

        # UI Components
        self.canvas = tk.Canvas(
            self.root, bg="white", width=WIDTH_CANVAS, height=HEIGHT_CANVAS
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bindings para arrastar
        self.canvas.bind("<Button-1>", self.on_node_press)
        self.canvas.bind("<B1-Motion>", self.on_node_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_node_release)

        self.control_panel = tk.Frame(self.root, width=200, bg="lightgrey")
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.setup_controls()

        # Calcular posições iniciais (Layout Circular)
        self.calculate_layout()
        self.draw_graph()

    def load_data(self):
        file_path = "example_cities.txt"
        if not self.reader.read_input(self.graph, file_path):
            messagebox.showerror("Erro", f"Não foi possível carregar {file_path}")

    def setup_controls(self):
        tk.Label(
            self.control_panel,
            text="Algoritmo de Busca",
            bg="lightgrey",
            font=("Arial", 12, "bold"),
        ).pack(pady=10)

        tk.Label(
            self.control_panel,
            text="Busca Não Informada",
            bg="lightgrey",
            font=("Arial", 10, "bold"),
        ).pack(pady=10)

        # Seleção de Algoritmo
        self.algorithm_var = tk.StringVar(value="BFS")
        tk.Radiobutton(
            self.control_panel,
            text="BFS (Largura)",
            variable=self.algorithm_var,
            value="BFS",
            bg="lightgrey",
        ).pack(anchor=tk.W, padx=20)
        tk.Radiobutton(
            self.control_panel,
            text="DFS (Profundidade)",
            variable=self.algorithm_var,
            value="DFS",
            bg="lightgrey",
        ).pack(anchor=tk.W, padx=20)
        tk.Radiobutton(
            self.control_panel,
            text="UCS (Custo Uniforme)",
            variable=self.algorithm_var,
            value="UCS",
            bg="lightgrey",
        ).pack(anchor=tk.W, padx=20)
        tk.Radiobutton(
            self.control_panel,
            text="DLS (Prof. Limitada)",
            variable=self.algorithm_var,
            value="DLS",
            bg="lightgrey",
        ).pack(anchor=tk.W, padx=20)

        # Campo para Profundidade Limitada
        self.limit_frame = tk.Frame(self.control_panel, bg="lightgrey")
        self.limit_frame.pack(pady=5)
        tk.Label(self.limit_frame, text="Limite (DLS):", bg="lightgrey").pack(
            side=tk.LEFT
        )
        self.limit_spinbox = tk.Spinbox(self.limit_frame, from_=0, to=20, width=5)
        self.limit_spinbox.pack(side=tk.LEFT, padx=5)
        self.limit_spinbox.delete(0, "end")
        self.limit_spinbox.insert(0, "3")  # Valor padrao

        tk.Label(
            self.control_panel,
            text="Busca Informada",
            bg="lightgrey",
            font=("Arial", 10, "bold"),
        ).pack(pady=10)

        tk.Radiobutton(
            self.control_panel,
            text="GFS (Gulosa)",
            variable=self.algorithm_var,
            value="GFS",
            bg="lightgrey",
        ).pack(anchor=tk.W, padx=20)
        tk.Radiobutton(
            self.control_panel,
            text="A* (A-Estrela)",
            variable=self.algorithm_var,
            value="A*",
            bg="lightgrey",
        ).pack(anchor=tk.W, padx=20)
        tk.Radiobutton(
            self.control_panel,
            text="IDA* (Iterativo A*)",
            variable=self.algorithm_var,
            value="IDA*",
            bg="lightgrey",
        ).pack(anchor=tk.W, padx=20)

        tk.Label(self.control_panel, text="Origem:", bg="lightgrey").pack(pady=(10, 0))
        self.start_var = tk.StringVar()
        self.start_menu = tk.OptionMenu(
            self.control_panel, self.start_var, *sorted(self.graph.get_vertices())
        )
        self.start_menu.pack(pady=5)

        tk.Label(self.control_panel, text="Destino:", bg="lightgrey").pack()
        self.goal_var = tk.StringVar()
        self.goal_menu = tk.OptionMenu(
            self.control_panel, self.goal_var, *sorted(self.graph.get_vertices())
        )
        self.goal_menu.pack(pady=5)

        tk.Button(
            self.control_panel,
            text="Encontrar Caminho",
            command=self.start_search_animation,
        ).pack(pady=20)
        tk.Button(
            self.control_panel, text="Limpar", command=self.clear_highlights
        ).pack(pady=5)

        self.path_label = tk.Label(
            self.control_panel, text="", bg="lightgrey", wraplength=180, justify="left"
        )
        self.path_label.pack(pady=20)

    def calculate_layout(self):
        # Obter os vertices do grafo
        vertices = self.graph.get_vertices()

        # Obter as latitudes e longitudes das cidades
        lats = [city["lat"] for city in ROMANIA_LAT_LON.values()]
        lons = [city["lon"] for city in ROMANIA_LAT_LON.values()]

        # Obter a latitude e longitude minima e maxima
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)

        # Padronizar de latitude/longitude para coordenadas da tela (x,y)
        for i, vertex in enumerate(vertices):
            lat, lon = ROMANIA_LAT_LON[vertex]["lat"], ROMANIA_LAT_LON[vertex]["lon"]
            x = (WIDTH_CANVAS * 0.05) + (lon - min_lon) / (
                max_lon - min_lon
            ) * WIDTH_CANVAS
            y = (HEIGHT_CANVAS + HEIGHT_CANVAS * 0.07) - (lat - min_lat) / (
                max_lat - min_lat
            ) * HEIGHT_CANVAS
            self.node_positions[vertex] = (x, y)

    def draw_graph(self):
        self.canvas.delete("all")
        adjacencies = self.graph.get_adjacencies()

        # So desenhamos arestas destacadas se NAO estivermos animando ou se a animacao acabou
        highlight_path = self.current_highlight_path if not self.is_animating else None

        # Desenhar Arestas
        drawn_edges = set()
        for u, neighbors in adjacencies.items():
            for v, weight in neighbors:
                edge = tuple(sorted((u, v)))
                if edge not in drawn_edges:
                    x1, y1 = self.node_positions[u]
                    x2, y2 = self.node_positions[v]

                    color = "black"
                    width = 1

                    if highlight_path:
                        for i in range(len(highlight_path) - 1):
                            if (
                                highlight_path[i] == u and highlight_path[i + 1] == v
                            ) or (
                                highlight_path[i] == v and highlight_path[i + 1] == u
                            ):
                                color = "red"
                                width = 3
                                break

                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    self.canvas.create_text(
                        mid_x, mid_y, text=str(weight), fill="blue", font=("Arial", 8)
                    )
                    drawn_edges.add(edge)

        # Desenhar Nodos
        for vertex, (x, y) in self.node_positions.items():
            color = "lightblue"

            # Cores durante a animação
            if self.is_animating:
                if vertex == self.animation_current:
                    color = "purple"  # Vértice atual da iteração
                elif vertex in self.animation_visited:
                    color = "lightgreen"  # Vértices já explorados

            # Cores do caminho final (sobrescreve animação se existir)
            if highlight_path and vertex in highlight_path:
                if vertex == highlight_path[0]:
                    color = "green"
                elif vertex == highlight_path[-1]:
                    color = "orange"
                else:
                    color = "yellow"

            self.canvas.create_oval(
                x - self.node_radius,
                y - self.node_radius,
                x + self.node_radius,
                y + self.node_radius,
                fill=color,
                outline="black",
                tags=("node", vertex),
            )
            self.canvas.create_text(
                x, y, text=vertex, font=("Arial", 8, "bold"), tags=("node", vertex)
            )

    def on_node_press(self, event):
        if self.is_animating:
            return
        for vertex, (x, y) in self.node_positions.items():
            if math.sqrt((event.x - x) ** 2 + (event.y - y) ** 2) <= self.node_radius:
                self.dragged_node = vertex
                break

    def on_node_drag(self, event):
        if self.dragged_node and not self.is_animating:
            self.node_positions[self.dragged_node] = (event.x, event.y)
            self.draw_graph()

    def on_node_release(self, event):
        self.dragged_node = None

    def start_search_animation(self):
        if self.is_animating:
            return

        start = self.start_var.get()
        goal = self.goal_var.get()
        algorithm = self.algorithm_var.get()

        if not start or not goal:
            messagebox.showwarning("Aviso", "Selecione origem e destino.")
            return

        # Limpa estados anteriores
        self.clear_highlights()

        # Executa o algoritmo e pega o buffer de passos
        if algorithm == "BFS":
            visited_order, path = bfs(self.graph, start, goal)
        elif algorithm == "DFS":
            visited_order, path = dfs(self.graph, start, goal)
        elif algorithm == "UCS":
            visited_order, path = ucs(self.graph, start, goal)
        elif algorithm == "DLS":
            try:
                limit = int(self.limit_spinbox.get())
                visited_order, path = dls(self.graph, start, goal, limit)
            except ValueError:
                messagebox.showerror("Erro", "Profundidade deve ser um numero inteiro.")
                return
        elif algorithm == "A*":
            visited_order, path = a_star(self.graph, start, goal)
        elif algorithm == "IDA*":
            visited_order, path = ida_star(self.graph, start, goal)
        else:
            visited_order, path = greedy_search(self.graph, start, goal)

        if not visited_order:
            messagebox.showinfo("Busca", "Nenhum vértice visitado.")
            return

        # Configura a animação
        self.animation_queue = visited_order
        self.final_path_buffer = path
        self.animation_visited = []
        self.is_animating = True
        self.path_label.config(text=f"Executando {algorithm}...")

        self.animate_step()

    def animate_step(self):
        if not self.animation_queue:
            # Fim da animação de iteração
            self.is_animating = False
            self.animation_current = None
            if self.final_path_buffer:
                self.current_highlight_path = self.final_path_buffer

                # Calcular o custo do caminho
                total_cost = 0
                adjacencies = self.graph.get_adjacencies()
                for i in range(len(self.final_path_buffer) - 1):
                    u = self.final_path_buffer[i]
                    v = self.final_path_buffer[i + 1]
                    for neighbor, weight in adjacencies.get(u, []):
                        if neighbor == v:
                            total_cost += weight
                            break

                self.path_label.config(
                    text=f"Caminho encontrado: {' -> '.join(self.current_highlight_path)}\n\nCusto Total: {total_cost}"
                )
            else:
                self.path_label.config(text="Caminho não encontrado ao final da busca.")

            self.draw_graph()
            return

        # Consome o próximo vértice do buffer
        self.animation_current = self.animation_queue.pop(0)
        self.animation_visited.append(self.animation_current)

        self.draw_graph()

        # Agenda o próximo passo (500ms de intervalo)
        self.root.after(500, self.animate_step)

    def clear_highlights(self):
        self.current_highlight_path = None
        self.animation_visited = []
        self.animation_current = None
        self.animation_queue = []
        self.is_animating = False
        self.draw_graph()
        self.path_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphInterface(root)
    root.mainloop()
