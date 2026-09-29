"""
Usage: python3 dfs.py exampleMap.txt
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from collections import deque
import linecache


# Directions are numbered clockwise, starting at north.
ORIENTATION_NAMES = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
DIRECTIONS = (
    (-1, 0), (-1, 1), (0, 1), (1, 1),
    (1, 0), (1, -1), (0, -1), (-1, -1),
)


@dataclass(frozen=True)
class State:
    row: int
    column: int
    orientation: int


@dataclass
class Node:
    state: State
    parent: Node | None
    action: str | None
    depth: int
    cost: int


@dataclass
class Result:
    final: Node | None
    last_examined: Node | None
    explored: int
    frontier: int

class Problem:
    # Load and validate the grid and its start and goal states.
    def __init__(self, grid: list[list[int]], start: State, goal: State):
        if not grid or not grid[0]:
            raise ValueError("The map must be nonempty")

        width = len(grid[0])
        for row in grid:
            if len(row) != width:
                raise ValueError("The map must be rectangular")

        self.grid = grid
        self.start = start
        self.goal = goal

        if not self.within_bounds(start.row, start.column):
            raise ValueError("Start is outside the map")
        if not self.within_bounds(goal.row, goal.column):
            raise ValueError("Goal is outside the map")

        # Orientation 8 means "any direction" for the goal only.
        if not 0 <= start.orientation < 8 or not 0 <= goal.orientation <= 8:
            raise ValueError("Invalid orientation")

    def within_bounds(self, row: int, column: int) -> bool:
        return 0 <= row < len(self.grid) and 0 <= column < len(self.grid[0])

    def is_goal(self, state: State) -> bool:
        # The goal can require a specific direction or accept any direction.
        goal_position = state.row == self.goal.row and state.column == self.goal.column
        goal_direction = self.goal.orientation == 8 or state.orientation == self.goal.orientation
        return goal_position and goal_direction

    def successors(self, node: Node) -> list[Node]:
        # Generate the possible actions in this order: forward, right, left.
        state = node.state
        children = []

        row_change, column_change = DIRECTIONS[state.orientation]
        next_row = state.row + row_change
        next_column = state.column + column_change

        if self.within_bounds(next_row, next_column):
            forward_state = State(next_row, next_column, state.orientation)
            move_cost = self.grid[next_row][next_column]
            children.append(
                Node(forward_state, node, "move_forward", node.depth + 1, node.cost + move_cost)
            )

        right_state = State(state.row, state.column, (state.orientation + 1) % 8)
        children.append(Node(right_state, node, "turn_right", node.depth + 1, node.cost + 1))

        left_state = State(state.row, state.column, (state.orientation - 1) % 8)
        children.append(Node(left_state, node, "turn_left", node.depth + 1, node.cost + 1))

        return children


class DFSSearch:
    def __init__(self, problem: Problem):
        self.problem = problem

    def search(self) -> Result:
        # Keep pending nodes on a stack and skip states already examined.
        start_node = Node(self.problem.start, None, None, 0, 0)
        stack = [start_node]
        visited: set[State] = set()
        last_examined = None

        while stack:
            current = stack.pop()
            if current.state in visited:
                continue

            visited.add(current.state)
            last_examined = current

            if self.problem.is_goal(current.state):
                return Result(current, last_examined, len(visited), len(stack))

            # A stack removes the last item first, so add children in reverse order.
            children = self.problem.successors(current)
            for child in reversed(children):
                if child.state not in visited:
                    stack.append(child)

        return Result(None, last_examined, len(visited), len(stack))

class BFSSearch:
    def __init__(self, problem: Problem):
        self.problem = problem

    def search(self) -> Result:
        
        queue = deque()
        queue_coordinates = set()
        visited: set[State] = set()

        def get_coordinates(rotation):

            if rotation == 0:
                return -1, 0
            elif rotation == 1:
                return -1, 1
            elif rotation == 2:
                return 0, 1
            elif rotation == 3:
                return 1, 1
            elif rotation == 4:
                return 1, 0
            elif rotation == 5:
                return 1, -1
            elif rotation == 6:
                return 0, -1
            elif rotation == 7:
                return -1, -1

        for rotation in range(8):

            start_state = {
                "x": self.problem.start.row,
                "y": self.problem.start.column,
                "rotation": rotation
            }

            queue.append(
                (start_state, 0)
            )

        queue_coordinates.add((
            self.problem.start.row,
            self.problem.start.column
        ))         

        while queue:
            
            current, step_count = queue.popleft()

            x = current["x"]
            y = current["y"]
            rotation = current["rotation"]

            state = (x, y, rotation)

            if state in visited:
                continue

            visited.add(state)

            print("current_coordinates: ", x, y, rotation)

            if (
                x == self.problem.goal.row
                and
                y == self.problem.goal.column
                and
                (
                    self.problem.goal.orientation == 8
                    or rotation == self.problem.goal.orientation
                )
            ):
                print("GOAL FOUND")

                return Result(
                    None,
                    None,
                    len(visited),
                    len(queue)
                )

         
            update_x, update_y = get_coordinates(rotation)

            new_x = x + update_x
            new_y = y + update_y

            # Check if new coordinate is inside the map
            if (
                0 <= new_x < len(self.problem.grid)
                and
                0 <= new_y < len(self.problem.grid[0])
            ):
                new_coordinate = (new_x, new_y)

                # Only create a new epoch if this coordinate
                # has not been reached before.
                if new_coordinate not in queue_coordinates:

                    queue_coordinates.add(new_coordinate)
                    for new_rotation in range(8):

                        
                        rotation_steps = min(
                            abs(new_rotation - rotation),
                            8 - abs(new_rotation - rotation)
                        )

                        new_step_count = (
                            step_count
                            + rotation_steps
                            + 1
                        )

                        new_state = {
                            "x": new_x,
                            "y": new_y,
                            "rotation": new_rotation
                        }

                        queue.append(
                            (new_state, new_step_count)
                        )

        return Result(
            None,
            None,
            len(visited),
            len(queue)
        )
# Read the map file and create a Problem with its start and goal states.
def load_problem(path: str) -> Problem:
    with open(path, encoding="utf-8") as file:
        lines = [line.split() for line in file if line.strip()]

    rows = int(lines[0][0])
    columns = int(lines[0][1])
    if rows <= 0 or columns <= 0 or len(lines) != rows + 3:
        raise ValueError("Incorrect number of rows or lines")

    grid = []
    for line in lines[1:1 + rows]:
        values = list(map(int, line))
        if len(values) != columns:
            raise ValueError("Incorrect number of columns")
        grid.append(values)

    # Pass the three values separately: row, column, and orientation.
    start_line = lines[1 + rows]
    start = State(int(start_line[0]), int(start_line[1]), int(start_line[2]))

    goal_line = lines[2 + rows]
    goal = State(int(goal_line[0]), int(goal_line[1]), int(goal_line[2]))

    return Problem(grid, start, goal)


# Follow parent links to rebuild the route from start to destination.
def reconstruct_path(node: Node | None) -> list[Node]:
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    path.reverse()
    return path


# Convert the numeric direction into a readable label for the output.
def format_state(state: State) -> str:
    if state.orientation == 8:
        direction = "*"
    else:
        direction = ORIENTATION_NAMES[state.orientation]
    return f"({state.row}, {state.column}, {direction})"


# Print the route, accumulated costs, and search statistics.
def show_result(result: Result) -> None:
    if result.final is None:
        print("No solution found. Path to the last examined node:")
        destination = result.last_examined
    else:
        print("Solution:")
        destination = result.final

    for index, node in enumerate(reconstruct_path(destination)):
        if index:
            print(f"Operator {index}: {node.action}")
        print(
            f"Node {index}: ({node.depth}, {node.cost}, "
            f"{node.action}, {format_state(node.state)})"
        )

    print(f"Total number of items in explored list: {result.explored}")
    print(f"Total number of items in frontier: {result.frontier}")


# Parse the command line, run DFS, and show the result.
def main() -> None:
    # parser = argparse.ArgumentParser(description="Depth-first search on the map")
    # parser.add_argument("grid", help="Input file, for example exampleMap.txt")
    # arguments = parser.parse_args()
    problem = load_problem("exampleMap.txt")

    print("Which algorithm would you like to use? (1) Depth-First (2) Breadth-First (3) A* :")
    choice = input()

    if choice == "1":
        print("You chose Depth-First Search and it will now be performed")
        result = DFSSearch(problem).search()
        show_result(result)
    elif choice == "2":
        print("You chose Breadth-First Search and it will now be performed")
        result = BFSSearch(problem).search()
        show_result(result)
    elif choice == "3":
        print("You chose A* Search, but it is not implemented yet.")
    else:
        print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()