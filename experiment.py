import random
from world import WumpusWorld
from agent import Agent
from visual import display_step

ACTIONS = ["move forward", "turn left", "turn right", "grab", "shoot", "climb out"]

def run_random_agent(world, agent, max_steps=50, display=False):
    step = 0
    while agent.is_alive and step < max_steps:
        action = random.choice(ACTIONS)
        agent.action(action, world, step)
        step += 1

        if display:
            display_step(agent, world)
        
        if agent.get_position() == (0, 0) and agent.has_gold:
            agent.action("climb out", world, step)
            break
        
    return agent.score, agent.has_gold, agent.is_alive

def run_smart_agent(world, agent, display=False):
    rules = agent.parse_rules("rules.json")

    step = 0
    while agent.is_alive and not (agent.get_position() == (0, 0) and agent.has_gold):

        agent.infer(rules)
        plan = agent.plan()
        if not plan or len(plan) == 0:
            break

        for action, _ in plan:
            if not agent.is_alive:
                break
            percept = agent.action(action, world, step)
            step += 1
            if display:
                display_step(agent, world)

            if not agent.process_percepts(percept):
                agent.action("grab", world, step)
                step += 1
                if display:
                    display_step(agent, world)
                break

            if agent.get_position() == (0, 0) and agent.has_gold:
                agent.action("climb out", world, step)
                step += 1
                if display:
                    display_step(agent, world)
                break

def run_experiment(map_size=8, n_wumpus=2, p_pit=0.2, num_trials=100, max_steps=50, verbose=False):
    def build_world():
        return WumpusWorld(N=map_size, K=n_wumpus, p=p_pit)

    def build_random_agent(initial_kb):
        return Agent(initial_kb, map_size, n_wumpus, p_pit)

    def build_smart_agent(initial_kb):
        return Agent(initial_kb, map_size, n_wumpus, p_pit)

    def run_and_log(agent_type, worlds):
        results = []

        for world in worlds:
            world.print_true_map()
            initial_kb = world.generate_initial_KB()

            if agent_type == "random":
                agent = build_random_agent(initial_kb)
                run_random_agent(world, agent, max_steps=max_steps, display=verbose)
            elif agent_type == "smart":
                agent = build_smart_agent(initial_kb)
                run_smart_agent(world, agent, display=verbose)

            results.append({
                "agent_type": agent_type,
                "success": agent.has_gold and agent.is_alive,
                "has_gold": agent.has_gold,
                "is_alive": agent.is_alive,
                "final_score": agent.score,
                "steps": len(agent.step_log)
            })

        return results

    #Chạy cả 2 agent

    worlds = [build_world() for i in range(num_trials)]
    print("\n[Running Smart Agent Trials...]")
    smart_results = run_and_log("smart", worlds)
    summarize_results(smart_results)

    print("\n[Running Random Agent Trials...]")
    random_results = run_and_log("random", worlds)
    summarize_results(random_results)

    return smart_results, random_results


def compute_success_rate(results):
    return sum(r["success"] for r in results) / len(results)

def compute_death_rate(results):
    return sum(not r["is_alive"] for r in results) / len(results)

def compute_gold_collected_rate(results):
    return sum(r["has_gold"] for r in results) / len(results)

import statistics
def compute_score_stats(results):
    scores = [r["final_score"] for r in results]
    return statistics.mean(scores), statistics.stdev(scores)

def compute_step_stats(results):
    steps = [r["steps"] for r in results]
    return statistics.mean(steps), statistics.stdev(steps)

def summarize_results(results):
    success_rate = compute_success_rate(results)
    death_rate = compute_death_rate(results)
    gold_rate = compute_gold_collected_rate(results)
    avg_score, std_score = compute_score_stats(results)
    avg_steps, std_steps = compute_step_stats(results)

    print("=== Evaluation Summary ===")
    print(f"Total Runs           : {len(results)}")
    print(f"Success Rate         : {success_rate:.2%}")
    print(f"Death Rate           : {death_rate:.2%}")
    print(f"Gold Collected Rate  : {gold_rate:.2%}")
    print(f"Average Score        : {avg_score:.2f}")
    print(f"Score Std Deviation  : {std_score:.2f}")
    print(f"Average Steps        : {avg_steps:.2f}")
    print(f"Steps Std Deviation  : {std_steps:.2f}")
