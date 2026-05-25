from search.models.result import SearchResult


class Logger:
    """Handles all CLI output formatting."""

    @staticmethod
    def print_result(result: SearchResult) -> None:
        print(f"Starting Node: {result.origin}")

        dest = result.destination if result.destination is not None else "N/A"
        print(f"Destination Node: {dest}")
        print(f"Number of nodes created: {result.nodes_created}")

        if result.path is None:
            print("No solution found.")
        else:
            path_str = " -> ".join(str(n) for n in result.path)
            print(f"Path: {path_str}")
            print(f"Path Cost: {result.path_cost}")
