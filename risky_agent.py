from astar_base_agent import BaseAStarAgent

class RiskyAStarAgent(BaseAStarAgent):
    def solve(self):
        def is_safe_or_unknown(pos):
            return pos not in self.world.confirmed_dangers
        return self.a_star(self.init_state(), is_safe_or_unknown)
