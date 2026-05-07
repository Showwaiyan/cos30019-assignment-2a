import heapq
from search.base import GraphSearch
from search.models.result import SearchResult


class GBFS(GraphSearch):
    """Greedy Best-First Search — uses only the heuristic cost to goal."""

    def __init__(self, graph: dict):
        pass

    def search(self, origin: int, destinations: list[int]) -> SearchResult:
        pass
