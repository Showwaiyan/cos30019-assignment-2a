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
    points = {}
    startNode = 0
    destinationNodes = []

    with open(filename) as file:
        startNode = int(file.readline())
        destinationNodes = list(map(lambda x: int(x),file.readline().strip().split(";")))
        for line in file:
            if('(' in line):
                part = line.strip().split(":")
                coordinates = part[1].replace("(", "").replace(")", "").split(",")  
                points[int(part[0])] = Node(int(part[0]), int(coordinates[0]), int(coordinates[1]), [])
                continue
            
            a = list(map(lambda x: int(x), line.strip().split(",")))
            points[a[0]].neighbors.append((a[1],a[2]))
        
    return [startNode,destinationNodes, points]

