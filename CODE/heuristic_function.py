def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def advanced_heuristic(state, goal, world, safe_tiles):
    if not state.has_gold:
        h1 = manhattan_distance(state.pos, goal)
    else:
        h1 = manhattan_distance(state.pos, (0, 0))

    h2 = 1000 if not state.has_gold else 0
    
    h3 = 0
    for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
        ni, nj = state.pos[0] + dx, state.pos[1] + dy
        if world.in_bounds((ni, nj)) and (ni, nj) in safe_tiles:
            h3 += 1

    h4 = 0
    if state.pos not in safe_tiles:
        p_pit = 0.2
        p_wumpus = 2 / (world.size * world.size)
        h4 = (p_pit + p_wumpus) * 1000

    return h1 + h2 + h3 + h4