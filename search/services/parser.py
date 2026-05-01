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
    graph = {}
    origin = 0
    destinations = []

    with open(filename) as file:
        origin = int(file.readline())

        # e.g. "5;7" -> [5, 7]
        destinations = list(map(lambda x: int(x),file.readline().strip().split(";")))

        for line in file:
            if('(' in line):
                # Node line format: "1:(1,4)" -> id=1, x=1, y=4
                node_id, coordinates = line.strip().split(":")
                x, y = coordinates.replace("(", "").replace(")", "").split(",")  
                graph[int(node_id)] = Node(int(node_id), int(x), int(y), [])
                continue
            
            # Edge line format: "1,2,5" -> from=1, to=2, cost=5
            from_id, to_id, cost = list(map(lambda x: int(x), line.strip().split(",")))
            graph[from_id].neighbors.append((to_id,cost))
        
    return (origin,destinations, graph)

