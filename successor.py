from state import State

def direction_to_delta(dir):
    return {
        "NORTH": (-1, 0),
        "SOUTH": (1, 0),
        "EAST": (0, 1),
        "WEST": (0, -1),
    }[dir]

def rotate_left(dir):
    dirs = ["NORTH", "WEST", "SOUTH", "EAST"]
    return dirs[(dirs.index(dir) + 1) % 4]

def rotate_right(dir):
    dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
    return dirs[(dirs.index(dir) + 1) % 4]

def generate_successors(state, world):
    successors = []
    dx, dy = direction_to_delta(state.direction)
    new_pos = (state.pos[0] + dx, state.pos[1] + dy)
    if world.in_bounds(new_pos):
        new_state = State(
            pos=new_pos,
            direction=state.direction,
            has_gold=state.has_gold,
            has_arrow=state.has_arrow,
            cost=state.cost + 1
        )
        successors.append(("FORWARD", new_state))

    successors.append(("TURN_LEFT", State(
        pos=state.pos,
        direction=rotate_left(state.direction),
        has_gold=state.has_gold,
        has_arrow=state.has_arrow,
        cost=state.cost + 1
    )))

    successors.append(("TURN_RIGHT", State(
        pos=state.pos,
        direction=rotate_right(state.direction),
        has_gold=state.has_gold,
        has_arrow=state.has_arrow,
        cost=state.cost + 1
    )))

    if world.is_gold(state.pos) and not state.has_gold:
        successors.append(("GRAB", State(
            pos=state.pos,
            direction=state.direction,
            has_gold=True,
            has_arrow=state.has_arrow,
            cost=state.cost
        )))

    return successors
