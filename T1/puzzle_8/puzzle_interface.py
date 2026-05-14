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
    dls,
    greedy_search,
    ida_star,
    ucs,
)


class PuzzleInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry("1200x850")
        self.root.configure(bg="#fefefe")

        # self.goal_board = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
        self.goal_board = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
        self.current_board = [list(row) for row in self.goal_board]

        self.is_animating = False
        self.search_buffer = []
        self.solution_path = []

        # Registra a validação do Tkinter
        self.vcmd = (self.root.register(self._validate_input), "%d", "%P", "%W")

        self.current_cells = []
        self.current_vars = []
        self.goal_cells = []
        self.goal_vars = []

        self._setup_ui()
        self._update_grid(self.current_board, self.current_vars, self.current_cells)
        self._update_grid(self.goal_board, self.goal_vars, self.goal_cells)

    def _setup_ui(self):
        # Container Principal para separar Esquerda (Puzzle) da Direita (Terminal)
        main_container = tk.Frame(self.root, bg="#fefefe")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Lado Esquerdo: Puzzle e Controles
        left_frame = tk.Frame(main_container, bg="#fefefe")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Container para os Tabuleiros
        grids_container = tk.Frame(left_frame, bg="#fefefe")
        grids_container.pack(pady=20)

        # Tabuleiro Atual
        current_container = tk.Frame(grids_container, bg="#fefefe")
        current_container.pack(side=tk.LEFT, padx=15)
        tk.Label(
            current_container,
            text="Estado Atual",
            font=("Arial", 12, "bold"),
            bg="#fefefe",
        ).pack(pady=5)
        self.grid_frame = self._create_grid_ui(
            current_container, self.current_vars, self.current_cells, self.current_board
        )

        # Tabuleiro Objetivo
        goal_container = tk.Frame(grids_container, bg="#fefefe")
        goal_container.pack(side=tk.LEFT, padx=15)
        tk.Label(
            goal_container, text="Objetivo", font=("Arial", 12, "bold"), bg="#fefefe"
        ).pack(pady=5)
        self.goal_grid_frame = self._create_grid_ui(
            goal_container, self.goal_vars, self.goal_cells, self.goal_board
        )

        # 1. Botões de Ação (Horizontal)
        action_frame = tk.Frame(left_frame, bg="#fefefe")
        action_frame.pack(pady=10)

        tk.Button(
            action_frame,
            text="Embaralhar",
            command=self.shuffle_board,
            width=15,
            bg="#cfe2f3",
            fg="#3c78d8",
            relief="flat",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            action_frame,
            text="Limpar Tudo",
            command=self.clear_board,
            width=15,
            bg="#f8d7da",
            fg="#dc3545",
            relief="flat",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            action_frame,
            text="Resetar Atual",
            command=self.reset_to_goal,
            width=15,
            bg="#e0e0e0",
            fg="#333333",
            relief="flat",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        # 2. Configurações de Algoritmo e Profundidade
        config_frame = tk.Frame(left_frame, bg="#fefefe", pady=10)
        config_frame.pack()

        # Linha de Rótulos
        label_row = tk.Frame(config_frame, bg="#fefefe")
        label_row.pack(fill="x")

        tk.Label(
            label_row,
            text="Algoritmo:",
            font=("Arial", 12),
            bg="#fefefe",
            fg="#333333",
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(
            label_row,
            text="Profundidade:",
            font=("Arial", 12),
            bg="#fefefe",
            fg="#333333",
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT)

        # Linha de Inputs
        input_row = tk.Frame(config_frame, bg="#fefefe")
        input_row.pack(fill="x", pady=(5, 15))

        self.algo_var = tk.StringVar(value="A*")
        algos = ["BFS", "DFS", "DLS", "UCS", "A*", "IDA*", "Greedy"]
        self.algo_menu = tk.OptionMenu(input_row, self.algo_var, *algos)
        self.algo_menu.config(
            width=12, relief="flat", bg="#ffffff", activebackground="#f0f0f0"
        )
        self.algo_menu.pack(side=tk.LEFT, padx=(0, 20))

        self.depth_var = tk.IntVar(value=10)
        self.depth_spin = tk.Spinbox(
            input_row,
            from_=1,
            to=1000,
            textvariable=self.depth_var,
            width=8,
            font=("Arial", 12),
            relief="flat",
            bg="#ffffff",
        )
        self.depth_spin.pack(side=tk.LEFT)

        # 3. Velocidade
        tk.Label(
            left_frame,
            text="Velocidade (ms):",
            font=("Arial", 12),
            bg="#fefefe",
            fg="#333333",
        ).pack()

        self.speed_scale = tk.Scale(
            left_frame,
            from_=1,
            to=1000,
            orient=tk.HORIZONTAL,
            length=300,
            bg="#fefefe",
            highlightthickness=0,
            troughcolor="#d0d0d0",
            activebackground="#a4c2f4",
        )
        self.speed_scale.set(300)
        self.speed_scale.pack(pady=(0, 20))

        # 4. Ação Principal e Status
        self.solve_btn = tk.Button(
            left_frame,
            text="RESOLVER",
            command=self.solve_puzzle,
            width=25,
            bg="#a4c2f4",
            fg="#ffffff",
            font=("Arial", 14, "bold"),
            relief="flat",
        )
        self.solve_btn.pack(pady=10)

        # Passos para Solução
        steps_frame = tk.Frame(left_frame, bg="#fefefe")
        steps_frame.pack(pady=5)

        tk.Label(
            steps_frame,
            text="Passos para solução: ",
            font=("Arial", 12, "bold"),
            bg="#fefefe",
            fg="#333333",
        ).pack(side=tk.LEFT)
        self.steps_val_label = tk.Label(
            steps_frame,
            text="-",
            font=("Arial", 12, "bold"),
            bg="#fefefe",
            fg="#007bff",
        )
        self.steps_val_label.pack(side=tk.LEFT)

        # Rodapé
        self.result_label = tk.Label(
            left_frame,
            text="Bem-vindo ao 8-Puzzle Solver!",
            font=("Arial", 14, "bold"),
            bg="#fefefe",
            fg="#333333",
        )
        self.result_label.pack(pady=(20, 5))

        self.status_label = tk.Label(
            left_frame,
            text="Dica: Use '0' para o espaço vazio",
            font=("Arial", 12, "italic"),
            fg="#888888",
            bg="#fefefe",
        )
        self.status_label.pack(pady=5)

        # Lado Direito: Terminal de Texto
        right_frame = tk.Frame(main_container, bg="#fefefe", padx=20)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            right_frame,
            text="Caminho da Solução:",
            font=("Arial", 12, "bold"),
            bg="#fefefe",
            fg="#333333",
        ).pack(anchor="w", pady=(0, 10))

        terminal_container = tk.Frame(right_frame, bg="#d0d0d0", padx=1, pady=1)
        terminal_container.pack(fill=tk.BOTH, expand=True)

        self.terminal_scroll = tk.Scrollbar(terminal_container)
        self.terminal_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.terminal = tk.Text(
            terminal_container,
            bg="#f4f4f4",
            fg="#333333",
            font=("Courier", 12),
            padx=10,
            pady=10,
            relief="flat",
            yscrollcommand=self.terminal_scroll.set,
            state="disabled",
            width=30,
        )
        self.terminal.pack(fill=tk.BOTH, expand=True)
        self.terminal_scroll.config(command=self.terminal.yview)

    def _validate_input(self, action, proposed_val, widget_name):
        if action == "0":
            return True
        if proposed_val == "":
            return True
        if len(proposed_val) > 1 or not proposed_val.isdigit():
            return False
        if not ("0" <= proposed_val <= "8"):
            return False

        # Identifica em qual grid estamos para validar duplicatas localmente
        target_vars = self.current_vars
        target_cells = self.current_cells

        # Verifica se o widget pertence ao grid de objetivo
        found_in_goal = False
        for r in range(3):
            for c in range(3):
                if str(self.goal_cells[r][c]) == widget_name:
                    target_vars = self.goal_vars
                    target_cells = self.goal_cells
                    found_in_goal = True
                    break
            if found_in_goal:
                break

        for r in range(3):
            for c in range(3):
                try:
                    cell_widget = target_cells[r][c]
                except:
                    continue
                if str(cell_widget) != widget_name:
                    if target_vars[r][c].get() == proposed_val:
                        return False
        return True

    def _on_cell_write(self, r, c, var, board, row_cells):
        val = var.get()
        if val.isdigit():
            board[r][c] = int(val)
        else:
            board[r][c] = -1

        cell = row_cells[c]
        if val == "0":
            cell.config(bg="#f0f0f0", fg="#f0f0f0")
        elif val == "":
            cell.config(bg="#f0f0f0")
        else:
            cell.config(bg="#ffffff", fg="#333333")

    def _update_grid(self, board, vars_list, cells_list):
        for r in range(3):
            for c in range(3):
                val = board[r][c]
                display_val = str(val) if val != -1 else ""
                vars_list[r][c].set(display_val)
                if val == 0:
                    cells_list[r][c].config(bg="#f0f0f0", fg="#f0f0f0")
                elif val == -1:
                    cells_list[r][c].config(bg="#f0f0f0")
                else:
                    cells_list[r][c].config(bg="#ffffff", fg="#333333")

    def _create_grid_ui(self, parent, vars_list, cells_list, board):
        grid_frame = tk.Frame(parent, bg="#d0d0d0", padx=2, pady=2)
        grid_frame.pack()

        for r in range(3):
            row_cells = []
            row_vars = []
            for c in range(3):
                var = tk.StringVar()
                entry = tk.Entry(
                    grid_frame,
                    textvariable=var,
                    font=("Arial", 32, "bold"),
                    width=3,
                    justify="center",
                    relief="flat",
                    bd=0,
                    validate="key",
                    validatecommand=self.vcmd,
                    bg="white",
                )
                entry.grid(row=r, column=c, padx=1, pady=1)
                var.trace_add(
                    "write",
                    lambda *args, row=r, col=c, v=var, b=board, clls=row_cells: (
                        self._on_cell_write(row, col, v, b, clls)
                    ),
                )
                row_cells.append(entry)
                row_vars.append(var)
            cells_list.append(row_cells)
            vars_list.append(row_vars)
        return grid_frame

    def _format_board_ascii(self, board):
        """Formata o tabuleiro no padrão:
        x1 | x2 | x3
        ------------
        x4 | x5 | x6
        ------------
        x7 | x8 | x9
        """
        rows = []
        for r in range(3):
            rows.append(" | ".join(map(str, board[r])))
        return "\n------------\n".join(rows)

    def _append_to_terminal(self, text):
        """Adiciona texto ao terminal e faz scroll para o final."""
        self.terminal.config(state="normal")
        self.terminal.insert(tk.END, text + "\n")
        self.terminal.config(state="disabled")
        self.terminal.see(tk.END)

    def _clear_terminal(self):
        """Limpa todo o conteúdo do terminal."""
        self.terminal.config(state="normal")
        self.terminal.delete("1.0", tk.END)
        self.terminal.config(state="disabled")

    def clear_board(self):
        if self.is_animating:
            return
        self.current_board = [[-1 for _ in range(3)] for _ in range(3)]
        self._update_grid(self.current_board, self.current_vars, self.current_cells)
        self._clear_terminal()

    def reset_to_goal(self):
        if self.is_animating:
            return
        self.current_board = [list(row) for row in self.goal_board]
        self._update_grid(self.current_board, self.current_vars, self.current_cells)
        self._clear_terminal()

    def shuffle_board(self):
        if self.is_animating:
            return

        # Garante que temos um objetivo válido antes de embaralhar
        flat_goal = [val for row in self.goal_board for val in row]
        if -1 in flat_goal or len(set(flat_goal)) != 9:
            messagebox.showwarning(
                "Aviso", "Preencha o objetivo corretamente antes de embaralhar!"
            )
            return

        board = [list(row) for row in self.goal_board]
        goal_tuple = tuple(tuple(row) for row in self.goal_board)
        for _ in range(30):
            state = PuzzleState(tuple(tuple(row) for row in board), goal=goal_tuple)
            neighbors = state.get_neighbors()
            if neighbors:
                board = [list(row) for row in random.choice(neighbors)]
        self.current_board = board
        self._update_grid(self.current_board, self.current_vars, self.current_cells)
        self._clear_terminal()

    def solve_puzzle(self):
        if self.is_animating:
            return

        # Reseta campo de passos e terminal
        self.steps_val_label.config(text="-")
        self._clear_terminal()

        # Valida Estado Atual
        flat_current = [val for row in self.current_board for val in row]
        if -1 in flat_current or len(set(flat_current)) != 9:
            messagebox.showwarning("Aviso", "Preencha o Estado Atual corretamente!")
            return

        # Valida Objetivo
        flat_goal = [val for row in self.goal_board for val in row]
        if -1 in flat_goal or len(set(flat_goal)) != 9:
            messagebox.showwarning("Aviso", "Preencha o Objetivo corretamente!")
            return

        start_board = tuple(tuple(row) for row in self.current_board)
        goal_board = tuple(tuple(row) for row in self.goal_board)

        if not PuzzleState(start_board, goal=goal_board).is_solvable():
            messagebox.showerror(
                "Erro", "Este tabuleiro não possui solução para este objetivo!"
            )
            return

        pg = PuzzleGraph(goal_board=goal_board)
        h = pg.get_heuristic
        algo_name = self.algo_var.get()

        self.result_label.config(text=f"Buscando solução com {algo_name}...")
        self.root.update()

        start_t = time.time()
        try:
            if algo_name == "BFS":
                visited, path = bfs(pg, start_board, goal_board)
            elif algo_name == "DFS":
                visited, path = dfs(pg, start_board, goal_board)
            elif algo_name == "DLS":
                limit = self.depth_var.get()
                visited, path = dls(pg, start_board, goal_board, limit)
            elif algo_name == "UCS":
                visited, path = ucs(pg, start_board, goal_board)
            elif algo_name == "A*":
                visited, path = a_star(pg, start_board, goal_board, h)
            elif algo_name == "IDA*":
                visited, path = ida_star(pg, start_board, goal_board, h)
            elif algo_name == "Greedy":
                visited, path = greedy_search(pg, start_board, goal_board, h)
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return
        end_t = time.time()

        if path:
            self.search_buffer = visited
            self.solution_path = path
            num_steps = len(path) - 1
            self.steps_val_label.config(text=str(num_steps))
            self.result_label.config(
                text=f"Busca finalizada ({end_t - start_t:.2f}s). Animando interação..."
            )

            # Preenche o terminal com o caminho (Otimizado para caminhos longos)
            terminal_lines = []
            terminal_lines.append(f"=== ALGORITMO: {algo_name} ===")
            terminal_lines.append(f"Tempo: {end_t - start_t:.4f}s")
            terminal_lines.append(f"Estados visitados: {len(visited)}")
            terminal_lines.append(f"Caminho encontrado: {num_steps} passos\n")

            # Se o caminho for muito longo (ex: DFS), mostramos apenas o início e o fim no terminal
            # para manter a performance da interface.
            display_path = path
            is_truncated = False
            if len(path) > 100:
                display_path = path[:50] + [None] + path[-50:]
                is_truncated = True

            for i, board in enumerate(display_path):
                if board is None:
                    terminal_lines.append(
                        "\n... (omitindo passos intermediários para performance) ...\n"
                    )
                    continue

                # Calcula o índice real do passo para exibição
                if not is_truncated or i < 50:
                    real_idx = i
                else:
                    real_idx = len(path) - (len(display_path) - i)

                if real_idx == 0:
                    terminal_lines.append("--- ESTADO INICIAL ---")
                elif real_idx == len(path) - 1:
                    terminal_lines.append("--- ESTADO FINAL (OBJETIVO) ---")
                else:
                    terminal_lines.append(f"--- PASSO {real_idx} ---")

                terminal_lines.append(self._format_board_ascii(board))
                terminal_lines.append("")  # Linha em branco para separar

            # Insere tudo de uma vez no terminal para maior eficiência
            self._append_to_terminal("\n".join(terminal_lines))

            self.animate_search()
        else:
            self.result_label.config(text="Solução não encontrada.")
            self._append_to_terminal("Solução não encontrada pelo algoritmo.")

    def animate_search(self):
        self.is_animating = True
        self._set_cells_state("disabled")

        # Como o 8-puzzle pode ter milhares de estados visitados,
        # vamos mostrar apenas uma amostra ou acelerar muito a animação.
        # Mostraremos os primeiros 50 estados e os últimos 10 para dar a ideia da busca.
        if len(self.search_buffer) > 100:
            sample = self.search_buffer[:50] + [None] + self.search_buffer[-10:]
        else:
            sample = self.search_buffer

        def step(index):
            if index < len(sample):
                state = sample[index]
                # Busca é 10x mais rápida que o slider para não demorar demais
                delay = max(10, self.speed_scale.get() // 10)
                if state is None:  # Marcador de pulo
                    self.result_label.config(
                        text="... pulando estados intermediários ..."
                    )
                    self.root.after(500, lambda: step(index + 1))
                else:
                    self._update_grid(state, self.current_vars, self.current_cells)
                    # Colore o fundo de azul suave para indicar busca
                    for r in range(3):
                        for c in range(3):
                            self.current_cells[r][c].config(bg="#e6f2ff")
                    self.root.after(delay, lambda: step(index + 1))
            else:
                self.result_label.config(text="Mostrando caminho final!")
                self.animate_solution()

        step(0)

    def animate_solution(self):
        def step(index):
            if index < len(self.solution_path):
                self._update_grid(
                    self.solution_path[index], self.current_vars, self.current_cells
                )
                # Colore o fundo de azul para indicar solução
                for r in range(3):
                    for c in range(3):
                        if self.solution_path[index][r][c] != 0:
                            self.current_cells[r][c].config(bg="#a4c2f4")

                delay = self.speed_scale.get()
                self.root.after(delay, lambda: step(index + 1))
            else:
                self.is_animating = False
                self._set_cells_state("normal")
                self.result_label.config(
                    text=f"Solução concluída! {len(self.solution_path) - 1} movimentos."
                )

        step(0)

    def _set_cells_state(self, state):
        for r in range(3):
            for c in range(3):
                self.current_cells[r][c].config(state=state)
                self.goal_cells[r][c].config(state=state)


if __name__ == "__main__":
    root = tk.Tk()
    PuzzleInterface(root)
    root.mainloop()
