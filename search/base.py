from abc import ABC, abstractmethod
from search.models.result import SearchResult


class GraphSearch(ABC):
    """
    Abstract base class for all tree-based search algorithms.
    Each algorithm subclass must implement the search() method.
    """

    def __init__(self, graph: dict):
        """
        :param graph: dict of node_id -> Node, representing the map
        """
        pass

    @abstractmethod
    def search(self, origin: int, destinations: list[int]) -> SearchResult:
        """
        Perform the search from origin to one of the destination nodes.

        :param origin: starting node ID
        :param destinations: list of goal node IDs
        :return: SearchResult
        """
        pass
