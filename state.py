class State:
    def __init__(self, pos, direction, has_gold, has_arrow, is_alive, visited, cost):
        self.pos = pos
        self.direction = direction
        self.has_gold = has_gold
        self.has_arrow = has_arrow
        self.is_alive = is_alive
        self.visited = visited
        self.cost = cost

    def __hash__(self):
        return hash((self.pos, self.direction, self.has_gold, self.has_arrow, self.is_alive))

    def __eq__(self, other):
        return (
            self.pos == other.pos and
            self.direction == other.direction and
            self.has_gold == other.has_gold and
            self.has_arrow == other.has_arrow and
            self.is_alive == other.is_alive
        )

    def __lt__(self, other):
        # So sánh đơn giản: so sánh theo cost để tránh lỗi heap
        return self.cost < other.cost
