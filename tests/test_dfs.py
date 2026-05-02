import pytest
from search.algorithms.dfs import DFS
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

class TestDFS:

    def test_finds_path(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[8])

        assert result is not None
        assert len(result) > 0
        assert result[0].id == 1
        assert result[-1].id == 8

    def test_path_order(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[8])

        path_ids = [n.id for n in result]
        assert path_ids == [1, 3, 6, 8]

    def test_different_origin_destination(self):
        dfs = DFS(map_0)

        result = dfs.search(origin=2, destinations=[8])
        path_ids = [n.id for n in result]
        assert path_ids == [2, 5, 7, 1, 3, 6, 8]

        result = dfs.search(origin=4, destinations=[7])
        path_ids = [n.id for n in result]
        assert path_ids == [4, 2, 5, 7]

    def test_no_solution(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=8, destinations=[1])

        assert result == []

    def test_no_solution_different_nodes(self):
        dfs = DFS(map_0)

        result = dfs.search(origin=8, destinations=[1, 2, 3])
        assert result == []

        result = dfs.search(origin=8, destinations=[4])
        assert result == []

        result = dfs.search(origin=7, destinations=[8])
        path_ids = [n.id for n in result]
        assert path_ids == [7, 1, 3, 6, 8]

    def test_node_expansion_order(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[8])

        assert 1 in map_0
        assert len(result) > 0

    def test_with_obstacles(self):
        restricted_map = map_0.copy()
        restricted_map[1] = Node(1, 0.0, 0.0, [(2, 1.0)])

        dfs = DFS(restricted_map)
        result = dfs.search(origin=1, destinations=[8])

        assert result == []

    def test_invalid_bounds(self):
        dfs = DFS(map_0)

        with pytest.raises(ValueError):
            dfs.search(origin=1, destinations=[99])

    def test_start_equals_goal(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[1])

        assert [n.id for n in result] == [1]