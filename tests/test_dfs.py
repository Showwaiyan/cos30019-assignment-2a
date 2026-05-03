import pytest
from search.algorithms.dfs import DFS
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

class TestDFS:

    def test_finds_path(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[8])

        assert isinstance(result, SearchResult)
        assert result.path is not None
        assert result.origin == 1
        assert result.destination == 8
        assert result.path_cost == 20.0
        assert result.nodes_created == 4
        assert result is not None
        assert result.path is not None
        assert len(result.path) > 0
        assert result.path[0] == 1
        assert result.path[-1] == 8

    def test_path_order(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[8])

        assert result.path == [1, 3, 6, 8]

    def test_different_origin_destination(self):
        dfs = DFS(map_0)

        result = dfs.search(origin=2, destinations=[8])
        assert result.path == [2, 5, 7, 1, 3, 6, 8]
        assert result.path_cost == 35.0

        result = dfs.search(origin=4, destinations=[7])
        assert result.path == [4, 2, 5, 7]
        assert result.path_cost == 15.0

        result = dfs.search(origin=4, destinations=[7])
        assert result.path == [4, 2, 5, 7]

    def test_no_solution(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=8, destinations=[1])

        assert result.path is None
        assert result.destination is None
        assert result.path_cost == 0.0

    def test_no_solution_different_nodes(self):
        dfs = DFS(map_0)

        result = dfs.search(origin=8, destinations=[1, 2, 3])
        assert result.path is None
        assert result.path_cost == 0.0

        result = dfs.search(origin=8, destinations=[4])
        assert result.path is None
        assert result.path_cost == 0.0

        result = dfs.search(origin=7, destinations=[8])
        assert result.path == [7, 1, 3, 6, 8]

    def test_node_expansion_order(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[8])

        # nodes_created should be 4 for the path [1, 3, 6, 8]
        assert result.nodes_created == 4
        assert 1 in map_0
        assert result.path is not None

    def test_with_obstacles(self):
        restricted_map = map_0.copy()
        restricted_map[1] = Node(1, 0, 0, [(2, 10)])

        dfs = DFS(restricted_map)
        result = dfs.search(origin=1, destinations=[8])

        assert result.path is None

    def test_invalid_bounds(self):
        dfs = DFS(map_0)

        with pytest.raises(ValueError):
            dfs.search(origin=1, destinations=[99])

    def test_start_equals_goal(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[1])

        assert result.path == [1]
        assert result.path_cost == 0.0
        assert result.nodes_created == 1


    def test_path_cost(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[8])

        assert result.path_cost == 20

    def test_nodes_created(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[8])

        assert result.nodes_created == 4
