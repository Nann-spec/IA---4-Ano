from puzzle_8.puzzle_graph import PuzzleGraph
from puzzle_8.search_algorithms import a_star


def test_puzzle():
    # Estado inicial (embaralhado)
    # 1 2 3
    # 0 4 6
    # 7 5 8
    start_board = ((1, 2, 3), (0, 4, 6), (7, 5, 8))

    # Estado objetivo
    # 1 2 3
    # 4   5
    # 6 7 8
    goal_board = ((1, 2, 3), (4, 0, 5), (6, 7, 8))

    pg = PuzzleGraph(goal_board=goal_board)

    # Heuristica personalizada para o puzzle
    def puzzle_heuristic(state_board, goal):
        from puzzle_8.puzzle_logic import PuzzleState

        return PuzzleState(state_board, goal=goal).manhattan_distance()

    print("Testando A* no 8-Puzzle...")
    visited, path = a_star(pg, start_board, goal_board, heuristic=puzzle_heuristic)

    if path:
        print(f"Sucesso! Caminho encontrado com {len(path) - 1} movimentos.")
        print(f"Visitados: {len(visited)}")
    else:
        print("Falha ao encontrar caminho.")


if __name__ == "__main__":
    test_puzzle()
