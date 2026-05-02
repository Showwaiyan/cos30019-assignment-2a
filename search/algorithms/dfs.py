from search.base import GraphSearch


class DFS(GraphSearch):
    """Depth-First Search — selects one option, tries it, backtracks when exhausted."""

    def __init__(self, graph: dict):
        pass

    def search(self, origin: int, destinations: list[int]) -> dict:
        pass
