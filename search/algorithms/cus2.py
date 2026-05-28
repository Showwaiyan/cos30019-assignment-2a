import heapq
from search.base import GraphSearch
from search.models.result import SearchResult


class CUS2(GraphSearch):
    """Custom Search 2 — Dijkstra Algorithm."""

    def __init__(self, graph: dict):
        self._graph = graph

    def search(self, origin: int, destinations: list[int]) -> SearchResult:
        """
        Perform Dijkstra's algorithm to find the shortest path from origin to any destination.
        
        Dijkstra's is essentially A* with h(n) = 0.
        """
        # Validate origin and destinations exist in graph
        if origin not in self._graph:
            raise ValueError(f"Origin {origin} not found in graph")
        for d in destinations:
            if d not in self._graph:
                raise ValueError(f"Destination {d} not found in graph")

        # Early exit if start node is already a destination
        if origin in destinations:
            return SearchResult(
                origin = origin,
                destination = origin,
                path = [origin],
                path_cost = 0,
                nodes_created = 1
            )

        # Priority queue stores tuples: (cumulative_cost, node_id, counter)
        # Order: cost (lowest first), then node_id (ascending), then counter (insertion order)
        priorityQueue = [(0, origin, 0)]
        counter = 1
        
        # track min cost to reach each node
        visited_costs = {origin: 0}
        
        # track parent pointers to reconstruct the path later
        came_from = {origin: None}
        
        nodes_created = 1 
        visited = set()

        while priorityQueue:
            current_cost, current_node_id, _ = heapq.heappop(priorityQueue)
            
            # If we already found a shorter path to this node, skip
            if current_node_id in visited:
                continue
            visited.add(current_node_id)
            
            # Check if we reached one of our destinations
            if current_node_id in destinations:
                path = []
                node = current_node_id
                while node is not None:
                    path.append(node)
                    node = came_from[node]
                path.reverse()
                
                return SearchResult(
                    origin = origin,
                    destination = current_node_id,
                    path = path,
                    path_cost = current_cost,
                    nodes_created = nodes_created
                )

            # Explore neighbors
            current_node = self._graph[current_node_id]
            for neighbor_id, edge_cost in current_node.neighbors:
                new_cost = current_cost + edge_cost

                # If this path to neighbor is cheaper than any previously found path
                if neighbor_id not in visited_costs or new_cost < visited_costs[neighbor_id]:
                    visited_costs[neighbor_id] = new_cost
                    came_from[neighbor_id] = current_node_id
                    nodes_created += 1
                    heapq.heappush(priorityQueue, (new_cost, neighbor_id, counter))
                    counter += 1

        # If the queue empties without finding a destination
        return SearchResult(
            origin = origin,
            destination = destinations,
            path = None,
            path_cost = 0,
            nodes_created = nodes_created
        )
