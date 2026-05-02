from search.base import GraphSearch
from search.models.graph import Node


class DFS(GraphSearch):
    """Depth-First Search — selects one option, tries it, backtracks when exhausted."""

    def __init__(self, graph: dict):
        self._graph = graph

    def search(self, origin: int, destinations: list[int]) -> list[Node]:
        for dest in destinations:
            if dest not in self._graph:
                raise ValueError(f"Destination {dest} not found in graph")
        
        if origin not in self._graph:
            raise ValueError(f"Origin {origin} not found in graph")

        visited = set()
        stack = [(origin, [origin])]

        while stack:
            node_id, path = stack.pop()

            if node_id in visited:
                continue
            visited.add(node_id)

            if node_id in destinations:
                return [self._graph[nid] for nid in path]

            node = self._graph.get(node_id)
            if node:
                for neighbor_id, _ in sorted(node.neighbors, key=lambda x: x[0]):
                    if neighbor_id not in visited:
                        stack.append((neighbor_id, path + [neighbor_id]))

        return []