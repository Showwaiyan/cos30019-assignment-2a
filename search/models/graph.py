from dataclasses import dataclass, field


@dataclass
class Node:
    """
    Represents a single node in the route-finding graph.

    :param id: unique node identifier
    :param x: x-coordinate
    :param y: y-coordinate
    :param neighbors: list of (neighbor_node_id, cost) tuples
    """
    id: int
    x: float
    y: float
    neighbors: list[tuple[int, float]] = field(default_factory=list)
