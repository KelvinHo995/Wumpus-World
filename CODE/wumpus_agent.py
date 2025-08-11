import random
from CODE.inference import InferenceEngine
from CODE.safe_astar import SafeAStarSolver
from CODE.risky_astar import RiskyAStarSolver
from CODE.state import State
class WumpusAgent:
    def __init__(self, world):
        self.world = world
        self.engine = InferenceEngine(world.size)
        self.rules = self.engine.parse_rules("rules.json")
        self.facts = self.initialize_facts()
        self.visited = set([(0, 0)])
        self.has_gold = False
        self.has_arrow = True
        self.score = 0
        self.action_count = 0
        
    def initialize_facts(self):
        facts = []
        size = self.world.size
        
        facts.append(("Safe", (0, 0)))
        facts.append(("Visited", (0, 0)))
        
        for i in range(size):
            for j in range(size):
                for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < size and 0 <= nj < size:
                        facts.append(("Adjacent", (i, j, ni, nj)))
        
        return facts
    
    def update_facts(self, percepts):
        x, y = self.world.agent_pos
        
        if (x, y) not in self.visited:
            self.visited.add((x, y))
            self.facts.append(("Visited", (x, y)))
        
        if "STENCH" in percepts:
            self.facts.append(("Stench", (x, y)))
        else:
            self.facts.append(("NotStench", (x, y)))
            
        if "BREEZE" in percepts:
            self.facts.append(("Breeze", (x, y)))
        else:
            self.facts.append(("NotBreeze", (x, y)))
            
        if "BUMP" in percepts:
            self.facts.append(("Wall", (x, y)))
            
        if "SCREAM" in percepts:
            self.facts.append(("Scream", ()))
            
        if "GLITTER" in percepts:
            self.facts.append(("Glitter", (x, y)))
    
    def choose_action(self):
        inferred = self.engine.forward_chaining(self.rules, self.facts)
        safe_tiles = self.engine.get_safe_tiles(inferred)
        frontier_tiles = self.engine.get_frontier_tiles(self.visited)
        
        current_state = State(
            self.world.agent_pos,
            self.world.agent_dir,
            self.has_gold,
            self.has_arrow
        )
        
        safe_solver = SafeAStarSolver(self.world, safe_tiles, self.visited)
        path = safe_solver.a_star(current_state)
        
        if not path:
            risky_solver = RiskyAStarSolver(self.world, frontier_tiles, self.visited)
            path = risky_solver.a_star(current_state)
        
        if not path:
            return random.choice(["TURN_LEFT", "TURN_RIGHT"])
        
        return path[0][0]
    
    def execute_action(self, action):
        self.action_count += 1
        result = self.world.execute_action(action)
        
        if action == "GRAB" and "GLITTER" in result.percepts:
            self.has_gold = True
        elif action == "SHOOT":
            self.has_arrow = False
        elif action == "CLIMB" and self.world.agent_pos == (0, 0):
            if self.has_gold:
                self.score += 1000
            return True
        
        if action == "FORWARD":
            self.score -= 1
        elif action in ["TURN_LEFT", "TURN_RIGHT"]:
            self.score -= 1
        elif action == "SHOOT":
            self.score -= 10
        elif action == "CLIMB":
            self.score += 1000 if self.has_gold else 0
        
        self.update_facts(result.percepts)
        
        if self.action_count % 5 == 0:
            self.world.move_wumpuses()
            self.update_facts_after_wumpus_movement()
        
        return False
    
    def update_facts_after_wumpus_movement(self):
        #Remove old stench information
        self.facts = [f for f in self.facts if f[0] not in ["Stench", "NotStench"]]
        
        #Add new percepts for current position
        current_percepts = self.world.get_percepts(self.world.agent_pos)
        self.update_facts(current_percepts)