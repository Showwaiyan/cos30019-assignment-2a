from collections import deque
from search.base import GraphSearch
from search.models.result import SearchResult


class BFS(GraphSearch):
    """Breadth-First Search — expands all nodes one level at a time."""

    def __init__(self, graph: dict):
        pass

    def search(self, origin: int, destinations: list[int]) -> SearchResult:
        pass
