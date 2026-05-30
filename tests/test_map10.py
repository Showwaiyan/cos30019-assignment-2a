import pytest
from search.algorithms.dfs import DFS
from search.algorithms.bfs import BFS
from search.algorithms.astar import AStar
from search.algorithms.gbfs import GBFS
from search.algorithms.cus2 import CUS2
from search.algorithms.cus1 import CUS1
from search.services.parser import load_map


class TestMap10:
    """Integration tests for Map10 using DFS, BFS, AStar, and GBFS."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load Map10 before each test."""
        _, _, self.graph = load_map("maps/Map10.txt")

    def test_dfs(self):
        """Test DFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [15], "expected_path": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15], "expected_cost": 42, "expected_nodes": 12},
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
            {"origin": 1, "destinations": [15], "expected_path": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15], "expected_cost": 42, "expected_nodes": 15},
            {"origin": 3, "destinations": [14], "expected_path": [3, 11, 12, 13, 14], "expected_cost": 13, "expected_nodes": 12},
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
            {"origin": 1, "destinations": [15], "expected_path": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15], "expected_cost": 42, "expected_nodes": 15},
            {"origin": 3, "destinations": [14], "expected_path": [3, 11, 12, 13, 14], "expected_cost": 13, "expected_nodes": 8},
        ]

        astar = AStar(self.graph)
        for tc in test_cases:
            result = astar.search(origin=tc["origin"], destinations=tc["destinations"])
            assert result.path == tc["expected_path"]
            assert result.path_cost == tc["expected_cost"]
            assert result.nodes_created == tc["expected_nodes"]

    def test_cus2(self):
        """Test CUS2 (IDA*) with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [15], "expected_path": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15], "expected_cost": 42, "expected_nodes": 15},
            {"origin": 3, "destinations": [14], "expected_path": [3, 11, 12, 13, 14], "expected_cost": 13, "expected_nodes": 8},
        ]

        cus2 = CUS2(self.graph)
        for tc in test_cases:
            result = cus2.search(origin=tc["origin"], destinations=tc["destinations"])
            assert result.path == tc["expected_path"]
            assert result.path_cost == tc["expected_cost"]
            assert result.nodes_created == tc["expected_nodes"]

    def test_gbfs(self):
        """Test GBFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [15], "expected_path": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15], "expected_cost": 42, "expected_nodes": 15},
            {"origin": 3, "destinations": [14], "expected_path": [3, 11, 12, 13, 14], "expected_cost": 13, "expected_nodes": 8},
        ]

        gbfs = GBFS(self.graph)
        for tc in test_cases:
            result = gbfs.search(origin=tc["origin"], destinations=tc["destinations"])
            assert result.path == tc["expected_path"]
            assert result.path_cost == tc["expected_cost"]
            assert result.nodes_created == tc["expected_nodes"]

    def test_dijkstra(self):
        """Test Dijkstra with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [15], "expected_path": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15], "expected_cost": 42, "expected_nodes": 15},
            {"origin": 3, "destinations": [14], "expected_path": [3, 11, 12, 13, 14], "expected_cost": 13, "expected_nodes": 10},
            {"origin": 1, "destinations": [1], "expected_path": [1], "expected_cost": 0, "expected_nodes": 1},
        ]

        dijkstra = CUS1(self.graph)
        for tc in test_cases:
            result = dijkstra.search(origin=tc["origin"], destinations=tc["destinations"])
            assert result.path == tc["expected_path"]
            assert result.path_cost == tc["expected_cost"]
            assert result.nodes_created == tc["expected_nodes"]
