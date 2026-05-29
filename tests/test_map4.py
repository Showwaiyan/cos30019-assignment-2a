import pytest
from search.algorithms.dfs import DFS
from search.algorithms.bfs import BFS
from search.algorithms.astar import AStar
from search.algorithms.gbfs import GBFS
from search.algorithms.cus2 import CUS2
from search.services.parser import load_map


class TestMap4:
    """Integration tests for Map4 using DFS."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load Map4 before each test."""
        origin, destinations, self.graph = load_map("maps/Map4.txt")
        self.origin = origin
        self.destinations = destinations

    def test_dfs(self):
        """Test DFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [14], "expected_path": [1, 2, 3, 5, 4, 6, 10, 8, 9, 11, 12, 13, 14], "expected_cost": 85, "expected_nodes": 14},
            {"origin": 1, "destinations": [7], "expected_path": [1, 2, 3, 5, 7], "expected_cost": 27, "expected_nodes": 14},
            {"origin": 3, "destinations": [14], "expected_path": [3, 1, 2, 4, 5, 6, 10, 8, 9, 11, 12, 13, 14], "expected_cost": 81, "expected_nodes": 14},
            {"origin": 5, "destinations": [14], "expected_path": [5, 3, 1, 2, 4, 6, 10, 8, 9, 11, 12, 13, 14], "expected_cost": 86, "expected_nodes": 14},
            {"origin": 6, "destinations": [7], "expected_path": [6, 4, 2, 1, 3, 5, 7], "expected_cost": 46, "expected_nodes": 8},
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
            {"origin": 1, "destinations": [14], "expected_path": [1, 2, 4, 10, 11, 14], "expected_cost": 50, "expected_nodes": 14},
            {"origin": 3, "destinations": [7, 14], "expected_path": [3, 5, 7], "expected_cost": 18, "expected_nodes": 8},
            {"origin": 5, "destinations": [14], "expected_path": [5, 4, 10, 11, 14], "expected_cost": 47, "expected_nodes": 14},
            {"origin": 6, "destinations": [7, 13], "expected_path": [6, 5, 7], "expected_cost": 15, "expected_nodes": 12},
            {"origin": 7, "destinations": [14], "expected_path": [7, 5, 4, 10, 11, 14], "expected_cost": 59, "expected_nodes": 14},
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
            {"origin": 1, "destinations": [14], "expected_path": [1, 2, 4, 10, 12, 14], "expected_cost": 43, "expected_nodes": 16},
            {"origin": 3, "destinations": [7, 14], "expected_path": [3, 5, 7], "expected_cost": 18, "expected_nodes": 9},
            {"origin": 5, "destinations": [14], "expected_path": [5, 6, 10, 12, 14], "expected_cost": 32, "expected_nodes": 15},
            {"origin": 6, "destinations": [7, 13], "expected_path": [6, 5, 7], "expected_cost": 15, "expected_nodes": 8},
            {"origin": 7, "destinations": [14], "expected_path": [7, 5, 6, 10, 12, 14], "expected_cost": 44, "expected_nodes": 15},
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
            {"origin": 1, "destinations": [14], "expected_path": [1, 2, 4, 10, 12, 14], "expected_cost": 43, "expected_nodes": 14},
            {"origin": 3, "destinations": [7, 14], "expected_path": [3, 5, 7], "expected_cost": 18, "expected_nodes": 8},
            {"origin": 5, "destinations": [14], "expected_path": [5, 6, 10, 12, 14], "expected_cost": 32, "expected_nodes": 14},
            {"origin": 6, "destinations": [7, 13], "expected_path": [6, 5, 7], "expected_cost": 15, "expected_nodes": 8},
            {"origin": 7, "destinations": [14], "expected_path": [7, 5, 6, 10, 12, 14], "expected_cost": 44, "expected_nodes": 14},
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
            {"origin": 1, "destinations": [14], "expected_path": [1, 2, 4, 10, 12, 14], "expected_cost": 43, "expected_nodes": 13},
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
