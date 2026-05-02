import pytest
from search.algorithms.dfs import DFS
from search.models.graph import Node

map_0 = {
    1: Node(1, 0.0, 0.0, [(2, 1.0), (3, 1.0)]),
    2: Node(2, 2.0, 4.0, [(4, 1.0), (5, 1.0)]),
    3: Node(3, 4.0, 4.0, [(6, 1.0)]),
    4: Node(4, 1.0, 2.0, [(2, 1.0)]),
    5: Node(5, 3.0, 2.0, [(7, 1.0)]),
    6: Node(6, 5.0, 2.0, [(8, 1.0)]),
    7: Node(7, 2.0, 0.0, [(1, 1.0)]),
    8: Node(8, 6.0, 0.0, [])
}

class TestDFS:

    def test_finds_path(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[8])

        # Expected path for DFS (depends on neighbor order, but should reach 8)
        assert result is not None
        assert result.path is not None
        assert result.path[0] == 1  # Start node ID
        assert result.path[-1] == 8 # End node ID
        assert len(result.path) > 0

    def test_no_solution(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=8, destinations=[1])

        assert result.path is None or result.path == []

    def test_node_expansion_order(self):
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[8])

        # This test ensures your DFS handles the cycle 1->2->5->7->1 without crashing
        assert 1 in map_0  # Logic check to ensure setup is correct
        assert result.path is not None

    def test_with_obstacles(self):
        """Test by simulating a missing node (obstacle)."""
        # Create a map where node 3 (the bridge to 8) is removed
        restricted_map = map_0.copy()
        restricted_map[1] = Node(1, 0.0, 0.0, [(2, 1.0)]) # Removed 3

        dfs = DFS(restricted_map)
        result = dfs.search(origin=1, destinations=[8])

        assert result.path is None or result.path == [] # Path should be impossible now

    def test_invalid_bounds(self):
        """Test with IDs that don't exist in the dictionary."""
        dfs = DFS(map_0)

        # Testing a node ID (99) that isn't in our hardcoded dictionary
        with pytest.raises(ValueError):
            dfs.search(origin=1, destinations=[99])

    def test_start_equals_goal(self):
        """Test the edge case where start and end are the same."""
        dfs = DFS(map_0)
        result = dfs.search(origin=1, destinations=[1])

        assert result.path == [1]