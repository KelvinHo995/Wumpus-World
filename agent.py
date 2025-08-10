from percepts import Percept
from world import WumpusWorld

DIRECTIONS = ['N', 'E', 'S', 'W']  # clockwise

# ======= Agent =======
class Agent:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dir_index = 1  # Start facing East (index in DIRECTIONS)
        self.has_gold = False
        self.is_alive = True
        self.remain_arrow = True
        self.score = 0
        self.step_log = []

    def get_position(self):
        return (self.x, self.y)
    
    def get_facing(self):
        return DIRECTIONS[self.dir_index]
    
    def action(self, act: str, world: WumpusWorld, step_no: int):
        result = ""
        bump = False
        scream = False

        if not self.is_alive:
            result = "Agent is dead. Minus 1000 points! No action possible!"
            percept = Percept(False, False, False, False, False)
            #self.step_log.append((step_no, act, result, self.score))
            self.step_log.append({
            "step": step_no,
            "action": act.upper(),
            "result": result,
            "percepts": percept.to_dict(),
            "score": self.score
            })
            return percept
        
        act = act.lower()

        if act == "turn left":
            self.dir_index = (self.dir_index - 1) % 4
            self.score -= 1
            result = f"Turned left. Now facing {self.get_facing()}"

        elif act == "turn right":
            self.dir_index = (self.dir_index + 1) % 4
            self.score -= 1
            result = f"Turned right. Now facing {self.get_facing()}"

        elif act == "move forward":
            dx, dy = 0, 0
            if self.get_facing() == 'N': dy = 1
            elif self.get_facing() == 'S': dy = -1
            elif self.get_facing() == 'E': dx = 1
            elif self.get_facing() == 'W': dx = -1

            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < world.N and 0 <= new_y < world.N:
                self.x = new_x
                self.y = new_y
                self.score -= 1
                current = world.grid[self.y][self.x]
                if current.has_pit:
                    self.score -= 1000
                    self.is_alive = False
                    result = "Agent fell into a Pit!"
                elif current.has_wumpus:
                    self.score -= 1000
                    self.is_alive = False
                    result = "Agent was eaten by Wumpus!"
                else:
                    result = f"Moved to ({self.x}, {self.y})"
            else:
                bump = True
                result = "BUMP! Hit wall. No movement."

        elif act == "grab":
            current = world.grid[self.y][self.x]
            if current.has_gold:
                self.has_gold = True 
                current.has_gold = False 
                self.score += 10
                result = "Grabbed the GOLD!"
            else:
                result = "No gold here to grab!"

        elif act == "shoot":
            if not self.remain_arrow:
                result = "No arrow left to shoot!"
            else:
                self.remain_arrow = False
                self.score -= 10
                result = "Shot arrow!"
                dx, dy = 0, 0

                if self.get_facing() == 'N': dy = 1
                elif self.get_facing() == 'S': dy = -1
                elif self.get_facing() == 'E': dx = 1
                elif self.get_facing() == 'W': dx = -1

                arrow_x, arrow_y = self.x, self.y
                while True:
                    arrow_x += dx
                    arrow_y += dy
                    if not (0 <= arrow_x < world.N and 0 <= arrow_y < world.N):
                        break

                    cell = world.grid[arrow_y][arrow_x]
                    if cell.has_wumpus:
                        cell.has_wumpus = False
                        scream = True
                        result += f" Scream! Killed Wumpus at ({arrow_x}, {arrow_y})"
                        break

        elif act == "climb out":
            if self.x == 0 and self.y == 0:
                if self.has_gold:
                    self.score += 1000
                    result = "Climbed out with Gold!"
                else:
                    result = "Climbed out without gold."
                self.is_alive = False
            else:
                result = "Can only climb out at (0,0)"

        #Modified with commit3
        percepts_raw = world.get_percepts(self.x, self.y)
        percept = Percept(
            stench=percepts_raw["stench"],
            breeze=percepts_raw["breeze"],
            glitter=percepts_raw["glitter"],
            bump=bump,
            scream=scream
        )
        # percepts["bump"] = bump
        # percepts["scream"] = scream
        # percept_str = ", ".join(f"{k}:{v}" for k, v in percepts.items())
        # self.step_log.append((step_no, act.upper(), result + f" | Percepts: [{percept_str}]", self.score))

         # Lưu lại vào log
        self.step_log.append({
            "step": step_no,
            "action": act.upper(),
            "result": result,
            "percepts": percept.to_dict(),
            "score": self.score
        })

        return percept 

    #Them
    def print_log(self):
        print("\n=== ACTION LOG ====")
        print("{:<5} | {:<12} | {:<50} | Score".format("Step", "Action", "Result"))
        print("-" * 85)
        for step, act, result, score in self.step_log:
            print(f"{step:<5} | {act:<12} | {result:<50} | {score}")

    def print_history(self):
        print("\n=== MOVE HISTORY ===")
        print("{:<5} | {:<10} | {}".format("Step", "Action", "Percepts"))
        print("-" * 40)
        for step, action, percepts in self.history:
            percept_str = ", ".join([f"{k}:{v}" for k, v in percepts.items()])
            print(f"{step:<5} | {action:<10} | {percept_str}")

    