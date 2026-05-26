import sys
from search.registry import get_algorithm
from search.services.parser import load_map
from search.services.logger import Logger


def main():
    if len(sys.argv) < 3:
        print("Usage: python search.py <map_filename> <algorithm_name>")
        sys.exit(1)

    filename = sys.argv[1]
    name = sys.argv[2]

    # Call load_map(filename) to parse the map
    origin, destinations, graph = load_map(filename)

    # Call get_algorithm(name) to get the algorithm class
    AlgoClass = get_algorithm(name)

    # Instantiate: AlgoClass(graph).search(origin, destinations)
    result = AlgoClass(graph).search(origin, destinations)

    # Call Logger.print_result(result) to output the result
    Logger.print_result(result)


if __name__ == "__main__":
    main()
