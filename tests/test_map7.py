import pytest
from search.algorithms.dfs import DFS
from search.algorithms.bfs import BFS
from search.algorithms.astar import AStar
from search.algorithms.gbfs import GBFS
from search.algorithms.cus2 import CUS2
from search.algorithms.cus1 import CUS1
from search.services.parser import load_map


class TestMap7:
    """Integration tests for Map7 using DFS, BFS, AStar, and GBFS."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load Map7 before each test."""
        origin, destinations, self.graph = load_map("maps/Map7.txt")
        self.origin = origin
        self.destinations = destinations

    def test_dfs(self):
        """Test DFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [18], "expected_path": [1, 2, 3, 4, 5, 12, 11, 10, 9, 8, 7, 13, 14, 18], "expected_cost": 88, "expected_nodes": 17},
            {"origin": 6, "destinations": [12, 18], "expected_path": [6, 1, 2, 3, 4, 5, 12], "expected_cost": 50, "expected_nodes": 8},
            {"origin": 1, "destinations": [14], "expected_path": [1, 2, 3, 4, 5, 12, 11, 10, 9, 8, 7, 13, 14], "expected_cost": 78, "expected_nodes": 16},
            {"origin": 7, "destinations": [18], "expected_path": [7, 6, 1, 2, 3, 4, 5, 12, 11, 10, 15, 18], "expected_cost": 80, "expected_nodes": 16},
            {"origin": 10, "destinations": [1], "expected_path": [10, 9, 8, 7, 6, 1], "expected_cost": 14, "expected_nodes": 9},
        ]

        dfs = DFS(self.graph)
        for tc in test_cases:
            result = dfs.search(
                origin=tc["origin"], destinations=tc["destinations"])

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
            {"origin": 1, "destinations": [18], "expected_path": [1, 6, 7, 13, 14, 18], "expected_cost": 28, "expected_nodes": 17},
            {"origin": 6, "destinations": [12, 18], "expected_path": [6, 7, 13, 12], "expected_cost": 16, "expected_nodes": 12},
            {"origin": 1, "destinations": [14], "expected_path": [1, 6, 7, 13, 14], "expected_cost": 18, "expected_nodes": 14},
            {"origin": 7, "destinations": [18], "expected_path": [7, 13, 14, 18], "expected_cost": 23, "expected_nodes": 17},
            {"origin": 10, "destinations": [1], "expected_path": [10, 9, 8, 7, 6, 1], "expected_cost": 14, "expected_nodes": 17},
        ]

        bfs = BFS(self.graph)
        for tc in test_cases:
            result = bfs.search(
                origin=tc["origin"], destinations=tc["destinations"])

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
            {"origin": 1, "destinations": [18], "expected_path": [1, 6, 7, 13, 14, 18], "expected_cost": 28, "expected_nodes": 9},
            {"origin": 6, "destinations": [12, 18], "expected_path": [6, 7, 13, 12], "expected_cost": 16, "expected_nodes": 7},
            {"origin": 1, "destinations": [14], "expected_path": [1, 6, 7, 13, 14], "expected_cost": 18, "expected_nodes": 8},
            {"origin": 7, "destinations": [18], "expected_path": [7, 13, 14, 18], "expected_cost": 23, "expected_nodes": 7},
            {"origin": 10, "destinations": [1], "expected_path": [10, 9, 8, 7, 6, 1], "expected_cost": 14, "expected_nodes": 9},
        ]

        astar = AStar(self.graph)
        for tc in test_cases:
            result = astar.search(origin=tc["origin"], destinations=tc["destinations"])

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


    def test_cus2(self):
        """Test CUS2 (IDA*) with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [18], "expected_path": [1, 6, 7, 13, 14, 18], "expected_cost": 28, "expected_nodes": 6},
            {"origin": 6, "destinations": [12, 18], "expected_path": [6, 7, 13, 12], "expected_cost": 16, "expected_nodes": 4},
            {"origin": 1, "destinations": [14], "expected_path": [1, 6, 7, 13, 14], "expected_cost": 18, "expected_nodes": 6},
            {"origin": 7, "destinations": [18], "expected_path": [7, 13, 14, 18], "expected_cost": 23, "expected_nodes": 4},
            {"origin": 10, "destinations": [1], "expected_path": [10, 9, 8, 7, 6, 1], "expected_cost": 14, "expected_nodes": 6},
        ]

        cus2 = CUS2(self.graph)
        for tc in test_cases:
            result = cus2.search(origin=tc["origin"], destinations=tc["destinations"])

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

    def test_gbfs(self):
        """Test GBFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [18], "expected_path": [1, 2, 3, 4, 5, 12, 13, 14, 18], "expected_cost": 74, "expected_nodes": 12},
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
            {"origin": 1, "destinations": [14], "expected_path": [1, 6, 7, 13, 14], "expected_cost": 18, "expected_nodes": 16},
            {"origin": 5, "destinations": [14], "expected_path": [5, 12, 13, 14], "expected_cost": 28, "expected_nodes": 20},
            {"origin": 7, "destinations": [14], "expected_path": [7, 13, 14], "expected_cost": 13, "expected_nodes": 15},
            {"origin": 1, "destinations": [1], "expected_path": [1], "expected_cost": 0, "expected_nodes": 1},
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
