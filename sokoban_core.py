from collections import namedtuple
import heapq

Node = namedtuple("Node", ["path_cost", "state", "parent", "action"])

class SokobanProblem:
    def __init__(self, filepath):
        walls = set()
        boxes_start = set()
        targets = set()
        agent_start = None

        with open(filepath, "r") as f:
            lines = f.readlines()

        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                if ch == '%':
                    walls.add((r, c))
                elif ch == 'A':
                    agent_start = (r, c)
                elif ch == 'B':
                    boxes_start.add((r, c))
                elif ch == 'D':
                    targets.add((r, c))
                elif ch == 'C':
                    boxes_start.add((r, c))
                    targets.add((r, c))

        self.walls = frozenset(walls)
        self.targets = frozenset(targets)
        self.initial_state = (agent_start, frozenset(boxes_start))

    def is_goal(self, state):
        agent_pos, box_positions = state
        return box_positions == self.targets

    def get_successors(self, state):
        agent_pos, box_positions = state
        directions = {
            "North": (-1, 0), "South": (1, 0),
            "West":  (0, -1), "East":  (0, 1),
        }
        successors = []

        for action, (dr, dc) in directions.items():
            new_agent_pos = (agent_pos[0] + dr, agent_pos[1] + dc)

            if new_agent_pos in self.walls:
                continue

            if new_agent_pos in box_positions:
                new_box_pos = (new_agent_pos[0] + dr, new_agent_pos[1] + dc)
                if new_box_pos in self.walls or new_box_pos in box_positions:
                    continue
                new_box_positions = (box_positions - {new_agent_pos}) | {new_box_pos}
                successors.append((action, (new_agent_pos, new_box_positions)))
            else:
                successors.append((action, (new_agent_pos, box_positions)))

        return successors


class UCSSolver:
    """Chạy thuật toán UCS trên 1 SokobanProblem bất kỳ."""

    def __init__(self, problem):
        self.problem = problem

    def search(self):
        start_node = Node(path_cost=0, state=self.problem.initial_state,
                           parent=None, action=None)

        frontier = []
        counter = 0
        heapq.heappush(frontier, (0, counter, start_node))
        counter += 1

        explored = set()

        while True:
            if not frontier:
                return None

            _, _, current_node = heapq.heappop(frontier)

            if self.problem.is_goal(current_node.state):
                return self._reconstruct_path(current_node), current_node.path_cost

            if current_node.state in explored:
                continue
            explored.add(current_node.state)

            for action, new_state in self.problem.get_successors(current_node.state):
                new_node = Node(
                    path_cost=current_node.path_cost + 1,
                    state=new_state,
                    parent=current_node,
                    action=action,
                )
                heapq.heappush(frontier, (new_node.path_cost, counter, new_node))
                counter += 1

    def _reconstruct_path(self, node):
        actions = []
        while node.parent is not None:
            actions.insert(0, node.action)
            node = node.parent
        return actions