from puzzle_logic import PuzzleState


class PuzzleGraph:
    def __init__(self, goal_board=None):
        self.goal_board = (
            goal_board if goal_board else ((1, 2, 3), (4, 0, 5), (6, 7, 8))
        )

    def get_adjacencies(self, state_board):
        """
        Gera vizinhos on-the-fly para o estado atual (board).
        Retorna lista de (novo_board, peso=1).
        """
        state = PuzzleState(state_board, goal=self.goal_board)
        neighbors = state.get_neighbors()
        # Cada movimento tem custo 1
        return [(neighbor, 1) for neighbor in neighbors]

    def get_vertices(self):
        """
        Para grafos dinamicos, nao podemos retornar todos os vertices antecipadamente.
        Retornamos uma lista vazia ou algo que nao quebre a validacao inicial.
        """
        return []

    def get_heuristic(self, state_board, goal_board):
        state = PuzzleState(state_board, goal=goal_board)
        return state.manhattan_distance()
