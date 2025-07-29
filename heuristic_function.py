#Mức phạt cho các ô gần vùng nguy hiểm (Wumpus, hố,...)
fining_value = 1  # Có thể thay thành 2, 3 hoặc strict hơn để agent đi an toàn hơn 

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def advanced_heuristic_function(pos, goal, start=None, dangers=None):
    # Hàm heuristic nâng cao để hướng dẫn agent đi tìm vàng và quay về an toàn
    # - pos: vị trí hiện tại
    # - goal: vị trí vàng
    # - start: vị trí ban đầu (dùng để tính đường quay về)
    # - dangers: tập hợp các vị trí nguy hiểm (hố hoặc Wumpus)

    h1 = manhattan_distance(pos, goal)  #pos đến vàng
    h2 = manhattan_distance(goal, start) if start else 0  #vàng quay về

    danger_fining = 0  #penalty cộng dồn khi cứ đi gần vùng nguy hiểm

    if dangers:
        #Duyệt các ô xung quanh pos 
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                ni, nj = pos[0] + dx, pos[1] + dy
                if (ni, nj) in dangers:
                    danger_fining += fining_value 

    return h1 + h2 + danger_fining 
