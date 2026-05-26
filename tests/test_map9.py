import pytest
from search.algorithms.dfs import DFS
from search.algorithms.bfs import BFS
from search.algorithms.astar import AStar
from search.algorithms.gbfs import GBFS
from search.services.parser import load_map


class TestMap9:
    """Integration tests for Map9 using DFS, BFS, AStar, and GBFS."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load Map9 before each test."""
        _, _, self.graph = load_map("maps/Map9.txt")

    def test_dfs(self):
        """Test DFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [17], "expected_path": [1, 2, 5, 6, 7, 8, 9, 10, 13, 14, 15, 16, 17], "expected_cost": 51, "expected_nodes": 17},
            {"origin": 2, "destinations": [17], "expected_path": [2, 1, 3, 6, 5, 8, 9, 10, 13, 14, 15, 16, 17], "expected_cost": 51, "expected_nodes": 17},
            {"origin": 1, "destinations": [8], "expected_path": [1, 2, 5, 6, 7, 8], "expected_cost": 23, "expected_nodes": 8},
        ]

        dfs = DFS(self.graph)
        for tc in test_cases:
            result = dfs.search(origin=tc["origin"], destinations=tc["destinations"])
            assert result.path == tc["expected_path"]
            assert result.path_cost == tc["expected_cost"]
            assert result.nodes_created == tc["expected_nodes"]

    def test_bfs(self):
        """Test BFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [17], "expected_path": [1, 2, 5, 8, 9, 10, 13, 16, 17], "expected_cost": 39, "expected_nodes": 17},
            {"origin": 2, "destinations": [17], "expected_path": [2, 5, 8, 9, 10, 13, 16, 17], "expected_cost": 34, "expected_nodes": 17},
            {"origin": 1, "destinations": [8], "expected_path": [1, 2, 5, 8], "expected_cost": 17, "expected_nodes": 8},
        ]

        bfs = BFS(self.graph)
        for tc in test_cases:
            result = bfs.search(origin=tc["origin"], destinations=tc["destinations"])
            assert result.path == tc["expected_path"]
            assert result.path_cost == tc["expected_cost"]
            assert result.nodes_created == tc["expected_nodes"]

    def test_astar(self):
        """Test A* with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [17], "expected_path": [1, 3, 6, 8, 9, 11, 14, 16, 17], "expected_cost": 23, "expected_nodes": 17},
            {"origin": 2, "destinations": [17], "expected_path": [2, 5, 6, 8, 9, 11, 14, 16, 17], "expected_cost": 23, "expected_nodes": 17},
            {"origin": 1, "destinations": [8], "expected_path": [1, 3, 6, 8], "expected_cost": 9, "expected_nodes": 8},
        ]

        astar = AStar(self.graph)
        for tc in test_cases:
            result = astar.search(origin=tc["origin"], destinations=tc["destinations"])
            assert result.path == tc["expected_path"]
            assert result.path_cost == tc["expected_cost"]
            assert result.nodes_created == tc["expected_nodes"]

    def test_gbfs(self):
        """Test GBFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [17], "expected_path": [1, 3, 6, 8, 9, 11, 14, 16, 17], "expected_cost": 23, "expected_nodes": 17},
            {"origin": 2, "destinations": [17], "expected_path": [2, 5, 8, 9, 11, 14, 16, 17], "expected_cost": 26, "expected_nodes": 15},
            {"origin": 1, "destinations": [8], "expected_path": [1, 3, 6, 8], "expected_cost": 9, "expected_nodes": 8},
        ]

        gbfs = GBFS(self.graph)
        for tc in test_cases:
            result = gbfs.search(origin=tc["origin"], destinations=tc["destinations"])
            assert result.path == tc["expected_path"]
            assert result.path_cost == tc["expected_cost"]
            assert result.nodes_created == tc["expected_nodes"]
