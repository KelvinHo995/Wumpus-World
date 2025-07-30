from world import World
from safe_agent import SafeAStarAgent
from risky_agent import RiskyAStarAgent

world = World()
world.load_map("map.txt")

start_pos = world.agent_pos
percepts = []

# Sinh percept 
for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    ni, nj = start_pos[0] + dx, start_pos[1] + dy
    if not world.in_bounds((ni, nj)):
        continue
    if (ni, nj) in world.pits:
        percepts.append("Breeze")
    if (ni, nj) in world.wumpus:
        percepts.append("Stench")

world.update_percepts(percepts, start_pos)

# In ra tập các ô an toàn và nguy hiểm (debug)
print("Confirmed Safe:", world.confirmed_safe)
print("Confirmed Dangers:", world.confirmed_dangers)

print("\n=== SAFE A* ===")
safe_agent = SafeAStarAgent(world)
safe_path = safe_agent.solve()

if safe_path:
    for step in safe_path:
        print(f"{step[0]} -> {step[1]}")
else:
    print("No safe path found.")

print("\n=== RISKY A* ===")
risky_agent = RiskyAStarAgent(world)
risky_path = risky_agent.solve()

if risky_path:
    for step in risky_path:
        print(f"{step[0]} -> {step[1]}")
else:
    print("No risky path found.")
