from astar_base_solver import BaseAStarSolver
from successor import generate_successors
from heuristic_function import advanced_heuristic

class RiskyAStarSolver(BaseAStarSolver):
    def __init__(self, safe_tiles, visited_tiles, map_size, n_wum, p_pit, frontier_tiles):
        super().__init__(safe_tiles, visited_tiles, map_size, n_wum, p_pit)
        self.frontier_tiles = frontier_tiles
        self.visited_tiles = visited_tiles
        
    def generate_successors(self, state):
        return generate_successors(state, self.map_size, risky_mode=True)
    
    def is_valid_position(self, pos):
        return self.world.in_bounds(pos)
    
    def is_goal(self, state):
        if state.has_gold:
            return state.pos == (0, 0)
        return state.pos in (self.frontier_tiles - self.visited_tiles)
    
    def heuristic(self, state):
        if not state.has_gold:        
            goals = self.frontier_tiles - self.visited_tiles
        else:
            goals = [(0, 0)]
        
        return advanced_heuristic(state, self.map_size, goals, self.safe_tiles, self.p_pit, self.n_wum)
    
    def a_star(self, start_state):
        path = super().a_star(start_state)
        if not path:
            return None
            
        for i, (action, _) in enumerate(path):
            if action == "SHOOT":
                return path[:i+1]
                
        return path