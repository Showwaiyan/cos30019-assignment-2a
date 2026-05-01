import pytest
from search.services.parser import load_map
from search.models.graph import Node


class TestParser:

    def test_load_valid_map(self, tmp_path):
        map_file = tmp_path / "test_map.txt"
        map_file.write_text(
            "1\n5;7\n1:(1,4)\n2:(4,10)\n3:(9,11)\n4:(6,7)\n5:(13,9)\n6:(5,4)\n7:(9,6)\n1,2,9\n1,4,7\n2,3,6\n5,3,7")

        origin, destinations, graph = load_map(str(map_file))

        assert origin == 1
        assert destinations == [5, 7]
        assert 1 in graph
        assert 2 in graph
        assert 3 in graph

    def test_origin_and_destinations(self, tmp_path):
        map_file = tmp_path / "test_map.txt"
        map_file.write_text("5\n10;20;30\n1:(0,0)")

        origin, destinations, graph = load_map(str(map_file))

        assert origin == 5
        assert destinations == [10, 20, 30]

    def test_edge_parsing(self, tmp_path):
        map_file = tmp_path / "test_map.txt"
        map_file.write_text(
            "1\n2\n1:(0,0)\n2:(1,1)\n3:(2,2)\n1,2,3\n2,3,4")

        origin, destinations, graph = load_map(str(map_file))

        assert 1 in graph
        assert 2 in graph
        assert 3 in graph
        assert (2, 3) in graph[1].neighbors
        assert (3, 4) in graph[2].neighbors

    def test_node_coordinates(self, tmp_path):
        map_file = tmp_path / "test_map.txt"
        map_file.write_text("1\n2\n1:(3,7)\n2:(10,5)\n1,2,5")

        origin, destinations, graph = load_map(str(map_file))

        assert graph[1].x == 3
        assert graph[1].y == 7
        assert graph[2].x == 10
        assert graph[2].y == 5

    def test_bidirectional_edges(self, tmp_path):
        map_file = tmp_path / "test_map.txt"
        map_file.write_text("1\n2\n1:(0,0)\n2:(1,1)\n1,2,5\n2,1,5")

        origin, destinations, graph = load_map(str(map_file))

        assert (2, 5) in graph[1].neighbors
        assert (1, 5) in graph[2].neighbors

    def test_empty_destinations(self, tmp_path):
        map_file = tmp_path / "test_map.txt"
        map_file.write_text("1\n2\n1:(0,0)")

        origin, destinations, graph = load_map(str(map_file))

        assert destinations == [2]
