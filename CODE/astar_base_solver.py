import heapq
from CODE.state import State

class BaseAStarSolver:
    def __init__(self, world, safe_tiles):
        self.world = world
        self.start_pos = world.agent_pos
        self.start_dir = world.agent_dir
        self.gold_pos = world.gold_pos
        self.safe_tiles = safe_tiles
        
    def init_state(self):
        return State(
            pos=self.start_pos,
            direction=self.start_dir,
            has_gold=False,
            has_arrow=True
        )
    
    def heuristic(self, state):
        from CODE.heuristic_function import advanced_heuristic
        return advanced_heuristic(state, self.gold_pos, self.world, self.safe_tiles)
    
    def generate_successors(self, state):
        raise NotImplementedError("Subclasses must implement this method")
    
    def is_valid_position(self, pos):
        raise NotImplementedError("Subclasses must implement this method")
    
    def is_goal(self, state):
        if state.has_gold:
            return state.pos == (0, 0)
        return False
    
    def a_star(self, start_state):
        frontier = []
        heapq.heappush(frontier, (0, start_state))
        
        came_from = {}
        cost_so_far = {start_state: 0}
        
        while frontier:
            _, current = heapq.heappop(frontier)
            
            if self.is_goal(current):
                return self.reconstruct_path(came_from, current)
            
            for action, neighbor in self.generate_successors(current):
                if not self.is_valid_position(neighbor.pos):
                    continue
                    
                new_cost = cost_so_far[current] + neighbor.cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = (current, action, neighbor.pos)
                    
        return None
    
    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            current, action, pos = came_from[current]
            path.append((action, pos))
        path.reverse()
        return path