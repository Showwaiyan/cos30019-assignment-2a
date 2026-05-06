from search.base import GraphSearch
from search.models.result import SearchResult


class AStar(GraphSearch):
    """A* Search — uses both path cost g(n) and heuristic h(n) to evaluate nodes."""

    def __init__(self, graph: dict):
        pass

    def search(self, origin: int, destinations: list[int]) -> SearchResult:
        pass
