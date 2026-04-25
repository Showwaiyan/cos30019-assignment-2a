from search.base import TreeSearch
from search.algorithms.bfs import BFS
from search.algorithms.dfs import DFS
from search.algorithms.gbfs import GBFS
from search.algorithms.astar import AStar
from search.algorithms.cus1 import CUS1
from search.algorithms.cus2 import CUS2


ALGORITHM_REGISTRY = {
    "BFS":  BFS,
    "DFS":  DFS,
    "GBFS": GBFS,
    "AS":   AStar,
    "CUS1": CUS1,
    "CUS2": CUS2,
}


def get_algorithm(name: str) -> type[TreeSearch]:
    """
    Return the algorithm class corresponding to the given name.
    Raises ValueError if the name is not recognised.

    :param name: algorithm name string (e.g. 'BFS', 'AS')
    :return: TreeSearch subclass (not an instance)
    """
    pass
