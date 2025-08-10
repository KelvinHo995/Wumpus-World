from random import randint

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
