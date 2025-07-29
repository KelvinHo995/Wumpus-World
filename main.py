from world import WumpusWorld
from a_star_function import AStarAgent

if __name__ == "__main__":
    world = WumpusWorld("maps/map1.txt")
    agent = AStarAgent(world)
    path = agent.solve()

    if path:
        print("Path found:")
        for step in path:
            print(step)
    else:
        print("No safe path found.")
