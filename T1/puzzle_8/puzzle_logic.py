class PuzzleState:
    def __init__(self, board, goal=None):
        self.board = board  # Tupla de tuplas ((1,2,3), (4,5,6), (7,8,0))
        self.goal = goal if goal else ((1, 2, 3), (4, 0, 5), (6, 7, 8))
        self.blank_pos = self._find_blank()

    def _find_blank(self):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def get_neighbors(self):
        neighbors = []
        if self.blank_pos is None:
            return neighbors

        r, c = self.blank_pos
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Cima, Baixo, Esquerda, Direita

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                # Cria novo tabuleiro trocando o zero com o vizinho
                new_board = [list(row) for row in self.board]
                new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
                # Converte de volta para tupla de tuplas
                neighbors.append(tuple(tuple(row) for row in new_board))
        return neighbors

    def manhattan_distance(self):
        distance = 0
        goal_map = {
            val: (r, c) for r, row in enumerate(self.goal) for c, val in enumerate(row)
        }

        for r in range(3):
            for c in range(3):
                val = self.board[r][c]
                if val != 0:
                    target_r, target_c = goal_map[val]
                    distance += abs(r - target_r) + abs(c - target_c)
        return distance

    def is_solvable(self):
        # Achata o tabuleiro em uma lista
        flat_board = [val for row in self.board for val in row if val != 0]
        inversions = 0
        for i in range(len(flat_board)):
            for j in range(i + 1, len(flat_board)):
                if flat_board[i] > flat_board[j]:
                    inversions += 1

        # Para o 8-puzzle (grade 3x3), o puzzle e soluvel se
        # o numero de inversoes tiver a mesma paridade que o estado objetivo.
        # Nosso objetivo ((1,2,3), (4,5,6), (7,8,0)) tem 0 inversoes (par).
        return inversions % 2 == 0

    def __eq__(self, other):
        if isinstance(other, PuzzleState):
            return self.board == other.board
        return self.board == other

    def __hash__(self):
        return hash(self.board)

    def __repr__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.board])
