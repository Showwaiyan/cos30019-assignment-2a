import heapq
from search.base import GraphSearch
from search.models.result import SearchResult


class AStar(GraphSearch):
    """A* Search — uses both path cost g(n) and heuristic h(n) to evaluate nodes."""

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

        # Heuristic function: Euclidean distance to the nearest destination
        #h(n) = sqrt((x1-x2)² + (y1-y2)²)
        def h(node_id):
            node = self._graph[node_id]
            return min(((node.x - self._graph[d].x)**2 + (node.y - self._graph[d].y)**2)**0.5 
                       for d in destinations)

        visited = set()
        queue = [(h(origin), origin, [origin], 0)]
        nodes_created = 1

        # Process nodes based on lowest f_score (g + h)
        while queue:
            # Dequeue node with lowest f_score from priority queue
            f, node_id, path, cost = heapq.heappop(queue)

            # Skip if already visited (handles duplicates in priority queue)
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
                waiting_nodes = {item[1] for item in queue}
                for neighbor_id, edge_cost in sorted(node.neighbors, key=lambda x: x[0]):
                    # Add unvisited neighbors that are not already in queue
                    if neighbor_id not in visited and neighbor_id not in waiting_nodes:
                        new_cost = cost + edge_cost
                        heapq.heappush(queue, (new_cost + h(neighbor_id), neighbor_id, path + [neighbor_id], new_cost))
                        nodes_created += 1

        # No solution found - return result with None values
        return SearchResult(
            origin=origin,
            destination=None,
            path=None,
            path_cost=0,
            nodes_created=nodes_created
        )
