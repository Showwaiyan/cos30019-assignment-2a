# COS30019 Assignment 2A — Tree-Based Search

Group project implementing tree-based search algorithms for the Route-Finding problem.

## Usage

```
python search.py <filename> <method>
```

### Example

```
python search.py maps/Map1.txt BFS
```

### Supported Methods

| Method | Type | Description |
|--------|------|-------------|
| `BFS`  | Uninformed | Breadth-First Search |
| `DFS`  | Uninformed | Depth-First Search |
| `GBFS` | Informed   | Greedy Best-First Search |
| `AS`   | Informed   | A* Search |
| `CUS1` | Uninformed | Custom Search 1 |
| `CUS2` | Informed   | Custom Search 2 |

## Project Structure

```
tree-search/
├── search.py                   # CLI entry point
├── search/
│   ├── base.py                 # Abstract TreeSearch class
│   ├── registry.py             # Dependency injection registry
│   ├── algorithms/             # One file per algorithm
│   ├── services/               # Parser and Logger
│   └── models/                 # Node, SearchResult dataclasses
├── maps/                       # Map .txt files
└── tests/                      # Unit tests
```

## Requirements

```
python >= 3.10
pytest
```
