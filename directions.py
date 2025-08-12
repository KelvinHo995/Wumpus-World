DIRECTIONS = ['N', 'E', 'S', 'W']  # clockwise

def direction_to_delta(dir):
    return {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1),
    }[dir]