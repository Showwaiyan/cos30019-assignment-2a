import pytest
from search.algorithms.dfs import DFS
from search.algorithms.bfs import BFS
from search.algorithms.astar import AStar
from search.algorithms.gbfs import GBFS
from search.algorithms.cus1 import CUS1
from search.services.parser import load_map


class TestMap1:
    """Integration tests for Map1 using DFS and BFS."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load Map1 before each test."""
        origin, destinations, self.graph = load_map("maps/Map1.txt")
        self.origin = origin
        self.destinations = destinations

    def test_dfs(self):
        """Test DFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [5, 7], "expected_path": [1, 2, 3, 5], "expected_cost": 20, "expected_nodes": 7},
            {"origin": 1, "destinations": [3], "expected_path": [1, 2, 3], "expected_cost": 15, "expected_nodes": 5},
            {"origin": 3, "destinations": [1], "expected_path": [3, 2, 4, 1], "expected_cost": 18, "expected_nodes": 7},
            {"origin": 6, "destinations": [3], "expected_path": [6, 1, 2, 3], "expected_cost": 20, "expected_nodes": 6},
            {"origin": 7, "destinations": [1], "expected_path": [7, 3, 2, 4, 1], "expected_cost": 24, "expected_nodes": 7},
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
            {"origin": 1, "destinations": [5, 7], "expected_path": [1, 6, 5], "expected_cost": 15, "expected_nodes": 7},
            {"origin": 1, "destinations": [3], "expected_path": [1, 2, 3], "expected_cost": 15, "expected_nodes": 6},
            {"origin": 3, "destinations": [1], "expected_path": [3, 2, 4, 1], "expected_cost": 18, "expected_nodes": 7},
            {"origin": 6, "destinations": [3], "expected_path": [6, 5, 3], "expected_cost": 17, "expected_nodes": 7},
            {"origin": 7, "destinations": [1], "expected_path": [7, 4, 1], "expected_cost": 12, "expected_nodes": 7},
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
            {"origin": 1, "destinations": [5, 7], "expected_path": [1, 6, 5], "expected_cost": 15, "expected_nodes": 5},
            {"origin": 3, "destinations": [1], "expected_path": [3, 2, 4, 1], "expected_cost": 18, "expected_nodes": 7},
            {"origin": 6, "destinations": [3], "expected_path": [6, 4, 2, 3], "expected_cost": 15, "expected_nodes": 7},
            {"origin": 7, "destinations": [1], "expected_path": [7, 4, 1], "expected_cost": 12, "expected_nodes": 7},
            {"origin": 4, "destinations": [5, 7], "expected_path": [4, 6, 5], "expected_cost": 14, "expected_nodes": 6},
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


    def test_gbfs(self):
        """Test GBFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 1, "destinations": [5, 7], "expected_path": [1, 6, 5], "expected_cost": 15, "expected_nodes": 5},
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
            {"origin": 1, "destinations": [5, 7], "expected_path": [1, 6, 5], "expected_cost": 15, "expected_nodes": 7},
            {"origin": 3, "destinations": [1], "expected_path": [3, 2, 4, 1], "expected_cost": 18, "expected_nodes": 7},
            {"origin": 6, "destinations": [3], "expected_path": [6, 4, 2, 3], "expected_cost": 15, "expected_nodes": 7},
            {"origin": 7, "destinations": [1], "expected_path": [7, 4, 1], "expected_cost": 12, "expected_nodes": 7},
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

        # Edge case: invalid origin
        with pytest.raises(ValueError):
            dijkstra.search(origin=99, destinations=[1])
