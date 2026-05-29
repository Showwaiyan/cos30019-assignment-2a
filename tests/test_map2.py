import pytest
from search.algorithms.dfs import DFS
from search.algorithms.bfs import BFS
from search.algorithms.astar import AStar
from search.algorithms.gbfs import GBFS
from search.algorithms.cus1 import CUS1
from search.services.parser import load_map


class TestMap2:
    """Integration tests for Map2 using DFS, BFS, and AStar."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load Map2 before each test."""
        origin, destinations, self.graph = load_map("maps/Map2.txt")
        self.origin = origin
        self.destinations = destinations

    def test_dfs(self):
        """Test DFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [11], "expected_path": [1, 2, 4, 6, 7, 8, 9, 10, 11], "expected_cost": 52, "expected_nodes": 11},
            {"origin": 1, "destinations": [5], "expected_path": [1, 2, 4, 6, 7, 5], "expected_cost": 28, "expected_nodes": 10},
            {"origin": 3, "destinations": [11], "expected_path": [3, 1, 2, 4, 6, 7, 8, 9, 10, 11], "expected_cost": 58, "expected_nodes": 11},
            {"origin": 6, "destinations": [9], "expected_path": [6, 1, 2, 4, 8, 7, 9], "expected_cost": 40, "expected_nodes": 10},
            {"origin": 5, "destinations": [1], "expected_path": [5, 3, 1], "expected_cost": 11, "expected_nodes": 4},
        ]

        dfs = DFS(self.graph)
        for tc in test_cases:
            result = dfs.search(origin=tc["origin"], destinations=tc["destinations"])

            assert result is not None
            assert result.origin == tc["origin"]
            if tc["expected_path"] is None:
                assert result.path is None
            else:
                assert result.path == tc["expected_path"]
            assert result.path_cost == tc["expected_cost"]
            assert result.nodes_created == tc["expected_nodes"]
            if tc["expected_path"]:
                assert result.destination == tc["expected_path"][-1]

    def test_bfs(self):
        """Test BFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [11], "expected_path": [1, 2, 4, 10, 11], "expected_cost": 35, "expected_nodes": 11},
            {"origin": 1, "destinations": [5], "expected_path": [1, 3, 5], "expected_cost": 11, "expected_nodes": 9},
            {"origin": 3, "destinations": [11], "expected_path": [3, 5, 7, 9, 11], "expected_cost": 22, "expected_nodes": 11},
            {"origin": 6, "destinations": [9], "expected_path": [6, 7, 9], "expected_cost": 14, "expected_nodes": 11},
            {"origin": 5, "destinations": [1], "expected_path": [5, 3, 1], "expected_cost": 11, "expected_nodes": 6},
        ]

        bfs = BFS(self.graph)
        for tc in test_cases:
            result = bfs.search(origin=tc["origin"], destinations=tc["destinations"])

            assert result is not None
            assert result.origin == tc["origin"]
            if tc["expected_path"] is None:
                assert result.path is None
            else:
                assert result.path == tc["expected_path"]
            assert result.path_cost == tc["expected_cost"]
            assert result.nodes_created == tc["expected_nodes"]
            if tc["expected_path"]:
                assert result.destination == tc["expected_path"][-1]

    def test_astar(self):
        """Test A* with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [11], "expected_path": [1,3,5,7,9,11], "expected_cost": 28, "expected_nodes": 13},
            {"origin": 3, "destinations": [11], "expected_path": [3,5,7,9,11], "expected_cost": 22, "expected_nodes": 8},
            {"origin": 6, "destinations": [9], "expected_path": [6,7,9], "expected_cost": 14, "expected_nodes": 7},
            {"origin": 5, "destinations": [11], "expected_path": [5,7,9,11], "expected_cost": 17, "expected_nodes": 7},
            {"origin": 2, "destinations": [9, 11], "expected_path": [2,4,8,9], "expected_cost": 21, "expected_nodes": 10},
        ]

        astar = AStar(self.graph)
        for tc in test_cases:
            result = astar.search(origin=tc["origin"], destinations=tc["destinations"])
            assert result.destination == tc["expected_path"][-1]


    def test_gbfs(self):
        """Test GBFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [11], "expected_path": [1, 6, 7, 9, 11], "expected_cost": 29, "expected_nodes": 11},
        ]

        gbfs = GBFS(self.graph)
        for tc in test_cases:
            result = gbfs.search(origin=tc["origin"], destinations=tc["destinations"])

            assert result is not None
            assert result.origin == tc["origin"]
            if tc["expected_path"] is None:
                assert result.path is None
            else:
                assert result.path == tc["expected_path"]
            assert result.path_cost == tc["expected_cost"]
            assert result.nodes_created == tc["expected_nodes"]
            if tc["expected_path"]:
                assert result.destination == tc["expected_path"][-1]

    def test_dijkstra(self):
        """Test Dijkstra with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [11], "expected_path": [1, 3, 5, 7, 9, 11], "expected_cost": 28, "expected_nodes": 13},
            {"origin": 3, "destinations": [11], "expected_path": [3, 5, 7, 9, 11], "expected_cost": 22, "expected_nodes": 11},
            {"origin": 6, "destinations": [9], "expected_path": [6, 7, 9], "expected_cost": 14, "expected_nodes": 11},
            {"origin": 5, "destinations": [11], "expected_path": [5, 7, 9, 11], "expected_cost": 17, "expected_nodes": 11},
            {"origin": 2, "destinations": [9, 11], "expected_path": [2, 4, 8, 9], "expected_cost": 21, "expected_nodes": 11},
            {"origin": 5, "destinations": [5], "expected_path": [5], "expected_cost": 0, "expected_nodes": 1},
        ]

        dijkstra = CUS1(self.graph)
        for tc in test_cases:
            result = dijkstra.search(origin=tc["origin"], destinations=tc["destinations"])

            assert result is not None
            assert result.origin == tc["origin"]
            if tc["expected_path"] is None:
                assert result.path is None
            else:
                assert result.path == tc["expected_path"]
            assert result.path_cost == tc["expected_cost"]
            assert result.nodes_created == tc["expected_nodes"]
            if tc["expected_path"]:
                assert result.destination == tc["expected_path"][-1]
