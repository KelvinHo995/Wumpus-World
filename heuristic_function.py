def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def advanced_heuristic(state, map_size, goals, safe_tiles, p_pit, n_wum):
    if not state.has_gold:
        h1 = min(manhattan_distance(state.pos, goal) for goal in goals)
    else:
        h1 = manhattan_distance(state.pos, (0, 0))

    h2 = 1000 if not state.has_gold else 0
    
    h3 = 0
    if not state.has_gold:
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            ni, nj = state.pos[0] + dx, state.pos[1] + dy
            if 0 <= ni < map_size and 0 <= nj < map_size and (ni, nj) in safe_tiles:
                h3 += 1

    h4 = 0
    if state.pos not in safe_tiles:
        p_wumpus = n_wum / (map_size ** 2)
        h4 = (p_pit + p_wumpus) * 1000

    return h1 + h2 + h3 + h4