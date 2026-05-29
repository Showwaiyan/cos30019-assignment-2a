import pytest
from search.algorithms.cus2 import CUS2
from search.services.parser import load_map


class TestCUS2:

    @pytest.fixture(autouse=True)
    def setup(self):
        origin, destinations, self.graph = load_map("maps/Map1.txt")
        self.origin = origin
        self.destinations = destinations

    def test_finds_path(self):
        cus2 = CUS2(self.graph)
        result = cus2.search(origin=1, destinations=[5, 7])
        assert result.path is not None
        assert result.path[0] == 1
        assert result.path[-1] in [5, 7]
        assert result.path == [1, 6, 5]

    def test_path_order(self):
        cus2 = CUS2(self.graph)
        result = cus2.search(origin=1, destinations=[3])
        assert result.path == [1, 2, 3]
        assert result.nodes_created == 6

    def test_different_origin_destinations(self):
        cus2 = CUS2(self.graph)

        result = cus2.search(origin=3, destinations=[1])
        assert result.path == [3, 2, 4, 1]
        assert result.path_cost == 18
        assert result.nodes_created == 7

        result = cus2.search(origin=6, destinations=[3])
        assert result.path == [6, 4, 2, 3]
        assert result.path_cost == 15
        assert result.nodes_created == 7

        result = cus2.search(origin=7, destinations=[1])
        assert result.path == [7, 4, 1]
        assert result.path_cost == 12
        assert result.nodes_created == 7

    def test_no_solution(self):
        from search.models.graph import Node
        restricted = {
            1: Node(1, 0, 0, [(2, 1)]),
            2: Node(2, 1, 0, [(1, 1)]),
            3: Node(3, 2, 0, []),
        }
        cus2 = CUS2(restricted)
        result = cus2.search(origin=1, destinations=[3])
        assert result.path is None
        assert result.destination == [3]
        assert result.nodes_created == 2

    def test_start_equals_goal(self):
        cus2 = CUS2(self.graph)
        result = cus2.search(origin=1, destinations=[1])
        assert result.path == [1]
        assert result.path_cost == 0
        assert result.nodes_created == 1

    def test_invalid_bounds(self):
        cus2 = CUS2(self.graph)
        with pytest.raises(ValueError):
            cus2.search(origin=1, destinations=[99])

    def test_path_cost(self):
        cus2 = CUS2(self.graph)
        result = cus2.search(origin=1, destinations=[5, 7])
        assert result.path_cost == 15

    def test_nodes_created(self):
        cus2 = CUS2(self.graph)
        result = cus2.search(origin=1, destinations=[5, 7])
        assert result.nodes_created == 5
