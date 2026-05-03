from collections import deque
from search.base import GraphSearch
from search.models.result import SearchResult


class BFS(GraphSearch):
    """Breadth-First Search — expands all nodes one level at a time."""

    def __init__(self, graph: dict):
        self._graph = graph

    def search(self, origin: int, destinations: list[int]) -> SearchResult:
        for dest in destinations:
            if dest not in self._graph:
                raise ValueError(f"Destination {dest} not found in graph")

        if origin not in self._graph:
            raise ValueError(f"Origin {origin} not found in graph")

        visited = set()
        queue = deque([(origin, [origin], 0.0)])
        nodes_created = 1

        while queue:
            node_id, path, cost = queue.popleft()

            if node_id in visited:
                continue
            visited.add(node_id)

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
                        queue.append((neighbor_id, path + [neighbor_id], cost + edge_cost))
                        nodes_created += 1

        return SearchResult(
            origin=origin,
            destination=None,
            path=None,
            path_cost=0.0,
            nodes_created=nodes_created
        )
