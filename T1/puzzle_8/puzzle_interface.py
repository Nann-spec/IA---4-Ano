import random
import time
import tkinter as tk
from tkinter import messagebox

from puzzle_graph import PuzzleGraph
from puzzle_logic import PuzzleState
from search_algorithms import (
    a_star,
    bfs,
    dfs,
    greedy_search,
    ida_star,
    ucs,
)


class PuzzleInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry("800x900")  # Aumentado para acomodar peças maiores

        self.goal_board = ((1, 2, 3), (4, 0, 5), (6, 7, 8))
        self.current_board = list(list(row) for row in self.goal_board)

        self.is_animating = False

        # Registra a validação do Tkinter com mais parâmetros:
        # %d: ação, %P: valor proposto, %W: nome do widget
        self.vcmd = (self.root.register(self._validate_input), "%d", "%P", "%W")

        self._setup_ui()
        self._update_grid()

    def _setup_ui(self):
        # Frame do Tabuleiro
        self.grid_frame = tk.Frame(self.root, bg="#333333", padx=20, pady=20)
        self.grid_frame.pack(pady=30)

        self.cells = []
        self.cell_vars = []
        for r in range(3):
            row_cells = []
            row_vars = []
            for c in range(3):
                var = tk.StringVar()
                # Aumentado o font size (48) e largura (4)
                entry = tk.Entry(
                    self.grid_frame,
                    textvariable=var,
                    font=("Arial", 48, "bold"),
                    width=3,
                    justify="center",
                    relief="flat",
                    bd=5,
                    validate="key",
                    validatecommand=self.vcmd,
                    bg="white",
                )
                entry.grid(row=r, column=c, padx=5, pady=5)

                # Sincroniza a edição manual com a estrutura interna
                var.trace_add(
                    "write",
                    lambda *args, row=r, col=c, v=var: self._on_cell_write(row, col, v),
                )

                row_cells.append(entry)
                row_vars.append(var)
            self.cells.append(row_cells)
            self.cell_vars.append(row_vars)

        # Painel de Controle
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Fileira 1 de botões
        btn_frame1 = tk.Frame(control_frame)
        btn_frame1.pack()

        tk.Button(
            btn_frame1, text="Embaralhar", command=self.shuffle_board, width=15
        ).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(
            btn_frame1,
            text="Limpar Tudo",
            command=self.clear_board,
            width=15,
            bg="#ffcccc",
        ).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(
            btn_frame1, text="Resetar Objetivo", command=self.reset_to_goal, width=15
        ).grid(row=0, column=2, padx=5, pady=5)

        # Fileira 2
        btn_frame2 = tk.Frame(control_frame)
        btn_frame2.pack(pady=10)

        tk.Label(btn_frame2, text="Algoritmo:", font=("Arial", 12)).grid(
            row=0, column=0, padx=5
        )
        self.algo_var = tk.StringVar(value="A*")
        algos = ["BFS", "DFS", "UCS", "A*", "IDA*", "Greedy"]
        self.algo_menu = tk.OptionMenu(btn_frame2, self.algo_var, *algos)
        self.algo_menu.config(width=10)
        self.algo_menu.grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame2,
            text="RESOLVER",
            command=self.solve_puzzle,
            width=20,
            bg="#ccffcc",
            font=("Arial", 12, "bold"),
        ).grid(row=0, column=2, padx=20)

        self.status_label = tk.Label(
            self.root,
            text="Dica: Use '0' para o espaço vazio",
            font=("Arial", 12, "italic"),
            fg="#666666",
        )
        self.status_label.pack(pady=5)

        self.result_label = tk.Label(
            self.root, text="Bem-vindo ao 8-Puzzle Solver!", font=("Arial", 14, "bold")
        )
        self.result_label.pack(pady=10)

    def _validate_input(self, action, proposed_val, widget_name):
        """Validação rigorosa em tempo real."""
        # Se for deleção, sempre permite
        if action == "0":
            return True

        # Se o campo ficar vazio, permite
        if proposed_val == "":
            return True

        # 1. Deve ser apenas um caractere e ser um dígito
        if len(proposed_val) > 1 or not proposed_val.isdigit():
            return False

        # 2. Deve estar no intervalo [0, 8]
        if not ("0" <= proposed_val <= "8"):
            return False

        # 3. Não pode ser repetido em nenhuma outra célula
        for r in range(3):
            for c in range(3):
                # Obtém o nome do widget da célula atual da iteração
                try:
                    cell_widget = self.cells[r][c]
                except (IndexError, AttributeError):
                    continue

                # Se não for o widget que estamos editando agora...
                if str(cell_widget) != widget_name:
                    # ...e o valor já existir lá, rejeita a entrada
                    if self.cell_vars[r][c].get() == proposed_val:
                        return False

        return True

    def _on_cell_write(self, r, c, var):
        """Sincroniza o valor da Entry com a matriz current_board."""
        val = var.get()
        if val.isdigit():
            self.current_board[r][c] = int(val)
        else:
            self.current_board[r][c] = -1  # Estado temporário para "vazio de digitação"

        # Atualiza cor visual do "0"
        if val == "0":
            self.cells[r][c].config(bg="#bbbbbb", fg="#bbbbbb")
        elif val == "":
            self.cells[r][c].config(bg="#eeeeee")
        else:
            self.cells[r][c].config(bg="white", fg="black")

    def _update_grid(self, board=None):
        """Atualiza os valores das Entries na tela."""
        if board is None:
            board = self.current_board

        for r in range(3):
            for c in range(3):
                val = board[r][c]
                # Se for -1 (limpo), deixamos a string vazia
                display_val = str(val) if val != -1 else ""
                self.cell_vars[r][c].set(display_val)

                if val == 0:
                    self.cells[r][c].config(bg="#bbbbbb", fg="#bbbbbb")
                elif val == -1:
                    self.cells[r][c].config(bg="#eeeeee")
                else:
                    self.cells[r][c].config(bg="white", fg="black")

    def clear_board(self):
        """Zera todos os campos para facilitar a inserção manual."""
        if self.is_animating:
            return
        self.current_board = [[-1 for _ in range(3)] for _ in range(3)]
        self._update_grid()
        self.result_label.config(text="Tabuleiro limpo. Insira os números (0-8).")

    def reset_to_goal(self):
        if self.is_animating:
            return
        self.current_board = list(list(row) for row in self.goal_board)
        self._update_grid()
        self.result_label.config(text="Tabuleiro resetado para o objetivo.")

    def shuffle_board(self):
        if self.is_animating:
            return

        # Faz movimentos aleatorios a partir do objetivo para garantir que seja soluvel
        board = list(list(row) for row in self.goal_board)
        moves = 30

        for _ in range(moves):
            state = PuzzleState(tuple(tuple(row) for row in board))
            neighbors = state.get_neighbors()
            if neighbors:
                board = [list(row) for row in random.choice(neighbors)]

        self.current_board = board
        self._update_grid()
        self.result_label.config(text="Tabuleiro embaralhado.")

    def solve_puzzle(self):
        if self.is_animating:
            return

        # Verifica se todas as células foram preenchidas
        flat_board = [val for row in self.current_board for val in row]
        if -1 in flat_board or len(set(flat_board)) != 9:
            messagebox.showwarning(
                "Aviso", "Preencha todos os campos com números únicos de 0 a 8!"
            )
            return

        start_board = tuple(tuple(row) for row in self.current_board)

        # Verificacao de solubilidade
        state = PuzzleState(start_board, goal=self.goal_board)
        if not state.is_solvable():
            messagebox.showerror(
                "Erro",
                "Este tabuleiro não possui solução!\n(A paridade das inversões é incompatível)",
            )
            return

        pg = PuzzleGraph(goal_board=self.goal_board)

        def h(state, goal):
            return PuzzleState(state, goal=goal).manhattan_distance()

        algo_name = self.algo_var.get()
        self.result_label.config(text=f"Resolvendo com {algo_name}...")
        self.root.update()

        start_time = time.time()

        try:
            if algo_name == "BFS":
                visited, path = bfs(pg, start_board, self.goal_board)
            elif algo_name == "DFS":
                visited, path = dfs(pg, start_board, self.goal_board)
            elif algo_name == "UCS":
                visited, path = ucs(pg, start_board, self.goal_board)
            elif algo_name == "A*":
                visited, path = a_star(pg, start_board, self.goal_board, h)
            elif algo_name == "IDA*":
                visited, path = ida_star(pg, start_board, self.goal_board, h)
            elif algo_name == "Greedy":
                visited, path = greedy_search(pg, start_board, self.goal_board, h)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a busca: {e}")
            return

        end_time = time.time()

        if path:
            self.result_label.config(
                text=f"Sucesso! {len(path) - 1} movimentos em {end_time - start_time:.2f}s"
            )
            self.animate_solution(path)
        else:
            self.result_label.config(text="Falha ao encontrar solucao.")

    def animate_solution(self, path):
        self.is_animating = True
        # Bloqueia edição durante animação
        self._set_cells_state("disabled")

        def step(index):
            if index < len(path):
                self._update_grid(path[index])
                self.current_board = [list(row) for row in path[index]]
                self.root.after(300, lambda: step(index + 1))
            else:
                self.is_animating = False
                self._set_cells_state("normal")

        step(0)

    def _set_cells_state(self, state):
        for r in range(3):
            for c in range(3):
                self.cells[r][c].config(state=state)


if __name__ == "__main__":
    root = tk.Tk()
    PuzzleInterface(root)
    root.mainloop()
