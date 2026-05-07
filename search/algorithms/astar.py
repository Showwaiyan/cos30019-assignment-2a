from search.base import TreeSearch
from search.models.result import SearchResult


class AStar(TreeSearch):
    """A* Search — uses both path cost g(n) and heuristic h(n) to evaluate nodes."""

    def __init__(self, graph: dict):
        pass

    def search(self, origin: int, destinations: list[int]) -> SearchResult:
        pass
