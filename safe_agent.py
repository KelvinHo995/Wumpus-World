from astar_base_agent import BaseAStarAgent

class SafeAStarAgent(BaseAStarAgent):
    def solve(self):
        return self.a_star(self.init_state(), lambda pos: self.world.is_safe(pos))
