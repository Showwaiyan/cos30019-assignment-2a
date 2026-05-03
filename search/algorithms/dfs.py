from search.base import GraphSearch
from search.models.result import SearchResult


class DFS(GraphSearch):
    """Depth-First Search — selects one option, tries it, backtracks when exhausted."""

    def __init__(self, graph: dict):
        self._graph = graph

    def search(self, origin: int, destinations: list[int]) -> SearchResult:
        for dest in destinations:
            if dest not in self._graph:
                raise ValueError(f"Destination {dest} not found in graph")

        if origin not in self._graph:
            raise ValueError(f"Origin {origin} not found in graph")

        nodes_created = 0
        visited = set()
        stack = [(origin, [origin], 0.0)]

        while stack:
            node_id, path, cost = stack.pop()

            if node_id in visited:
                continue

            visited.add(node_id)
            nodes_created += 1

            if node_id in destinations:
                return SearchResult(
                    origin=origin,
                    destination=node_id,
                    path=path,
                    path_cost=cost,
                    nodes_created=nodes_created
                )

            node = self._graph.get(node_id)
            if node:
                for neighbor_id, edge_cost in sorted(node.neighbors, key=lambda x: x[0]):
                    if neighbor_id not in visited:
                        stack.append((neighbor_id, path + [neighbor_id], cost + edge_cost))

        return SearchResult(
            origin=origin,
            destination=None,
            path=None,
            path_cost=0.0,
            nodes_created=nodes_created
        )

