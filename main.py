from agent import Agent
from world import WumpusWorld
from visual import display_step
from inference import InferenceEngine

def main():
    world = WumpusWorld(N=4, K=0, p=0.2)
    agent = Agent()

    print("\n[1] Hiển thị bản đồ thật (Full Info):")
    world.print_true_map()

    print("\n[2] Start Simulation:")
    # ✅ Generate Initial KB at (0, 0)
    initial_kb = world.generate_initial_KB(agent)
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

    engine = InferenceEngine()
    rules = engine.parse_rules('rules.json')
    deleted = set()

    for i, act in enumerate(actions):
        initial_kb = engine.forward_chaining(rules, initial_kb, deleted)

        print(f"\n>> STEP {i+1}: {act.upper()}")
        percept = agent.action(act, world, i+1)
        #agent.action(act, world, i+1)
        # world.print_agent_map(agent)
        # print("\n[***] Print percept for testing:") # muốn in dòng này thì phải tắt display_step ở dòng dưới
        # print(percept) # muốn in dòng này thì phải tắt display_step ở dòng dưới
        display_step(agent, world)

        if not agent.is_alive:
            break
        
        pos = agent.get_position()
        if percept.breeze:
            initial_kb.add(("Breeze", pos))
        else:
            initial_kb.add(("NotBreeze", pos))

        if percept.stench:
            initial_kb.add(("Stench", pos))
        else:
            initial_kb.add(("NotStench", pos))

        initial_kb.add(("NoPit", pos))
        initial_kb.add(("NoWumpus", pos))
    # print("\n[3] Final Log:")
    # agent.print_log()

if __name__ == "__main__":
    main()
