import pytest
from search.algorithms.bfs import BFS
from search.models.graph import Node

map_0 = {
    1: Node(1, 0.0, 0.0, [(2, 1.0), (3, 1.0)]),
    2: Node(2, 2.0, 4.0, [(4, 1.0), (5, 1.0)]),
    3: Node(3, 4.0, 4.0, [(6, 1.0)]),
    4: Node(4, 1.0, 2.0, [(2, 1.0)]),
    5: Node(5, 3.0, 2.0, [(7, 1.0)]),
    6: Node(6, 5.0, 2.0, [(8, 1.0)]),
    7: Node(7, 2.0, 0.0, [(1, 1.0)]),
    8: Node(8, 6.0, 0.0, [])
}

class TestBFS:

    def test_finds_path(self):
        bfs = BFS(map_0)
        result = bfs.search(origin=1, destinations=[8])

        assert result is not None
        assert result.path is not None
        assert len(result.path) > 0
        assert result.path[0] == 1
        assert result.path[-1] == 8

    def test_path_order(self):
        bfs = BFS(map_0)
        result = bfs.search(origin=1, destinations=[8])

        # BFS shortest path from 1 to 8: 1 -> 3 -> 6 -> 8
        assert result.path == [1, 3, 6, 8]

    def test_different_origin_destination(self):
        bfs = BFS(map_0)

        result = bfs.search(origin=2, destinations=[8])
        assert result.path == [2, 5, 7, 1, 3, 6, 8]

        result = bfs.search(origin=4, destinations=[7])
        assert result.path == [4, 2, 5, 7]

    def test_no_solution(self):
        bfs = BFS(map_0)
        result = bfs.search(origin=8, destinations=[1])

        assert result.path is None
        assert result.destination is None

    def test_no_solution_different_nodes(self):
        bfs = BFS(map_0)

        result = bfs.search(origin=8, destinations=[1, 2, 3])
        assert result.path is None

        result = bfs.search(origin=8, destinations=[4])
        assert result.path is None

        result = bfs.search(origin=7, destinations=[8])
        assert result.path == [7, 1, 3, 6, 8]

    def test_node_expansion_order(self):
        bfs = BFS(map_0)
        result = bfs.search(origin=1, destinations=[8])

        assert 1 in map_0
        assert result.path is not None

    def test_with_obstacles(self):
        restricted_map = map_0.copy()
        restricted_map[1] = Node(1, 0, 0, [(2, 1)])

        bfs = BFS(restricted_map)
        result = bfs.search(origin=1, destinations=[8])

        assert result.path is None

    def test_invalid_bounds(self):
        bfs = BFS(map_0)

        with pytest.raises(ValueError):
            bfs.search(origin=1, destinations=[99])

    def test_start_equals_goal(self):
        bfs = BFS(map_0)
        result = bfs.search(origin=1, destinations=[1])

        assert result.path == [1]

    def test_path_cost(self):
        bfs = BFS(map_0)
        result = bfs.search(origin=1, destinations=[8])

        assert result.path_cost == 20

    def test_nodes_created(self):
        bfs = BFS(map_0)
        result = bfs.search(origin=1, destinations=[8])

        assert result.nodes_created == 8
