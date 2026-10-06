from schemas import Node, Result, State


class AStarSearch:
    def __init__(self, problem):
        self.problem = problem

    def heuristic(self, state: State) -> int:
        # Use Chebyshev distance as the heuristic.
        return max(
            abs(self.problem.goal.row - state.row),
            abs(self.problem.goal.column - state.column),
        )

    def search(self) -> Result:
        start_node = Node(
            self.problem.start,
            None,
            None,
            0,
            0,
            self.heuristic(self.problem.start),
        )
        prioritized_queue = [start_node]
        visited: set[State] = set()
        last_examined = None

        while prioritized_queue:
            # Sort the prioritized queue based on the total cost (cost + heuristic).
            prioritized_queue.sort(key=lambda node: node.cost + node.heuristic)
            current = prioritized_queue.pop(0)
            last_examined = current

            if current.state in visited:
                continue

            visited.add(current.state)

            if self.problem.is_goal(current.state):
                return Result(
                    current,
                    last_examined,
                    len(visited),
                    len(prioritized_queue),
                )

            children = self.problem.successors(current)

            for child in children:
                if child.state not in visited:
                    child.heuristic = self.heuristic(child.state)
                    prioritized_queue.append(child)

        return Result(
            None,
            last_examined,
            len(visited),
            len(prioritized_queue),
        )
