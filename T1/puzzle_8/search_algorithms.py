import heapq
from collections import deque


def _reconstruct_path(came_from, current):
    """Reconstrói o caminho percorrido a partir do dicionário de pais."""
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    return path[::-1]


def bfs(graph, start, goal):
    """BFS otimizada com dicionário de pais."""
    queue = deque([start])
    came_from = {start: None}
    visited_order = []

    while queue:
        current = queue.popleft()
        visited_order.append(current)

        if current == goal:
            return visited_order, _reconstruct_path(came_from, current)

        for neighbor, weight in graph.get_adjacencies(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)
    return visited_order, None


def dfs(graph, start, goal):
    """DFS otimizada com conjunto de visitados e dicionário de pais."""
    stack = [start]
    came_from = {start: None}
    visited_order = []
    visited = set()

    while stack:
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        if current == goal:
            return visited_order, _reconstruct_path(came_from, current)

        for neighbor, weight in reversed(graph.get_adjacencies(current)):
            if neighbor not in visited:
                came_from[neighbor] = current
                stack.append(neighbor)
    return visited_order, None


def ucs(graph, start, goal):
    """UCS otimizada com priority queue e g_costs."""
    pq = [(0, start)]
    came_from = {start: None}
    g_costs = {start: 0}
    visited_order = []
    explored = set()

    while pq:
        cost, current = heapq.heappop(pq)
        if current in explored:
            continue

        explored.add(current)
        visited_order.append(current)

        if current == goal:
            return visited_order, _reconstruct_path(came_from, current)

        for neighbor, weight in graph.get_adjacencies(current):
            new_cost = cost + weight
            if neighbor not in g_costs or new_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))
    return visited_order, None


def dls(graph, start, goal, limit):
    """DLS otimizada com limite de profundidade."""
    stack = [(start, 0, [start])]
    visited_order = []

    while stack:
        current, depth, path = stack.pop()
        visited_order.append(current)

        if current == goal:
            return visited_order, path

        if depth < limit:
            for neighbor, weight in reversed(graph.get_adjacencies(current)):
                if neighbor not in path:  # Evita ciclos no caminho atual
                    stack.append((neighbor, depth + 1, path + [neighbor]))
    return visited_order, None


def greedy_search(graph, start, goal, heuristic):
    """Busca Gulosa otimizada."""
    pq = [(heuristic(start, goal), start)]
    came_from = {start: None}
    visited_order = []
    visited = set()

    while pq:
        h, current = heapq.heappop(pq)
        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        if current == goal:
            return visited_order, _reconstruct_path(came_from, current)

        for neighbor, weight in graph.get_adjacencies(current):
            if neighbor not in visited:
                came_from[neighbor] = current
                heapq.heappush(pq, (heuristic(neighbor, goal), neighbor))
    return visited_order, None


def a_star(graph, start, goal, heuristic):
    """A* otimizado com f = g + h."""
    pq = [(heuristic(start, goal), start, 0)]
    came_from = {start: None}
    g_costs = {start: 0}
    visited_order = []
    explored = set()

    while pq:
        f, current, g = heapq.heappop(pq)
        if current in explored:
            continue

        explored.add(current)
        visited_order.append(current)

        if current == goal:
            return visited_order, _reconstruct_path(came_from, current)

        for neighbor, weight in graph.get_adjacencies(current):
            new_g = g + weight
            if neighbor not in g_costs or new_g < g_costs[neighbor]:
                g_costs[neighbor] = new_g
                came_from[neighbor] = current
                f_total = new_g + heuristic(neighbor, goal)
                heapq.heappush(pq, (f_total, neighbor, new_g))
    return visited_order, None


def ida_star(graph, start, goal, heuristic):
    """IDA* otimizado."""
    threshold = heuristic(start, goal)
    visited_order = []

    while True:
        path = [start]
        result, t = _ida_recursive(
            graph, path, 0, threshold, goal, visited_order, heuristic
        )
        if result == "FOUND":
            return visited_order, path
        if t == float("inf"):
            return visited_order, None
        threshold = t


def _ida_recursive(graph, path, g, threshold, goal, visited_order, heuristic):
    node = path[-1]
    f = g + heuristic(node, goal)
    visited_order.append(node)

    if f > threshold:
        return "NOT_FOUND", f
    if node == goal:
        return "FOUND", threshold

    min_t = float("inf")
    for neighbor, weight in graph.get_adjacencies(node):
        if neighbor not in path:
            path.append(neighbor)
            res, t = _ida_recursive(
                graph, path, g + weight, threshold, goal, visited_order, heuristic
            )
            if res == "FOUND":
                return "FOUND", threshold
            if t < min_t:
                min_t = t
            path.pop()
    return "NOT_FOUND", min_t
