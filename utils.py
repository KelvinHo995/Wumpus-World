def get_adjacent(i, j, size):
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    neighbors = []
    for di, dj in directions:
        ni, nj = i+di, j+dj
        if 0 <= ni < size[0] and 0 <= nj < size[1]:
            neighbors.append((ni, nj))
    return neighbors
