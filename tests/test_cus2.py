import pytest
from search.algorithms.cus2 import CUS2
from search.models.graph import Node
from search.models.result import SearchResult

# Sample map for testing
map_0 = {
    1: Node(1, 0, 0, [(2, 10), (3, 10)]),
    2: Node(2, 2, 4, [(4, 5), (5, 5)]),
    3: Node(3, 4, 4, [(6, 5)]),
    4: Node(4, 1, 2, [(2, 5)]),
    5: Node(5, 3, 2, [(7, 5)]),
    6: Node(6, 5, 2, [(8, 5)]),
    7: Node(7, 2, 0, [(1, 5)]),
    8: Node(8, 6, 0, [])
}

class TestCUS2:

    def test_finds_path(self):
        cus2 = CUS2(map_0)
        result = cus2.search(origin=1, destinations=[8])
        assert result.path is not None
        assert result.path[0] == 1
        assert result.path[-1] == 8
    
    def test_path_order(self):
        cus2 = CUS2(map_0)
        result = cus2.search(origin=1, destinations=[8])
        # Dijkstra shortest path from 1 to 8: 1 -> 3 -> 6 -> 8
        assert result.path == [1, 3, 6, 8]
    
    def test_different_origin_destinations(self):
        cus2 = CUS2(map_0)
        
        result = cus2.search(origin=2, destinations=[8])
        assert result.path == [2, 5, 7, 1, 3, 6, 8]
        
    def test_no_solution(self):
        cus2 = CUS2(map_0)
        
        result = cus2.search(origin=8, destinations=[1])
        assert result.path is None
        assert result.destination is None
    
    def test_start_equals_goal(self):
        cus2 = CUS2(map_0)
        result = cus2.search(origin=1, destinations=[1])
        assert result.path == [1]
    
    def test_path_cost(self):
        cus2 = CUS2(map_0)
        result = cus2.search(origin=1, destinations=[8])
        assert result.path_cost == 20

    def test_invalid_bounds(self):
        cus2 = CUS2(map_0)
        with pytest.raises(ValueError):
            cus2.search(origin=1, destinations=[99])
