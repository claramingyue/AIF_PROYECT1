from schemas import Node, Result, State


class DFSSearch:
    def __init__(self, problem):
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
