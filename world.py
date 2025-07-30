from inference_engine import InferenceEngine

class World:
    def __init__(self):
        self.inference = InferenceEngine()
        self.rules = [
            {
                "if": [
                    ("Breeze", ("x", "y")),
                    ("Adjacent", ("x", "y", "a", "b"))
                ],
                "then": ("PossiblyPit", ("a", "b"))
            },
            {
                "if": [
                    ("Stench", ("x", "y")),
                    ("Adjacent", ("x", "y", "a", "b"))
                ],
                "then": ("PossiblyWumpus", ("a", "b"))
            }
        ]
        self.facts = set()
        self.possible_dangers = set()
        self.safe_visited = set()
        self.agent_dir = 'EAST'

    def load_map(self, filepath):
        with open(filepath, 'r') as f:
            lines = [line.strip().split() for line in f if line.strip()]
        lines.reverse()  # Hàng dưới cùng là hàng 0

        self.height = len(lines)
        self.width = len(lines[0]) if self.height > 0 else 0

        self.pits = set()
        self.wumpus = set()
        self.gold_pos = None
        self.agent_pos = None

        for i in range(self.height):
            for j in range(self.width):
                cell = lines[i][j]
                pos = (i, j)
                if cell == 'A':
                    self.agent_pos = pos
                    self.safe_visited.add(pos)
                elif cell == 'P':
                    self.pits.add(pos)
                elif cell == 'W':
                    self.wumpus.add(pos)
                elif cell == 'G':
                    self.gold_pos = pos

    def in_bounds(self, pos):
        i, j = pos
        return 0 <= i < self.height and 0 <= j < self.width

    def is_pit(self, pos):
        return pos in self.pits

    def is_wumpus(self, pos):
        return pos in self.wumpus

    def is_gold(self, pos):
        return pos == self.gold_pos

    def update_percepts(self, percepts, pos):
        for percept in percepts:
            self.facts.add((percept, (str(pos[0]), str(pos[1]))))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = pos[0] + dx, pos[1] + dy
            if self.in_bounds((ni, nj)):
                self.facts.add(("Adjacent", (str(pos[0]), str(pos[1]), str(ni), str(nj))))

        inferred = self.inference.forward_chaining(self.rules, self.facts)

        self.possible_dangers = set()
        for (pred, args) in inferred:
            if pred in {"PossiblyPit", "PossiblyWumpus"}:
                self.possible_dangers.add((int(args[0]), int(args[1])))

    def get_danger_positions(self):
        return self.possible_dangers

    def is_safe(self, pos):
        return self.in_bounds(pos) and pos in self.confirmed_safe

    @property
    def confirmed_safe(self):
        return self.safe_visited.union({self.agent_pos})

    @property
    def confirmed_dangers(self):
        return self.possible_dangers - self.confirmed_safe
