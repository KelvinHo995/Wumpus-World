from state import State
from directions import DIRECTIONS, direction_to_delta

def rotate_left(dir):
    return DIRECTIONS[(DIRECTIONS.index(dir) - 1) % 4]

def rotate_right(dir):
    return DIRECTIONS[(DIRECTIONS.index(dir) + 1) % 4]

def generate_successors(state, map_size, risky_mode=False):
    successors = []
    dx, dy = direction_to_delta(state.direction)
    new_pos = (state.pos[0] + dx, state.pos[1] + dy)
    
    if 0 <= new_pos[0] < map_size and 0 <= new_pos[1] < map_size:
        new_state = State(
            pos=new_pos,
            direction=state.direction,
            has_gold=state.has_gold,
            has_arrow=state.has_arrow,
            cost=state.cost + 1
        )
        successors.append(("move forward", new_state))
    
    successors.append(("turn left", State(
        pos=state.pos,
        direction=rotate_left(state.direction),
        has_gold=state.has_gold,
        has_arrow=state.has_arrow,
        cost=state.cost + 1
    )))
    
    successors.append(("turn right", State(
        pos=state.pos,
        direction=rotate_right(state.direction),
        has_gold=state.has_gold,
        has_arrow=state.has_arrow,
        cost=state.cost + 1
    )))
    
    if risky_mode and state.has_arrow:
        successors.append(("shoot", State(
            pos=state.pos,
            direction=state.direction,
            has_gold=state.has_gold,
            has_arrow=False,
            cost=state.cost + 10
        )))
    
    if state.pos == (0, 0):
        successors.append(("climb out", State(
            pos=state.pos,
            direction=state.direction,
            has_gold=state.has_gold,
            has_arrow=state.has_arrow,
            cost=state.cost
        )))
    
    return successors