from collections import deque

from schemas import Node, Result, State


class BFSSearch:
    def __init__(self, problem):
        self.problem = problem

    def search(self) -> Result:
        start_node = Node(self.problem.start, None, None, 0, 0)
        queue = deque([start_node])
        discovered: set[State] = {self.problem.start}
        visited: set[State] = set()
        last_examined = None

        while queue:
            current = queue.popleft()
            visited.add(current.state)
            last_examined = current

            if self.problem.is_goal(current.state):
                return Result(current, last_examined, len(visited), len(queue))

            children = self.problem.successors(current)

            for child in children:
                if child.state not in discovered:
                    discovered.add(child.state)
                    queue.append(child)

        return Result(None, last_examined, len(visited), len(queue))
