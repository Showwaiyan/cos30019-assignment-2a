import heapq
import math
from search.base import GraphSearch
from search.models.result import SearchResult


class AStar(GraphSearch):
    """A* Search — uses both path cost g(n) and heuristic h(n) to evaluate nodes."""

    def __init__(self, graph: dict):
        self._graph = graph

    def search(self, origin: int, destinations: list[int]) -> SearchResult:
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
        # open_set stores (f_score, node_id) tuples; min-heap returns lowest f_score first
        open_set = []
        heapq.heappush(open_set, (0, origin))

        # came_from tracks parent node for path reconstruction
        came_from = {}

        # g_score tracks actual cost from start to each node
        g_score = {origin: 0}

        # nodes_created counts total expanded + frontier nodes
        nodes_created = 1

        # visited tracks already expanded nodes (closed set)
        visited = set()

        while open_set:
            # Pop node with lowest f_score from priority queue
            # heapq stores (f_score, node_id) tuples; heappop() returns the tuple
            # Use _ to discard f_score since we only need node_id for expansion
            _, current = heapq.heappop(open_set)

            # Skip if already visited (handles duplicate entries in queue)
            if current in visited:
                continue
            visited.add(current)

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

            # Expand current node's neighbors (generate successors)
            current_node = self._graph[current]
            for neighbor_id, edge_cost in current_node.neighbors:
                # Skip already visited neighbors
                if neighbor_id in visited:
                    continue

                # Calculate tentative g_score (actual cost from start via current node)
                tentative_g = g_score[current] + edge_cost

                # Update if we found a better path to this neighbor
                if neighbor_id not in g_score or tentative_g < g_score[neighbor_id]:
                    # Record parent for path reconstruction
                    came_from[neighbor_id] = current

                    # Update g_score with better path cost
                    g_score[neighbor_id] = tentative_g

                    # Calculate f_score = g(n) + h(n)
                    # h(n): Euclidean distance to nearest destination (admissible heuristic)
                    node = self._graph[neighbor_id]
                    goal = min(destinations, key=lambda d: math.sqrt((node.x - self._graph[d].x) ** 2 + (node.y - self._graph[d].y) ** 2))
                    f_score = tentative_g + math.sqrt((node.x - self._graph[goal].x) ** 2 + (node.y - self._graph[goal].y) ** 2)

                    # Add to open set; lower f_score = higher priority in queue
                    heapq.heappush(open_set, (f_score, neighbor_id))
                    nodes_created += 1

        # No path found to any destination (search exhausted)
        return SearchResult(
            origin=origin,
            destination=None,
            path=None,
            path_cost=0,
            nodes_created=nodes_created
        )
