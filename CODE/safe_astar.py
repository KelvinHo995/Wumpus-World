from CODE.astar_base_solver import BaseAStarSolver
from CODE.successor import generate_successors
from CODE.heuristic_function import manhattan_distance

class SafeAStarSolver(BaseAStarSolver):
    def __init__(self, world, safe_tiles, visited_tiles):
        super().__init__(world, safe_tiles)
        self.visited_tiles = visited_tiles
        
    def generate_successors(self, state):
        return generate_successors(state, self.world, risky_mode=False)
    
    def is_valid_position(self, pos):
        return pos in self.safe_tiles
    
    def is_goal(self, state):
        if state.has_gold:
            return state.pos == (0, 0)
        return state.pos in (self.safe_tiles - self.visited_tiles)
    
    def heuristic(self, state):
        if state.has_gold:
            return manhattan_distance(state.pos, (0, 0))
        
        unvisited_safe = self.safe_tiles - self.visited_tiles
        if not unvisited_safe:
            return float('inf')
        
        return min(manhattan_distance(state.pos, tile) for tile in unvisited_safe)