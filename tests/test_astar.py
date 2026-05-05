import pytest
from search.algorithms.astar import AStar
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

class TestAStar:

    def test_finds_path(self):
        astar = AStar(map_0)
        result = astar.search(origin=1, destinations=[8])
        assert result.path is not None
        assert result.path[0] == 1
        assert result.path[-1] == 8
    
    def test_path_order(self):
        astar = AStar(map_0)
        result = astar.search(origin=1 , destinations=[8])
        
        # A* shortest path from 1 to 8: 1 -> 3 -> 6 -> 8
        assert result.path == [1, 3, 6, 8]
    
    def test_different_origin_destinations(self):
        astar = AStar(map_0)
        
        result = astar.search(origin=2, destinations=[8])
        assert result.path == [2, 5, 7, 1, 3, 6, 8]
        
        result = astar.search(origin=4, destinations=[8])
        assert result.path == [4, 2, 5, 7, 1, 3, 6, 8]
    
    def test_no_solution(self):
        astar = AStar(map_0)
        
        result = astar.search(origin=8, destinations=[1])
        assert result.path is None
        assert result.destination is None
        
    def test_no_solution_with_different_nodes(self):
        astar = AStar(map_0)
        
        result = astar.search(origin=8 ,destinations=[1, 2, 3])
        assert result.path is None
        
        result = astar.search(origin=8 , destinations=[4])
        assert result.path is None
        
        result = astar.search(origin=7 , destinations=[8])
        assert result.path == [7, 1, 3, 6, 8]
    
    def test_node_expansion_order(self):
        astar = AStar(map_0)
        
        result = astar.search(origin=1, destinations=[8])
        assert 1 in map_0
        assert result.path is not None
    
    def test_with_obstacles(self):
        restricted_map = map_0.copy()
        restricted_map[1] = Node(1, 0, 0, [(2, 1)])
        
        astar = AStar(restricted_map)
        result = astar.search(origin=1 , destinations=[8])
        assert result.path is None
    
    def test_invalid_bounds(self):
        astar = AStar(map_0)
        
        with pytest.raises(ValueError):
            astar.search(origin=1 , destinations=[99])
    
    def test_start_equals_goal(self):
        astar = AStar(map_0)
        result = astar.search(origin=1 , destinations=[1])
        
        assert result.path == [1]
    
    def test_path_cost(self):
        astar = AStar(map_0)
        result = astar.search(origin=1, destinations=[8])
        
        assert result.path_cost == 20

    def test_nodes_created(self):
        astar = AStar(map_0)
        result = astar.search(origin=1, destinations=[8])
        
        
        assert result.nodes_created == 8
