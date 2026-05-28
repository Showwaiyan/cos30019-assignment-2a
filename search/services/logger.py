from search.models.result import SearchResult


class Logger:
    """Handles all CLI output formatting."""

    @staticmethod
    def print_result(result: SearchResult) -> None:
        """
        Print the search result to stdout in the requested format.

        :param result: SearchResult dataclass instance
        """
        print(f"> Starting Node: {result.origin}")
        print(f"> Destination Node: {result.destination}")

        if result.path is None:
            print("> No solution found.")
        else:
            print(f"> Number of nodes created: {result.nodes_created}")
            path_str = " -> ".join(map(str, result.path))
            print(f"> Path: {path_str}")
            cost = f"{result.path_cost:.1f}" if result.path_cost % 1 != 0 else int(result.path_cost)
            print(f"> Path Cost: {cost}")
