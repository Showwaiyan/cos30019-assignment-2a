from search.models.result import SearchResult


class Logger:
    """Handles all CLI output formatting."""

    @staticmethod
    def print_result(result: SearchResult) -> None:
        """
        Print the search result to stdout in the required assignment format.

        If no solution found:
            <origin> <destination>
            No solution found.

        If solution found:
            <origin> <destination>
            <number_of_nodes_created>
            <path>
            <path_cost>

        :param result: SearchResult dataclass instance
        """
        pass
