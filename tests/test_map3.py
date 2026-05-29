import pytest
from search.algorithms.dfs import DFS
from search.algorithms.bfs import BFS
from search.algorithms.astar import AStar
from search.algorithms.gbfs import GBFS
from search.algorithms.cus2 import CUS2
from search.services.parser import load_map


class TestMap3:
    """Integration tests for Map3 using DFS."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Load Map3 before each test."""
        origin, destinations, self.graph = load_map("maps/Map3.txt")
        self.origin = origin
        self.destinations = destinations

    def test_dfs(self):
        """Test DFS with various origin-destination pairs."""
        test_cases = [
            {"origin": 2, "destinations": [7], "expected_path": None, "expected_cost":0 , "expected_nodes": 7},
            {"origin": 2, "destinations": [6], "expected_path": [2, 1, 3, 5, 4, 6], "expected_cost": 32, "expected_nodes": 7},
            {"origin": 1, "destinations": [7], "expected_path": None, "expected_cost": 0, "expected_nodes": 7},
            {"origin": 3, "destinations": [6], "expected_path": [3, 1, 2, 4, 5, 8, 6], "expected_cost": 48, "expected_nodes": 7},
            {"origin": 5, "destinations": [1], "expected_path": [5, 2, 1], "expected_cost": 14, "expected_nodes": 6},
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
            {"origin": 2, "destinations": [6], "expected_path": [2, 4, 6], "expected_cost": 13, "expected_nodes": 7},
            {"origin": 1, "destinations": [6], "expected_path": [1, 2, 4, 6], "expected_cost": 19, "expected_nodes": 7},
            {"origin": 3, "destinations": [6], "expected_path": [3, 2, 4, 6], "expected_cost": 21, "expected_nodes": 7},
            {"origin": 5, "destinations": [1], "expected_path": [5, 2, 1], "expected_cost": 14, "expected_nodes": 7},
            {"origin": 4, "destinations": [1], "expected_path": [4, 2, 1], "expected_cost": 13, "expected_nodes": 7},
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
            {"origin": 2, "destinations": [6], "expected_path": [2, 4, 6], "expected_cost": 13, "expected_nodes": 7},
            {"origin": 1, "destinations": [6], "expected_path": [1, 2, 4, 6], "expected_cost": 19, "expected_nodes": 7},
            {"origin": 3, "destinations": [6], "expected_path": [3, 5, 4, 6], "expected_cost": 17, "expected_nodes": 7},
            {"origin": 5, "destinations": [1], "expected_path": [5, 3, 1], "expected_cost": 14, "expected_nodes": 6},
            {"origin": 4, "destinations": [1, 6], "expected_path": [4, 6], "expected_cost": 6, "expected_nodes": 5},
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
            {"origin": 2, "destinations": [6], "expected_path": [2, 4, 6], "expected_cost": 13, "expected_nodes": 7},
            {"origin": 1, "destinations": [6], "expected_path": [1, 2, 4, 6], "expected_cost": 19, "expected_nodes": 7},
            {"origin": 3, "destinations": [6], "expected_path": [3, 5, 4, 6], "expected_cost": 17, "expected_nodes": 7},
            {"origin": 5, "destinations": [1], "expected_path": [5, 3, 1], "expected_cost": 14, "expected_nodes": 6},
            {"origin": 4, "destinations": [1, 6], "expected_path": [4, 6], "expected_cost": 6, "expected_nodes": 5},
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
            {"origin": 2, "destinations": [7], "expected_path": None, "expected_cost": 0, "expected_nodes": 7},
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
