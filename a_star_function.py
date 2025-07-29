import heapq  
from heuristic_function import advanced_heuristic_function  

class AStarAgent:
    def __init__(self, world):
        self.world = world
        self.start = world.agent_pos  
        self.gold = world.gold_pos  

    def solve(self):
        way_to_gold = self.a_star(self.start, self.gold)
        if not way_to_gold:
            return None 

        way_back_home = self.a_star(self.gold, self.start)
        if not way_back_home:
            return None  
        
        #Ghép hai đoạn đường lại, bỏ phần trùng nhau (ô chứa vàng)
        return way_to_gold[:-1] + way_back_home

    def a_star(self, start, goal):
        my_set = []
        heapq.heappush(my_set, (
            0 + advanced_heuristic_function(start, goal, self.start, self.world.get_danger_positions()),  #f = g + h
            0,  #g = 0 (chưa di chuyển bước nào)
            start  #vị trí hiện tại
        ))

        journey = {}  #Dùng để truy ngược đường đi
        g_score = {start: 0}  #Lưu chi phí đi ngắn nhất đến mỗi ô

        while my_set:
            _, g, current = heapq.heappop(my_set)  
            if current == goal:
                return self.reconstruct_path(journey, current)  #Tìm thấy đường, dựng lại đường đi ngược

            for neighbor in self.world.get_neighbors(current):
                if not self.world.is_safe(neighbor):
                    continue 

                tentative_g = g + 1  #Chi phí tạm thời nếu đi đến neighbor

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g 
                    priority = tentative_g + advanced_heuristic_function(
                        neighbor, goal, self.start, self.world.get_danger_positions()
                    )
                    heapq.heappush(my_set, (priority, tentative_g, neighbor))  
                    journey[neighbor] = current  

        return None  

    def reconstruct_path(self, journey, current):
        # Dựng lại đường đi từ goal ngược về start
        path = [current]
        while current in journey:
            current = journey[current]
            path.append(current)
        return path[::-1]  # Đảo ngược để có đường đi từ start đến goal
