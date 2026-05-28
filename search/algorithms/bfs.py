from collections import deque
from search.base import GraphSearch
from search.models.result import SearchResult


class BFS(GraphSearch):
    """Breadth-First Search — expands all nodes one level at a time."""

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

        visited = set()
        queue = deque([(origin, [origin], 0)])
        nodes_created = 1

        # Process nodes level by level (FIFO order)
        while queue:
            # Dequeue node from front of queue
            node_id, path, cost = queue.popleft()

            # Skip if already visited (handles duplicates in queue)
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
                waiting_nodes = {item[0] for item in queue}
                for neighbor_id, edge_cost in sorted(node.neighbors, key=lambda x: x[0]):
                    # Add unvisited neighbors that are not already in queue
                    if neighbor_id not in visited and neighbor_id not in waiting_nodes:
                        queue.append((neighbor_id, path + [neighbor_id], cost + edge_cost))
                        nodes_created += 1

        # No solution found - return result with None values
        return SearchResult(
            origin=origin,
            destination=destinations,
            path=None,
            path_cost=0,
            nodes_created=nodes_created
        )
