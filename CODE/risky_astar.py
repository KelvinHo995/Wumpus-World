from CODE.astar_base_solver import BaseAStarSolver
from CODE.successor import generate_successors
from CODE.heuristic_function import manhattan_distance

class RiskyAStarSolver(BaseAStarSolver):
    def __init__(self, world, frontier_tiles, visited_tiles):
        super().__init__(world, set())
        self.frontier_tiles = frontier_tiles
        self.visited_tiles = visited_tiles
        
    def generate_successors(self, state):
        return generate_successors(state, self.world, risky_mode=True)
    
    def is_valid_position(self, pos):
        return self.world.in_bounds(pos)
    
    def is_goal(self, state):
        if state.has_gold:
            return state.pos == (0, 0)
        return state.pos in (self.frontier_tiles - self.visited_tiles)
    
    def heuristic(self, state):
        if state.has_gold:
            return manhattan_distance(state.pos, (0, 0))
        
        unvisited_frontier = self.frontier_tiles - self.visited_tiles
        if not unvisited_frontier:
            return float('inf')
        
        return min(manhattan_distance(state.pos, tile) for tile in unvisited_frontier)
    
    def a_star(self, start_state):
        path = super().a_star(start_state)
        if not path:
            return None
            
        for i, (action, _) in enumerate(path):
            if action == "SHOOT":
                return path[:i+1]
                
        return path