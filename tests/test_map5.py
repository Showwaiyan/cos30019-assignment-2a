import pytest
from search.algorithms.dfs import DFS
from search.algorithms.bfs import BFS
from search.algorithms.astar import AStar
from search.algorithms.gbfs import GBFS
from search.algorithms.cus2 import CUS2
from search.services.parser import load_map


class TestMap5:
    """Integration tests for Map5 using DFS, BFS, A*, and GBFS."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load Map5 before each test."""
        origin, destinations, self.graph = load_map("maps/Map5.txt")
        self.origin = origin
        self.destinations = destinations

    def test_dfs(self):
        test_cases = [
            {"origin": 1, "destinations": [15], "expected_path": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], "expected_cost": 47, "expected_nodes": 15},
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
        test_cases = [
            {"origin": 1, "destinations": [15], "expected_path": [1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15], "expected_cost": 37, "expected_nodes": 15},
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
        test_cases = [
            {"origin": 1, "destinations": [15], "expected_path": [1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15], "expected_cost": 37, "expected_nodes": 15},
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
            {"origin": 1, "destinations": [15], "expected_path": [1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15], "expected_cost": 37, "expected_nodes": 15},
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
            {"origin": 1, "destinations": [15], "expected_path": [1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15], "expected_cost": 37, "expected_nodes": 14},
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
