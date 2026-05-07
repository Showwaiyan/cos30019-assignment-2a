from collections import deque
from search.base import TreeSearch
from search.models.result import SearchResult


class DFS(TreeSearch):
    """Depth-First Search — selects one option, tries it, backtracks when exhausted."""

    def __init__(self, graph: dict):
        self._graph = graph

    def search(self, origin: int, destinations: list[int]) -> SearchResult:
        # Validate all destination nodes exist in graph
        for dest in destinations:
            if dest not in self._graph:
                raise ValueError(f"Destination {dest} not found in graph")

        # Validate origin node exists in graph
        if origin not in self._graph:
            raise ValueError(f"Origin {origin} not found in graph")

        # Initialize: visited set, queue with origin node, nodes_created counter
        visited = set()
        queue = deque([(origin, [origin], 0)])
        nodes_created = 1

        # Process nodes in stack order (LIFO - pop from front)
        while queue:
            # Pop node from front of queue
            node_id, path, cost = queue.pop()

            # Skip if already visited
            if node_id in visited:
                continue

            # Mark node as visited (expanded)
            visited.add(node_id)

            # Check if current node is a goal
            if node_id in destinations:
                return SearchResult(
                    origin=origin,
                    destination=node_id,
                    path=path,
                    path_cost=cost,
                    nodes_created=nodes_created
                ) 

            # Explore neighbors in ascending order by node ID
            node = self._graph.get(node_id)
            if node:
                # Get all nodes currently waiting in queue to avoid duplicates
                waiting_nodes = {n[0] for n in queue}
                for neighbor_id, edge_cost in sorted(node.neighbors, key=lambda x: x[0], reverse=True):
                    # Add unvisited neighbors to queue
                    if neighbor_id not in visited:
                        queue.append((neighbor_id, path + [neighbor_id], cost + edge_cost))
                        # count only nodes which are not in waiting_nodes to avoid double counting
                        nodes_created = nodes_created + 1 if neighbor_id not in waiting_nodes else nodes_created

        # No solution found - return result with None values
        return SearchResult(
            origin=origin,
            destination=None,
            path=None,
            path_cost=0,
            nodes_created=nodes_created
        )

