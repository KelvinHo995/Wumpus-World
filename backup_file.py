from random import randint
from typing import Tuple
import os
import platform
import time

from percepts import Percept

DIRECTIONS = ['N', 'E', 'S', 'W']  # clockwise

def clear_console():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def display_step(agent, world):
    clear_console()

    # === Hiển thị bản đồ
    pos = agent.get_position()
    print("=== WUMPUS WORLD ===")
    for y in reversed(range(world.N)):
        row = ""
        for x in range(world.N):
            if (x, y) == pos:
                row += " A  "
            else:
                row += " .  "
        print(row)

    # === Thông tin Agent hiện tại
    print("\n=== AGENT STATE ===")
    print(f"Position      : {pos}")
    print(f"Facing        : {agent.get_facing()}")

    if agent.step_log:
        last_step = agent.step_log[-1]
        #action_taken = last_step[1]
        action_taken = last_step["action"]
        #result = last_step[2]
        result = last_step["result"]
        #short_result = result.split(" | ")[0]  #Ẩn Percepts để bảng gọn hơn
        #score = last_step[3]
        score = last_step["score"]
        percepts = last_step["percepts"]

        print(f"Action Taken  : {action_taken}")
        #print(f"Result        : {short_result}")
        print(f"Result        : {result}")
        print(f"Current Score : {score}")

        # # Hiển thị Percepts tách riêng
        # if "Percepts:" in result:
        #     percept_part = result.split("Percepts:")[1].strip(" []")
        #     print("\nPercepts:")
        #     for item in percept_part.split(", "):
        #         if ":" in item:
        #             k, v = item.split(":")
        #             print(f" - {k.capitalize()}: {v}")

        print("\nPercepts:")
        for k, v in percepts.items():
            print(f" - {k.capitalize()}: {v}")

    # === Bảng Action Log cập nhật
    print("\n=== ACTION LOG ===")
    print("{:<5} | {:<12} | {:<45} | Score".format("Step", "Action", "Result"))
    print("-" * 80)
    #for step, action, result, score in agent.step_log:
    #    short_result1 = result.split(" | ")[0]  # Ẩn Percepts để bảng gọn hơn

    for entry in agent.step_log:
        step = entry["step"]
        action = entry["action"]
        result = entry["result"]
        score = entry["score"]

        #print(f"{step:<5} | {action:<12} | {short_result1:<45} | {score}")
        print(f"{step:<5} | {action:<12} | {result:<45} | {score}")

    input("\nPress Enter to continue...")

# ======= Mô tả ô bản đồ =======
class Cell:
    def __init__(self):
        self.has_pit = False
        self.has_wumpus = False
        self.has_gold = False

# ======= Môi trường Wumpus World =======
class WumpusWorld:
    def __init__(self, N=4, K=2, p=0.2):
        self.N = N
        self.K = K
        self.p = p
        self.grid = [[Cell() for _ in range(N)] for _ in range(N)]
        self.set_fixed_map() # Có thể dùng dòng này hoặc dòng dưới...
        #self.place_elements()

    def set_fixed_map(self):
        # Không đặt pit/gold để dễ test
        # Đặt 1 Wumpus cố định tại (3,0) – hàng ngang với Agent
        self.grid[0][3].has_wumpus = True

        self.grid[3][3].has_wumpus = True  # nằm khác hướng → không bị bắn

        # (Tùy chọn) Đặt Gold để test hành vi khác
        # self.grid[0][2].has_gold = True

    def place_elements(self):
        # Wumpus
        count = 0
        while count < self.K:
            x, y = randint(0, self.N - 1), randint(0, self.N - 1)
            if (x, y) != (0, 0) and not self.grid[y][x].has_wumpus:
                self.grid[y][x].has_wumpus = True
                count += 1

        # Pits
        for y in range(self.N):
            for x in range(self.N):
                if (x, y) != (0, 0) and not self.grid[y][x].has_wumpus:
                    if randint(0, 100) < int(self.p * 100):
                        self.grid[y][x].has_pit = True

        # Gold (can appear at (0,0))
        while True:
            x, y = randint(0, self.N - 1), randint(0, self.N - 1)
            cell = self.grid[y][x]
            if not cell.has_pit and not cell.has_wumpus:
                cell.has_gold = True
                break

    def get_percepts(self, x: int, y: int):
        stench = breeze = glitter = False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.N and 0 <= ny < self.N:
                neighbor = self.grid[ny][nx]
                if neighbor.has_wumpus:
                    stench = True
                if neighbor.has_pit:
                    breeze = True
        glitter = self.grid[y][x].has_gold
        return {"stench": stench, "breeze": breeze, "glitter": glitter}

    def print_true_map(self):
        print("\n=== TRUE MAP (Full Info - For Debugging Only) ===")
        for y in reversed(range(self.N)):
            row = ""
            for x in range(self.N):
                cell = self.grid[y][x]
                items = []
                if cell.has_wumpus:
                    items.append("W")
                elif cell.has_pit:
                    items.append("P")
                elif cell.has_gold:
                    items.append("G")
                else:
                    items.append(".")
                content = "".join(items).ljust(3)
                row += f"{content}"
            print(row)

    def print_agent_map(self, agent):
        pos = agent.get_position()
        print("\n=== AGENT VIEW ===")
        for y in reversed(range(self.N)):
            row = ""
            for x in range(self.N):
                if (x, y) == pos:
                    row += " A  "
                else:
                    row += " .  "
            print(row)

        # In thêm thông tin trạng thái agent:
        print(f"\n[INFO] Agent position: {pos}")
        print(f"[INFO] Facing direction: {agent.get_facing()}")

        # Current percepts
        # percepts = self.get_percepts(*pos)
        # print("[INFO] Current percepts:")
        # for k, v in percepts.items():
        #     print(f" - {k.capitalize()}: {v}")

        # # Score
        # print(f"[INFO] Current score: {agent.score}")
        last_step = agent.step_log[-1] if agent.step_log else None
        if last_step:
            action_taken = last_step[1]
            result_text = last_step[2]
            current_score = last_step[3]

            print(f"[INFO] Action: {action_taken}")
            print(f"[INFO] Result: {result_text}")
            print(f"[INFO] Current score: {current_score}")


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

def main():
    world = WumpusWorld(N=8, K=2, p=0.2)
    agent = Agent()

    print("\n[1] Hiển thị bản đồ thật (Full Info):")
    world.print_true_map()

    print("\n[2] Start Simulation:")
    # actions = [
    #     "move forward", "turn left", "move forward",
    #     "grab", "turn right", "move forward",
    #     "move forward", "turn left", "move forward",
    #     "climb out"
    # ]
    actions = [
        "shoot",      # Bắn mũi tên từ (0,0) → hy vọng trúng (3,0)
        "move forward",
        "move forward",
        "move forward",
        "turn right",
        "move forward"
    ]

    for i, act in enumerate(actions):
        print(f"\n>> STEP {i+1}: {act.upper()}")
        percept = agent.action(act, world, i+1)
        #agent.action(act, world, i+1)
        # world.print_agent_map(agent)
        print("\n[***] Print percept for testing:") # muốn in dòng này thì phải tắt display_step ở dòng dưới
        print(percept) # muốn in dòng này thì phải tắt display_step ở dòng dưới
        display_step(agent, world)
        if not agent.is_alive:
            break

    # print("\n[3] Final Log:")
    # agent.print_log()

if __name__ == "__main__":
    main()
