from agent import Agent
from world import WumpusWorld
from visual import display_step

def main():
    map_size = 4
    n_wum = 1
    p_pit = 0.2
    world = WumpusWorld(N=map_size, K=n_wum, p=p_pit)
    

    print("\n[1] Hiển thị bản đồ thật (Full Info):")
    world.print_true_map()

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

    # for i, act in enumerate(actions):
    #     # initial_kb = engine.forward_chaining(rules, initial_kb, deleted)
    #     initial_kb = agent.infer(rules)
    #     print(f"\n>> STEP {i+1}: {act.upper()}")
    #     percept = agent.action(act, world, i+1)
    #     agent.process_percepts(percept)
    #     #agent.action(act, world, i+1)
    #     # world.print_agent_map(agent)
    #     # print("\n[***] Print percept for testing:") # muốn in dòng này thì phải tắt display_step ở dòng dưới
    #     # print(percept) # muốn in dòng này thì phải tắt display_step ở dòng dưới
    #     display_step(agent, world)

    #     if not agent.is_alive:
    #         break
    
    step = 0
    while agent.is_alive:
        agent.infer(rules)
        plan = agent.plan()

        for action in plan:
            percept = agent.action(action, world, step)
            step += 1

            display_step(agent, world)
            if agent.process_percepts(percept) == False:
                agent.action("grab", world, step)
                step += 1
                display_step(agent, world)
                break
        

if __name__ == "__main__":
    main()
