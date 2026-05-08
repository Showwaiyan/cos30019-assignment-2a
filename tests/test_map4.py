import pytest
from search.algorithms.dfs import DFS
from search.algorithms.bfs import BFS
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
            {"origin": 1, "destinations": [14], "expected_path": [], "expected_cost": 0, "expected_nodes": 0},
            {"origin": 1, "destinations": [7], "expected_path": [], "expected_cost": 0, "expected_nodes": 0},
            {"origin": 3, "destinations": [14], "expected_path": [], "expected_cost": 0, "expected_nodes": 0},
            {"origin": 5, "destinations": [14], "expected_path": [], "expected_cost": 0, "expected_nodes": 0},
            {"origin": 6, "destinations": [7], "expected_path": [], "expected_cost": 0, "expected_nodes": 0},
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
            if tc["expected_path"] is not None:
                assert result.destination == tc["expected_path"][-1]

    def test_bfs(self):
        """Test BFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [14], "expected_path": [], "expected_cost": 0, "expected_nodes": 0},
            {"origin": 3, "destinations": [7, 14], "expected_path": [], "expected_cost": 0, "expected_nodes": 0},
            {"origin": 5, "destinations": [14], "expected_path": [], "expected_cost": 0, "expected_nodes": 0},
            {"origin": 6, "destinations": [7, 13], "expected_path": [], "expected_cost": 0, "expected_nodes": 0},
            {"origin": 7, "destinations": [14], "expected_path": [], "expected_cost": 0, "expected_nodes": 0},
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
            if tc["expected_path"] is not None:
                assert result.destination == tc["expected_path"][-1]
