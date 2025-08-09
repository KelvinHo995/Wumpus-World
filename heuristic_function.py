def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def advanced_heuristic_function(state, goal, world):
    # manhattan from this tile to goal tile
    if not state.has_gold:
        h1 = manhattan_distance(state.pos, goal)
    else:
        h1 = manhattan_distance(state.pos, (0, 0))

    # gold heuristic is 1000 by default, else 0 to encourage finding gold
    if not state.has_gold:
        h2 = 1000
    else:
        h2 = 0
    
    # heuristic to encourage going to safe/unsafe tiles with more unknown neighbours
    h3 = 0
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        ni, nj = state.pos[0] + dx, state.pos[1] + dy
        if world.in_bounds((ni, nj)) and world.is_safe((ni, nj)):
            h3 += 1

    # if this state is unsafe then put some weight, dying has a cost of 1000
    p_pit = 0.2, p_wumpus = 2 / (world.height * world.height)
    if not world.is_safe(state.pos):
        h4  = (p_pit + p_wumpus) * 1000


    # danger_fining = 0
    # for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
    #     ni, nj = state.pos[0] + dx, state.pos[1] + dy
    #     if world.in_bounds((ni, nj)) and ((ni, nj) in world.get_danger_positions()):
    #         danger_fining += fining_value

    return h1 + h2 + h3 + h4
