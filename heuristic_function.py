fining_value = 2

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def advanced_heuristic_function(state, goal, world):
    if not state.has_gold:
        h1 = manhattan_distance(state.pos, goal)
        h2 = manhattan_distance(goal, (0, 0))
    else:
        h1 = manhattan_distance(state.pos, (0, 0))
        h2 = 0

    danger_fining = 0
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        ni, nj = state.pos[0] + dx, state.pos[1] + dy
        if world.in_bounds((ni, nj)) and ((ni, nj) in world.get_danger_positions()):
            danger_fining += fining_value

    return h1 + h2 + danger_fining
