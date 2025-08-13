import json

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)

import os
from world import WumpusWorld
from agent import Agent
from experiment import run_smart_agent

def evaluate_on_testcase(folder_path):
    config_path = os.path.join(folder_path, "config.json")
    config = load_config(config_path)

    import random
    random.seed(config["random_seed"])
    world = WumpusWorld(N=config["map_size"], K=config["num_wumpus"], p=config["pit_probability"])
    initial_kb = world.generate_initial_KB()
    agent = Agent(initial_kb, config["map_size"], config["num_wumpus"], config["pit_probability"])

    run_smart_agent(world, agent, display=False)

    print(f"\n=== Evaluation: {folder_path} ===")
    print(f"Final Score : {agent.score}")
    print(f"Has Gold    : {agent.has_gold}")
    print(f"Alive       : {agent.is_alive}")
    print(f"Steps Taken : {len(agent.step_log)}")
    print(f"Final Position: {agent.get_position()}")
    print(f"Escaped     : {agent.get_position() == (0, 0) and agent.has_gold and agent.is_alive}")
    print("===================================")

def evaluate_all_testcases():
    for i in range(1, 4):
        folder = f"testcases/map{i}"
        evaluate_on_testcase(folder)

if __name__ == "__main__":
    evaluate_all_testcases()