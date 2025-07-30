import heapq
from state import State
from heuristic_function import advanced_heuristic_function
from successor import generate_successors

class BaseAStarAgent:
    def __init__(self, world):
        self.world = world
        self.start_pos = world.agent_pos
        self.start_dir = world.agent_dir
        self.gold_pos = world.gold_pos

    def init_state(self):
        return State(
            pos=self.start_pos,
            direction=self.start_dir,
            has_gold=False,
            has_arrow=True,
            is_alive=True,
            visited={self.start_pos},
            cost=0
        )

    def a_star(self, start_state, is_valid_fn):
        frontier = []
        heapq.heappush(frontier, (
            start_state.cost + advanced_heuristic_function(start_state, self.gold_pos, self.world),
            start_state
        ))

        came_from = {}
        g_score = {start_state: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if self.is_goal(current):
                return self.reconstruct_path(came_from, current)

            for action, neighbor in generate_successors(current, self.world):
                if not neighbor.is_alive or not is_valid_fn(neighbor.pos):
                    continue

                tentative_g = current.cost + (neighbor.cost - current.cost)
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    priority = tentative_g + advanced_heuristic_function(neighbor, self.gold_pos, self.world)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = (current, action)

        return None

    def is_goal(self, state):
        return state.has_gold and state.pos == (0, 0) and state.is_alive

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            prev, action = came_from[current]
            path.append((action, current.pos))
            current = prev
        path.reverse()
        return path
