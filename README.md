# Architecture — Class Diagram

```mermaid
---
config:
  layout: elk
---
classDiagram
    direction TB

    class GraphSearch {
        <<abstract>>
        +graph : dict
        +__init__(graph: dict)
        +search(origin: int, destinations: list) dict*
    }

    class BFS {
        -frontier : deque
        +search(origin: int, destinations: list) dict
    }

    class DFS {
        -frontier : list
        +search(origin: int, destinations: list) dict
    }

    class GBFS {
        -frontier : heapq
        +search(origin: int, destinations: list) dict
    }

    class AStar {
        -frontier : heapq
        -g_costs : dict
        +search(origin: int, destinations: list) dict
    }

    class CUS1 {
        +search(origin: int, destinations: list) dict
    }

    class CUS2 {
        +search(origin: int, destinations: list) dict
    }

    class Registry {
        +ALGORITHM_REGISTRY : dict
        +get_algorithm(name: str) type~GraphSearch~
    }

    class Parser {
        +load_map(filename: str) tuple
    }

    class Logger {
        +print_result(result: dict)
    }

    class CLI {
        +main()
    }

    GraphSearch <|-- BFS
    GraphSearch <|-- DFS
    GraphSearch <|-- GBFS
    GraphSearch <|-- AStar
    GraphSearch <|-- CUS1
    GraphSearch <|-- CUS2

    Registry --> GraphSearch : returns class type
    CLI --> Registry : get_algorithm(method)
    CLI --> Parser : origin, destinations, graph
    CLI --> Logger : print_result(result)
    CLI --> GraphSearch : AlgoClass(graph).search(origin, destinations)
```

## Key Design Decisions

| Decision | Rationale |
|---|---|
| `GraphSearch` is abstract | Enforces uniform `search()` interface across all algorithms via Python `ABC` |
| `graph` stored in `__init__` | Stable state — defines what the object operates on |
| `origin` & `destinations` as `search()` params | Transient query inputs — allows object reuse across multiple searches |
| `Registry` returns class type, not instance | CLI controls instantiation; separates name resolution from object creation (DI pattern) |
| `Parser` is a standalone service | Keeps file I/O concerns out of `GraphSearch` (Single Responsibility Principle) |
| `Logger` is a standalone service | Decouples output formatting from algorithm logic; easy to swap for GUI renderer later |
