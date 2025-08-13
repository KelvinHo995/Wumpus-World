import os
import platform

def clear_console():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def display_step(agent, world):
    clear_console()
    world.print_true_map()
    # === Hiển thị bản đồ
    pos = agent.get_position()
    print("=== WUMPUS WORLD ===")
    for y in reversed(range(world.N)):
        row = ""
        for x in range(world.N):
            if (x, y) == pos:
                row += " A  "
            else:
                row += " .  "
        print(row)

    # === Thông tin Agent hiện tại
    print("\n=== AGENT STATE ===")
    print(f"Position      : {pos}")
    print(f"Facing        : {agent.get_facing()}")

    if agent.step_log:
        last_step = agent.step_log[-1]
        #action_taken = last_step[1]
        action_taken = last_step["action"]
        #result = last_step[2]
        result = last_step["result"]
        #short_result = result.split(" | ")[0]  #Ẩn Percepts để bảng gọn hơn
        #score = last_step[3]
        score = last_step["score"]
        percepts = last_step["percepts"]

        print(f"Action Taken  : {action_taken}")
        #print(f"Result        : {short_result}")
        print(f"Result        : {result}")
        print(f"Current Score : {score}")

        # # Hiển thị Percepts tách riêng
        # if "Percepts:" in result:
        #     percept_part = result.split("Percepts:")[1].strip(" []")
        #     print("\nPercepts:")
        #     for item in percept_part.split(", "):
        #         if ":" in item:
        #             k, v = item.split(":")
        #             print(f" - {k.capitalize()}: {v}")

        print("\nPercepts:")
        for k, v in percepts.items():
            print(f" - {k.capitalize()}: {v}")

    # === Bảng Action Log cập nhật
    print("\n=== ACTION LOG ===")
    print("{:<5} | {:<12} | {:<45} | Score".format("Step", "Action", "Result"))
    print("-" * 80)
    #for step, action, result, score in agent.step_log:
    #    short_result1 = result.split(" | ")[0]  # Ẩn Percepts để bảng gọn hơn

    for entry in agent.step_log:
        step = entry["step"]
        action = entry["action"]
        result = entry["result"]
        score = entry["score"]

        #print(f"{step:<5} | {action:<12} | {short_result1:<45} | {score}")
        print(f"{step:<5} | {action:<12} | {result:<45} | {score}")

    input("\nPress Enter to continue...")
