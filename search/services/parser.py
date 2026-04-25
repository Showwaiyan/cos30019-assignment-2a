from search.models.graph import Node


def load_map(filename: str) -> tuple[int, list[int], dict]:
    """
    Parse a .txt map file and return the origin, destinations, and graph.

    File format:
        Line 1  : origin node ID
        Line 2  : destination node IDs separated by semicolons
        Lines   : node coordinates  N(x,y)
        Lines   : edges             (N1, N2, cost)

    :param filename: path to the .txt map file
    :return: (origin, destinations, graph)
             graph is dict of node_id -> Node
    """
    pass
