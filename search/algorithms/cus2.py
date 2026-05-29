import math
from search.base import GraphSearch
from search.models.result import SearchResult


class CUS2(GraphSearch):
    """Custom Search 2 — Iterative Deepening A* (IDA*)."""

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

        def h(node_id: int) -> float:
            node = self._graph[node_id]
            return min(
                math.sqrt((node.x - self._graph[d].x) ** 2 + (node.y - self._graph[d].y) ** 2)
                for d in destinations
            )

        threshold = h(origin)
        nodes_created = 1
        seen_nodes = {origin}
        next_threshold = [float("inf")]

        def dfs(node_id: int, g: float, path: list[int], visited: set[int]):
            nonlocal nodes_created

            f = g + h(node_id)

            if f > threshold:
                if f < next_threshold[0]:
                    next_threshold[0] = f
                return None

            if node_id in destinations:
                return (list(path), g)

            node = self._graph[node_id]
            for neighbor_id, edge_cost in sorted(
                node.neighbors, key=lambda x: (g + x[1] + h(x[0]), x[0])
            ):
                if neighbor_id in visited:
                    continue

                if neighbor_id not in seen_nodes:
                    seen_nodes.add(neighbor_id)
                    nodes_created += 1
                visited.add(neighbor_id)
                path.append(neighbor_id)

                result = dfs(neighbor_id, g + edge_cost, path, visited)
                if result is not None:
                    return result

                path.pop()
                visited.remove(neighbor_id)

            return None

        while True:
            result = dfs(origin, 0, [origin], {origin})
            if result is not None:
                path, cost = result
                return SearchResult(
                    origin=origin,
                    destination=path[-1],
                    path=path,
                    path_cost=cost,
                    nodes_created=nodes_created
                )

            if next_threshold[0] == float("inf"):
                return SearchResult(
                    origin=origin,
                    destination=destinations,
                    path=None,
                    path_cost=0,
                    nodes_created=nodes_created
                )

            threshold = next_threshold[0]
            next_threshold[0] = float("inf")
