import heapq
import math
from collections import deque

from utils.constants import ROMANIA_LAT_LON


def get_romania_heuristic(city_a, city_b):
    """Calcula a distância euclidiana padrao para a Romenia."""
    a, b = str(city_a).upper(), str(city_b).upper()
    if a in ROMANIA_LAT_LON and b in ROMANIA_LAT_LON:
        pos_a, pos_b = ROMANIA_LAT_LON[a], ROMANIA_LAT_LON[b]
        return math.sqrt(
            (pos_b["lat"] - pos_a["lat"]) ** 2 + (pos_b["lon"] - pos_a["lon"]) ** 2
        )
    return float("inf")


def bfs(graph, start, goal):
    vertices = graph.get_vertices()
    if start not in vertices or goal not in vertices:
        return [], None

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

        adjacencies = graph.get_adjacencies()
        for neighbor, weight in adjacencies.get(current, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return visited_order, None


def dfs(graph, start, goal):
    vertices = graph.get_vertices()
    if start not in vertices or goal not in vertices:
        return [], None

    stack = [(start, [start])]
    visited = set()
    visited_order = []

    while stack:
        current, path = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)

        if current == goal:
            return visited_order, path

        adjacencies = graph.get_adjacencies()
        for neighbor, weight in reversed(adjacencies.get(current, [])):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    return visited_order, None


def ucs(graph, start, goal):
    vertices = graph.get_vertices()
    if start not in vertices or goal not in vertices:
        return [], None

    priority_queue = [(0, start, [start])]
    costs = {v: float("inf") for v in vertices}
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

        adjacencies = graph.get_adjacencies()
        for neighbor, weight in adjacencies.get(current, []):
            new_cost = cost + weight
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))
    return visited_order, None


def dls(graph, start, goal, limit):
    vertices = graph.get_vertices()
    if start not in vertices or goal not in vertices:
        return [], None

    stack = [(start, [start], 0)]
    visited_order = []
    min_depths = {v: float("inf") for v in vertices}

    while stack:
        current, path, depth = stack.pop()
        if depth >= min_depths[current]:
            continue
        min_depths[current] = depth
        visited_order.append(current)

        if current == goal:
            return visited_order, path

        if depth < limit:
            adjacencies = graph.get_adjacencies()
            for neighbor, weight in reversed(adjacencies.get(current, [])):
                if depth + 1 < min_depths[neighbor]:
                    stack.append((neighbor, path + [neighbor], depth + 1))
    return visited_order, None


def greedy_search(graph, start, goal):
    vertices = graph.get_vertices()
    if start not in vertices or goal not in vertices:
        return [], None

    priority_queue = [(get_romania_heuristic(start, goal), start, [start])]
    visited_order, visited = [], set()

    while priority_queue:
        h_val, current, path = heapq.heappop(priority_queue)
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)

        if current == goal:
            return visited_order, path

        adjacencies = graph.get_adjacencies()
        for neighbor, weight in adjacencies.get(current, []):
            if neighbor not in visited:
                heapq.heappush(
                    priority_queue,
                    (
                        get_romania_heuristic(neighbor, goal),
                        neighbor,
                        path + [neighbor],
                    ),
                )
    return visited_order, None


def a_star(graph, start, goal):
    vertices = graph.get_vertices()
    if start not in vertices or goal not in vertices:
        return [], None

    priority_queue = [(get_romania_heuristic(start, goal), start, [start], 0)]
    g_costs = {v: float("inf") for v in vertices}
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

        adjacencies = graph.get_adjacencies()
        for neighbor, weight in adjacencies.get(current, []):
            new_g = g_score + weight
            if new_g < g_costs[neighbor]:
                g_costs[neighbor] = new_g
                f_total = new_g + get_romania_heuristic(neighbor, goal)
                heapq.heappush(
                    priority_queue, (f_total, neighbor, path + [neighbor], new_g)
                )
    return visited_order, None


def ida_star(graph, start, goal):
    vertices = graph.get_vertices()
    if start not in vertices or goal not in vertices:
        return [], None

    threshold = get_romania_heuristic(start, goal)
    visited_order = []
    path = [start]

    while True:
        result, t = _ida_recursive(graph, path, 0, threshold, goal, visited_order)
        if result == "FOUND":
            return visited_order, path
        if t == float("inf"):
            return visited_order, None
        threshold = t


def _ida_recursive(graph, path, g, threshold, goal, visited_order):
    node = path[-1]
    f = g + get_romania_heuristic(node, goal)
    visited_order.append(node)

    if f > threshold:
        return "NOT_FOUND", f
    if node == goal:
        return "FOUND", threshold

    min_t = float("inf")
    adjacencies = graph.get_adjacencies()
    for neighbor, weight in adjacencies.get(node, []):
        if neighbor not in path:
            path.append(neighbor)
            res, t = _ida_recursive(
                graph, path, g + weight, threshold, goal, visited_order
            )
            if res == "FOUND":
                return "FOUND", threshold
            if t < min_t:
                min_t = t
            path.pop()
    return "NOT_FOUND", min_t
