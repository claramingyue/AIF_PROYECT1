# AIF_PROYECT1

Implementation of different search algorithms for solving a pathfinding problem on a weighted grid.

The project includes the following algorithms:

- Depth-First Search (DFS)
- Breadth-First Search (BFS)
- A* Search

## Project Structure

```text
AIF_PROYECT1/
├── project1.py
├── dfs.py
├── bfs.py
├── astar.py
├── schemas.py
├── exampleMap.txt
└── lab1-AIF-2026.pdf
```

## Requirements

The project only uses the Python standard library.

Recommended version:

```text
Python 3.9+
```

## Execution

Clone the repository:

```bash
git clone https://github.com/claramingyue/AIF_PROYECT1.git
cd AIF_PROYECT1
```

Run the program with a map file:

```bash
python3 project1.py exampleMap.txt
```

The program will ask which search algorithm should be used:

```text
(1) Depth-First
(2) Breadth-First
(3) A*
```

## Map Format

The input file follows this structure:

```text
ROWS COLUMNS
COST COST COST ...
COST COST COST ...
...
START_ROW START_COLUMN START_ORIENTATION
GOAL_ROW GOAL_COLUMN GOAL_ORIENTATION
```

Each state is represented as:

```text
(row, column, orientation)
```

The available orientations are:

| Value | Orientation |
|------:|-------------|
| 0 | North |
| 1 | North-East |
| 2 | East |
| 3 | South-East |
| 4 | South |
| 5 | South-West |
| 6 | West |
| 7 | North-West |
| 8 | Any orientation (goal only) |

Coordinates are zero-indexed.

## Algorithms

### Depth-First Search

Implemented in `dfs.py`.

DFS uses a stack and explores one branch of the search space before backtracking.

### Breadth-First Search

Implemented in `bfs.py`.

BFS uses a queue and explores the search space level by level.

### A* Search

Implemented in `astar.py`.

A* evaluates nodes using:

```text
f(n) = g(n) + h(n)
```

where `g(n)` is the accumulated path cost and `h(n)` is the heuristic value.

The heuristic used is the Chebyshev distance:

```text
h(n) = max(|goal_row - row|, |goal_column - column|)
```

## Output

When a solution is found, the program prints the sequence of states and actions that form the resulting path.

It also reports information about the explored states and the remaining frontier.
