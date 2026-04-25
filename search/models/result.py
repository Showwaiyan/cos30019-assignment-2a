from dataclasses import dataclass


@dataclass
class SearchResult:
    """
    Holds the output of a single search run.

    :param origin: starting node ID
    :param destination: reached goal node ID (None if no solution)
    :param path: ordered list of node IDs from origin to destination
    :param path_cost: total cost of the path
    :param nodes_created: total number of nodes created (expanded + frontier)
    """
    origin: int
    destination: int | None
    path: list[int] | None
    path_cost: float
    nodes_created: int
