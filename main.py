from agent import Agent
from world import WumpusWorld
from experiment import run_experiment
from visual import display_step, clear_console
import os

def main():
    clear_console()
    map_size = int(input("Enter map size: "))
    n_wum = int(input("Enter number of Wumpuses: "))
    p_pit = float(input("Enter pit density: "))
    world = WumpusWorld(map_size, n_wum, p_pit)

    inital_KB = world.generate_initial_KB()
    agent = Agent(inital_KB, map_size, n_wum, p_pit)
    rules = agent.parse_rules("rules.json")

    step = 0
    diff = 1
    while agent.is_alive and not (agent.get_position() == (0, 0) and agent.has_gold):
        if diff > 0:
            agent.infer(rules)
        plan = agent.plan()
        if not plan or len(plan) == 0:
            break
        
        pre_KB_len = sum(len(args_set) for pred, args_set in agent.KB.items())

        for action, _ in plan:
            if not agent.is_alive:
                break
            percept = agent.action(action, world, step)
            step += 1
            display_step(agent, world)

            agent_continue = agent.process_percepts(percept)

            if not agent_continue:
                agent.action("grab", world, step)
                step += 1
                display_step(agent, world)
                break

            if agent.get_position() == (0, 0) and agent.has_gold:
                agent.action("climb out", world, step)
                step += 1
                display_step(agent, world)
                break

        post_KB_len = sum(len(args_set) for pred, args_set in agent.KB.items())
        diff = post_KB_len - pre_KB_len

if __name__ == "__main__":
    main()