# Graph Search & Route Finding Algorithms (COS30019 - Assignment 2A)

A Python-based modular framework implementing and visualizing search algorithms on coordinate-based graph networks. The repository includes a command-line interface (CLI) for running searches, a comprehensive test suite, and an interactive **Pygame Visualizer** that showcases the node expansion process step-by-step in a modern dark theme.

---

## 🚀 Features

- **Standard Algorithms**:
  - **Breadth-First Search (BFS)**: Explores nodes level-by-level (unweighted shortest path).
  - **Depth-First Search (DFS)**: Explores as deep as possible before backtracking.
  - **Greedy Best-First Search (GBFS)**: Uses Euclidean distance heuristic to guide the search.
  - **A* Search (AS)**: Combines path cost and Euclidean distance heuristic for optimal search.
- **Custom Algorithms**:
  - **CUS1 (Dijkstra's)**: Finds the shortest path in a weighted graph using path cost only ($h(n) = 0$).
  - **CUS2 (Iterative Deepening A* / IDA*)**: An optimal memory-efficient variation of A* combining depth-first search depth control with A*'s $f$-cost evaluation.
- **Interactive Visualizer**: Modern, responsive Pygame GUI featuring:
  - File picker to load any map file.
  - Real-time controls (Play/Pause, Step-by-Step, Speed adjust, Reset).
  - Color-coded node types (Start, Goal, Frontier, Visited, Current).
  - Real-time metrics panel (Path cost, Nodes created, Step counter, FPS, Scale).
- **Comprehensive Testing**: Fully validated with `pytest` across 10 distinct map configurations and 125 test cases.

---

## 🛠️ Installation & Setup

1. **Clone/Navigate to the directory**:
   ```bash
   cd cos30019-assignment-2a
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: `requirements.txt` contains `pytest` and `pygame`.*

---

## 💻 Usage

### 1. Command-Line Interface (CLI)

Run search queries from the console by specifying the map file and the algorithm key name:

```bash
python search.py <map_filename> <algorithm_name>
```

#### Algorithm Keys:
- `BFS` - Breadth-First Search
- `DFS` - Depth-First Search
- `GBFS` - Greedy Best-First Search
- `AS` - A* Search
- `CUS1` - Dijkstra's Algorithm
- `CUS2` - Iterative Deepening A* (IDA*)

#### Example Command:
```bash
python search.py maps/Map1.txt AS
```

#### Example Output:
```text
> Starting Node: 1
> Destination Node: [8]
> Number of nodes created: 10
> Path: 1 -> 4 -> 2 -> 5 -> 7 -> 8
> Path Cost: 30
```

### 2. Interactive Pygame Visualizer

Launch the GUI to select maps, toggle algorithms, and view search progress interactively:

```bash
python visualize.py
```

#### Visualizer Features & Controls:
- **Load Map**: Click **Select Map** to open the in-app file explorer and pick a `.txt` map file.
- **Control Bar**: Use buttons to Play/Pause, Step Forward/Backward, Reset, or Speed up/slow down simulation.
- **Interactive Panel**: Use the sidebar to switch algorithms on the fly and see how each method alters node exploration order.

---

## 📁 Map File Format

The project parses custom graph files structured as follows:

```text
1            <-- Line 1: Origin/Start node ID
8            <-- Line 2: Destination node ID(s) (semicolon-separated for multiple: e.g. 5;7)
1:(0,0)      <-- Lines 3+: Node ID and its (x, y) coordinates for heuristic distance
2:(2,4)
3:(4,4)
...
1,2,10       <-- Lines after nodes: Edge definitions in the format (from_node, to_node, cost)
1,3,10
2,4,5
```

---

## 🏗️ Architecture

The code conforms to clean object-oriented principles, splitting concerns between CLI parsing, core search algorithms, and service-based outputs.

### Class Diagram

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

### Key Design Decisions

| Decision | Rationale |
|---|---|
| `GraphSearch` is abstract | Enforces uniform `search()` interface across all algorithms via Python `ABC` |
| `graph` stored in `__init__` | Stable state — defines what the object operates on |
| `origin` & `destinations` as `search()` params | Transient query inputs — allows object reuse across multiple searches |
| `Registry` returns class type, not instance | CLI controls instantiation; separates name resolution from object creation (DI pattern) |
| `Parser` is a standalone service | Keeps file I/O concerns out of `GraphSearch` (Single Responsibility Principle) |
| `Logger` is a standalone service | Decouples output formatting from algorithm logic; easy to swap for GUI renderer later |

---

## 🧪 Testing

The repository uses `pytest` for unit testing. The test suite verifies the correctness of paths, path costs, and frontier behaviors on various maps.

To run all tests:
```bash
pytest
```
