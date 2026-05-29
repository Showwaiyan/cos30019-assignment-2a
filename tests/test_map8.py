import pytest
from search.algorithms.dfs import DFS
from search.algorithms.bfs import BFS
from search.algorithms.astar import AStar
from search.algorithms.gbfs import GBFS
from search.algorithms.cus2 import CUS2
from search.services.parser import load_map


class TestMap8:
    """Integration tests for Map8 using DFS, BFS, AStar, and GBFS."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load Map8 before each test."""
        _, _, self.graph = load_map("maps/Map8.txt")

    def test_dfs(self):
        """Test DFS with various origin-destination pairs."""
        test_cases = [
            # Default origin and destination
            {"origin": 1, "destinations": [16], "expected_path": [1, 2, 3, 4, 5, 16], "expected_cost": 32, "expected_nodes": 16},
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
            # Default origin and destination
            {"origin": 1, "destinations": [16], "expected_path": [1, 2, 3, 4, 5, 16], "expected_cost": 32, "expected_nodes": 16},
            {"origin": 9, "destinations": [16], "expected_path": [9, 15, 12, 5, 16], "expected_cost": 24, "expected_nodes": 16},
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
            # Default origin and destination
            {"origin": 1, "destinations": [16], "expected_path": [1, 9, 10, 11, 12, 5, 16], "expected_cost": 27, "expected_nodes": 13},
            {"origin": 2, "destinations": [2], "expected_path": [2], "expected_cost": 0, "expected_nodes": 1},
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
            {"origin": 1, "destinations": [16], "expected_path": [1, 9, 10, 11, 12, 5, 16], "expected_cost": 27, "expected_nodes": 13},
            {"origin": 9, "destinations": [16], "expected_path": [9, 10, 11, 12, 5, 16], "expected_cost": 22, "expected_nodes": 11},
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
            # Default origin and destination
            {"origin": 1, "destinations": [16], "expected_path": [1, 9, 15, 12, 5, 16], "expected_cost": 29, "expected_nodes": 13},
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
