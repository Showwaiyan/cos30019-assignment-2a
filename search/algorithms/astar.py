import heapq
import math
from search.base import GraphSearch
from search.models.result import SearchResult


class AStar(GraphSearch):
    """A* Search — uses both path cost g(n) and heuristic h(n) to evaluate nodes."""

    def __init__(self, graph: dict):
        self._graph = graph

    def search(self, origin: int, destinations: list[int]) -> SearchResult:
        if origin not in self._graph:
            raise ValueError(f"Origin {origin} not found in graph")
        for d in destinations:
            if d not in self._graph:
                raise ValueError(f"Destination {d} not found in graph")

        if origin in destinations:
            return SearchResult(
                origin=origin,
                destination=origin,
                path=[origin],
                path_cost=0,
                nodes_created=1
            )

        open_set = []
        heapq.heappush(open_set, (0, origin))
        came_from = {}
        g_score = {origin: 0}
        nodes_created = 1
        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)

            if current in visited:
                continue
            visited.add(current)

            if current in destinations:
                path = []
                node = current
                while node in came_from:
                    path.append(node)
                    node = came_from[node]
                path.append(origin)
                path.reverse()
                return SearchResult(
                    origin=origin,
                    destination=current,
                    path=path,
                    path_cost=g_score[current],
                    nodes_created=nodes_created
                )

            current_node = self._graph[current]
            for neighbor_id, edge_cost in current_node.neighbors:
                if neighbor_id in visited:
                    continue

                tentative_g = g_score[current] + edge_cost

                if neighbor_id not in g_score or tentative_g < g_score[neighbor_id]:
                    came_from[neighbor_id] = current
                    g_score[neighbor_id] = tentative_g
                    node = self._graph[neighbor_id]
                    goal = min(destinations, key=lambda d: math.sqrt((node.x - self._graph[d].x) ** 2 + (node.y - self._graph[d].y) ** 2))
                    f_score = tentative_g + math.sqrt((node.x - self._graph[goal].x) ** 2 + (node.y - self._graph[goal].y) ** 2)
                    heapq.heappush(open_set, (f_score, neighbor_id))
                    nodes_created += 1

        return SearchResult(
            origin=origin,
            destination=None,
            path=None,
            path_cost=0,
            nodes_created=nodes_created
        )
