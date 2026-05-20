import heapq
import math
from search.base import GraphSearch
from search.models.result import SearchResult


class GBFS(GraphSearch):
    """Greedy Best-First Search — uses only the heuristic cost to goal."""

    def __init__(self, graph: dict):
        self._graph = graph

    def search(self, origin: int, destinations: list[int]) -> SearchResult:
        """
        Perform Greedy Best-First Search from origin to nearest destination.
        
        Priority Queue uses h(n) = Euclidean distance to nearest destination.
        Tie-breaking: smaller node ID first.
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
                origin=origin,
                destination=origin,
                path=[origin],
                path_cost=0,
                nodes_created=1
            )

        # Initialize priority queue (open set) with origin node
        # open_set stores (h_score, node_id) tuples
        # Order: h_score (lowest first), then node_id (ascending) as tiebreaker
        open_set = []
        
        # Helper to calculate h(n)
        def get_heuristic(node_id):
            node = self._graph[node_id]
            # Euclidean distance to the nearest destination
            return min(math.sqrt((node.x - self._graph[d].x) ** 2 + (node.y - self._graph[d].y) ** 2) for d in destinations)

        h_start = get_heuristic(origin)
        heapq.heappush(open_set, (h_start, origin))

        # came_from tracks parent node for path reconstruction
        came_from = {}

        # g_score tracks actual cost from start to each node (needed for SearchResult)
        g_score = {origin: 0}

        # nodes_created counts total expanded + frontier nodes
        nodes_created = 1

        # visited tracks already expanded nodes (closed set)
        visited = set()

        while open_set:
            # Pop node with lowest h_score from priority queue
            _, current = heapq.heappop(open_set)

            # Skip if already visited (handles duplicate entries if any)
            if current in visited:
                continue
            
            # Check if current node is a destination (goal test)
            if current in destinations:
                # Reconstruct path by backtracking from goal to start
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
            
            visited.add(current)

            # Expand current node's neighbors
            current_node = self._graph[current]
            for neighbor_id, edge_cost in current_node.neighbors:
                # Skip already visited neighbors
                if neighbor_id in visited:
                    continue

                # GBFS typically doesn't reconsider nodes already in the frontier
                # because h(n) is fixed. We only add if it's the first time we see it.
                if neighbor_id not in came_from:
                    came_from[neighbor_id] = current
                    g_score[neighbor_id] = g_score[current] + edge_cost

                    h_val = get_heuristic(neighbor_id)
                    heapq.heappush(open_set, (h_val, neighbor_id))
                    nodes_created += 1

        # No path found
        return SearchResult(
            origin=origin,
            destination=None,
            path=None,
            path_cost=0,
            nodes_created=nodes_created
        )
