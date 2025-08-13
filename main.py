from agent import Agent
from world import WumpusWorld
from experiment import run_experiment
import os
def main():
    map_size = int(input("Enter map size: "))
    n_wum = int(input("Enter number of Wumpuses: "))
    p_pit = float(input("Enter pit density: "))
    num_trials = 2
    run_experiment(map_size, n_wum, p_pit, num_trials, max_steps=50, verbose=False)

    # #print("\n[1] Hiển thị bản đồ thật (Full Info):")
    
    # #print("\n[2] Start Simulation:")

    # #print("\n[***] Initial Knowledge Base from (0, 0):")

    # actions = [
    #     # "shoot",      # Bắn mũi tên từ (0,0) → hy vọng trúng (3,0)
    #     "turn left",
    #     "move forward",
    #     "move forward",
    #     "move forward",
    #     "turn right",
    #     "move forward"
    # ]

if __name__ == "__main__":
    main()
