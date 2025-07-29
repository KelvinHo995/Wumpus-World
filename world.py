from k_inference import InferenceEngine
from utils import get_adjacent

class WumpusWorld:
    def __init__(self, map_file):
        self.grid, self.size = self.load_map(map_file)
        self.agent_pos = (0, 0)
        self.gold_pos = self.find_tile('G')
        self.facts = self.extract_facts()
        self.inferred_dangers = self.run_inference()

    def load_map(self, path):
        with open(path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        grid = [list(row) for row in lines]
        return grid, (len(grid), len(grid[0]))

    def find_tile(self, tile):
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == tile:
                    return (i, j)
        return None

    def extract_facts(self):
        facts = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.grid[i][j] == 'B':
                    facts.append(("Breeze", (str(i), str(j))))
                elif self.grid[i][j] == 'S':
                    facts.append(("Stench", (str(i), str(j))))
                for ni, nj in get_adjacent(i, j, self.size):
                    facts.append(("Adjacent", (str(i), str(j), str(ni), str(nj))))
        return facts

    def run_inference(self):
        engine = InferenceEngine()
        rules = [
            {
                "if": [("Breeze", ("x", "y")), ("Adjacent", ("x", "y", "a", "b"))],
                "then": ("PossiblyPit", ("a", "b"))
            },
            {
                "if": [("Stench", ("x", "y")), ("Adjacent", ("x", "y", "a", "b"))],
                "then": ("PossiblyWumpus", ("a", "b"))
            }
        ]
        return engine.forward_chaining(rules, self.facts)

    def is_safe(self, pos):
        i, j = pos
        for fact in self.inferred_dangers:
            if fact[0] in ["PossiblyPit", "PossiblyWumpus"]:
                x, y = map(int, fact[1])
                if (x, y) == (i, j):
                    return False
        return True

    def get_neighbors(self, pos):
        return get_adjacent(*pos, self.size)
    
    def get_danger_positions(self):
        dangers = set()
        for fact in self.inferred_dangers:
            if fact[0] in ["PossiblyPit", "PossiblyWumpus"]:
                x, y = map(int, fact[1])
                dangers.add((x, y))
        return dangers

