DIRECTIONS = ['N', 'E', 'S', 'W']  # clockwise

def direction_to_delta(dir):
    return {
        "N": (0, 1),
        "S": (0, -1),
        "E": (1, 0),
        "W": (-1, 0),
    }[dir]