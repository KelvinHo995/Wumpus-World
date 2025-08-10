from agent import Agent
from world import WumpusWorld
from visual import display_step

def main():
    world = WumpusWorld(N=8, K=2, p=0.2)
    agent = Agent()

    print("\n[1] Hiển thị bản đồ thật (Full Info):")
    world.print_true_map()

    print("\n[2] Start Simulation:")
    # actions = [
    #     "move forward", "turn left", "move forward",
    #     "grab", "turn right", "move forward",
    #     "move forward", "turn left", "move forward",
    #     "climb out"
    # ]
    actions = [
        "shoot",      # Bắn mũi tên từ (0,0) → hy vọng trúng (3,0)
        "move forward",
        "move forward",
        "move forward",
        "turn right",
        "move forward"
    ]

    for i, act in enumerate(actions):
        print(f"\n>> STEP {i+1}: {act.upper()}")
        percept = agent.action(act, world, i+1)
        #agent.action(act, world, i+1)
        # world.print_agent_map(agent)
        print("\n[***] Print percept for testing:") # muốn in dòng này thì phải tắt display_step ở dòng dưới
        print(percept) # muốn in dòng này thì phải tắt display_step ở dòng dưới
        display_step(agent, world)
        if not agent.is_alive:
            break

    # print("\n[3] Final Log:")
    # agent.print_log()

if __name__ == "__main__":
    main()
