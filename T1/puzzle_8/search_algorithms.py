import heapq
from collections import defaultdict, deque


def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set()
    visited_order = []

    while queue:
        current, path = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)

        if current == goal:
            return visited_order, path

        for neighbor, weight in graph.get_adjacencies(current):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return visited_order, None


def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    visited_order = []

    # x = 0

    while stack:
        # x = x + 1
        # print(f"Visitando nó {x} vezes")
        current, path = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)

        if current == goal:
            return visited_order, path

        for neighbor, weight in reversed(graph.get_adjacencies(current)):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    return visited_order, None


def ucs(graph, start, goal):
    priority_queue = [(0, start, [start])]
    costs = defaultdict(lambda: float("inf"))
    costs[start] = 0
    visited_order, explored = [], set()

    while priority_queue:
        cost, current, path = heapq.heappop(priority_queue)
        if current in explored:
            continue
        explored.add(current)
        visited_order.append(current)

        if current == goal:
            return visited_order, path

        for neighbor, weight in graph.get_adjacencies(current):
            new_cost = cost + weight
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))
    return visited_order, None


def dls(graph, start, goal, limit):
    stack = [(start, [start], 0)]
    visited_order = []
    min_depths = defaultdict(lambda: float("inf"))

    while stack:
        current, path, depth = stack.pop()
        if depth >= min_depths[current]:
            continue
        min_depths[current] = depth
        visited_order.append(current)

        if current == goal:
            return visited_order, path

        if depth < limit:
            for neighbor, weight in reversed(graph.get_adjacencies(current)):
                if depth + 1 < min_depths[neighbor]:
                    stack.append((neighbor, path + [neighbor], depth + 1))
    return visited_order, None


def greedy_search(graph, start, goal, heuristic):
    priority_queue = [(heuristic(start, goal), start, [start])]
    visited_order, visited = [], set()

    while priority_queue:
        h_val, current, path = heapq.heappop(priority_queue)
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)

        if current == goal:
            return visited_order, path

        for neighbor, weight in graph.get_adjacencies(current):
            if neighbor not in visited:
                heapq.heappush(
                    priority_queue,
                    (heuristic(neighbor, goal), neighbor, path + [neighbor]),
                )
    return visited_order, None


def a_star(graph, start, goal, heuristic):
    priority_queue = [(heuristic(start, goal), start, [start], 0)]
    g_costs = defaultdict(lambda: float("inf"))
    g_costs[start] = 0
    visited_order, explored = [], set()

    while priority_queue:
        f_score, current, path, g_score = heapq.heappop(priority_queue)
        if current in explored:
            continue
        explored.add(current)
        visited_order.append(current)

        if current == goal:
            return visited_order, path

        for neighbor, weight in graph.get_adjacencies(current):
            new_g = g_score + weight
            if new_g < g_costs[neighbor]:
                g_costs[neighbor] = new_g
                f_total = new_g + heuristic(neighbor, goal)
                heapq.heappush(
                    priority_queue, (f_total, neighbor, path + [neighbor], new_g)
                )
    return visited_order, None


def ida_star(graph, start, goal, heuristic):
    threshold = heuristic(start, goal)
    visited_order = []
    path = [start]

    while True:
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
