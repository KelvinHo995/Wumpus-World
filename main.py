from agent import Agent
from world import WumpusWorld
from visual import display_step
import os
def main():
    map_size = int(input("Enter map size: "))
    n_wum = int(input("Enter number of Wumpuses: "))
    p_pit = float(input("Enter pit density: "))
    world = WumpusWorld(N=map_size, K=n_wum, p=p_pit)
    

    print("\n[1] Hiển thị bản đồ thật (Full Info):")

    print("\n[2] Start Simulation:")
    # ✅ Generate Initial KB at (0, 0)
    initial_kb = world.generate_initial_KB()
    print("\n[***] Initial Knowledge Base from (0, 0):")
    # for fact in initial_kb:
    #     print(fact)
    # engine = InferenceEngine()
    # engine.forward_chaining(engine.parse_rules('rules.json'), initial_kb)
    # actions = [
    #     "move forward", "turn left", "move forward",
    #     "grab", "turn right", "move forward",
    #     "move forward", "turn left", "move forward",
    #     "climb out"
    # ]
    actions = [
        # "shoot",      # Bắn mũi tên từ (0,0) → hy vọng trúng (3,0)
        "turn left",
        "move forward",
        "move forward",
        "move forward",
        "turn right",
        "move forward"
    ]

    agent = Agent(initial_kb, map_size, n_wum, p_pit)
    rules = agent.parse_rules('rules.json')

    step = 0
    while agent.is_alive:

        agent.infer(rules)
        plan = agent.plan()

        # if plan is None or len(plan) == 0:
        #     print("The agent infers that it's unable to continue")
        #     break

        # print("gold: ", agent.has_gold)
        # for action, _ in plan:
        #     print(action)
        
        # input("Enter pls\n")
        
        for action, _ in plan:
            if not agent.is_alive:
                break
            percept = agent.action(action, world, step)
            step += 1

            display_step(agent, world)

            if agent.process_percepts(percept) == False:
                agent.action("grab", world, step)
                step += 1
                display_step(agent, world)
                break
                
            if agent.get_position() == (0, 0) and agent.has_gold:
                agent.action("climb out", world, step)
                step += 1
                display_step(agent, world)
                break
        

if __name__ == "__main__":
    main()
