import pytest
from search.registry import get_algorithm
from search.base import GraphSearch
from search.algorithms.bfs import BFS
from search.algorithms.dfs import DFS
from search.algorithms.astar import AStar
from search.algorithms.gbfs import GBFS
from search.algorithms.cus1 import CUS1
from search.algorithms.cus2 import CUS2


class TestRegistry:

    def test_returns_correct_class(self):
        assert get_algorithm("BFS") == BFS
        assert get_algorithm("DFS") == DFS
        assert get_algorithm("AS") == AStar
        assert get_algorithm("GBFS") == GBFS
        assert get_algorithm("CUS1") == CUS1
        assert get_algorithm("CUS2") == CUS2

    def test_case_insensitive(self):
        assert get_algorithm("bfs") == BFS
        assert get_algorithm("Bfs") == BFS
        assert get_algorithm("as") == AStar
        assert get_algorithm("As") == AStar

    def test_invalid_algorithm_raises(self):
        with pytest.raises(ValueError, match="Algorithm 'INVALID' is not recognized."):
            get_algorithm("INVALID")

    def test_returned_class_is_subclass_of_graphsearch(self):
        algo_class = get_algorithm("BFS")
        assert issubclass(algo_class, GraphSearch)
        
        algo_class = get_algorithm("AS")
        assert issubclass(algo_class, GraphSearch)
