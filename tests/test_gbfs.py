import pytest
from search.algorithms.gbfs import GBFS
from search.models.graph import Node
from search.models.result import SearchResult

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

class TestGBFS:

    def test_finds_path(self):
        gbfs = GBFS(map_0)
        result = gbfs.search(origin=1, destinations=[8])
        assert result.path is not None
        assert result.path[0] == 1
        assert result.path[-1] == 8
    
    def test_path_order(self):
        gbfs = GBFS(map_0)
        result = gbfs.search(origin=1, destinations=[8])
        
        # GBFS path from 1 to 8 in map_0: 
        # h(2) = sqrt((6-2)^2 + (0-4)^2) = sqrt(32) ≈ 5.66
        # h(3) = sqrt((6-4)^2 + (0-4)^2) = sqrt(20) ≈ 4.47
        # Picks 3.
        # From 3, neighbor 6: h(6) = sqrt((6-5)^2 + (0-2)^2) = sqrt(5) ≈ 2.24
        # From 6, neighbor 8: h(8) = 0
        assert result.path == [1, 3, 6, 8]
    
    def test_no_solution(self):
        gbfs = GBFS(map_0)
        result = gbfs.search(origin=8, destinations=[1])
        assert result.path is None
        assert result.destination == [1]
        
    def test_start_equals_goal(self):
        gbfs = GBFS(map_0)
        result = gbfs.search(origin=1, destinations=[1])
        assert result.path == [1]
        assert result.path_cost == 0
    
    def test_invalid_nodes(self):
        gbfs = GBFS(map_0)
        with pytest.raises(ValueError):
            gbfs.search(origin=99, destinations=[1])
        with pytest.raises(ValueError):
            gbfs.search(origin=1, destinations=[99])

    def test_path_cost(self):
        gbfs = GBFS(map_0)
        result = gbfs.search(origin=1, destinations=[8])
        # 1->3 (10) + 3->6 (5) + 6->8 (5) = 20
        assert result.path_cost == 20

    def test_nodes_created(self):
        gbfs = GBFS(map_0)
        result = gbfs.search(origin=1, destinations=[8])
        # 1 added initially.
        # Neighbors of 1: 2, 3 added. (nodes_created = 3)
        # Pop 3. Neighbor 6 added. (nodes_created = 4)
        # Pop 6. Neighbor 8 added. (nodes_created = 5)
        # Pop 8. Done.
        assert result.nodes_created == 5
