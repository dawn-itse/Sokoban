def read_map(filepath):
    """
    Đọc file layout, trả về:
    - walls: set các tọa độ (r, c) là tường
    - agent_start: tuple (r, c)
    - boxes_start: frozenset các tọa độ box
    - targets: frozenset các tọa độ đích
    - height, width: kích thước lưới
    """
    walls = set()
    boxes_start = set()
    targets = set()
    agent_start = None

    with open(filepath, "r") as f:
        lines = f.readlines()

    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == '%':
                walls.add((r, c))
            elif ch == 'A':
                agent_start = (r, c)
            elif ch == 'B':
                boxes_start.add((r, c))
            elif ch == 'D':
                targets.add((r, c))
            elif ch == 'C':
                boxes_start.add((r, c))
                targets.add((r, c))

    height = len(lines)
    width = max(len(line) for line in lines)

    return {
        "walls": frozenset(walls),
        "agent_start": agent_start,
        "boxes_start": frozenset(boxes_start),
        "targets": frozenset(targets),
        "height": height,
        "width": width,
    }


def is_goal(state, targets):
    """Kiểm tra state hiện tại đã là trạng thái đích chưa."""
    agent_pos, box_positions = state
    return box_positions == targets


def get_successors(state, walls):
    """
    Nhận vào 1 state (agent_pos, box_positions) và tập walls.
    Trả về list các (action, new_state) hợp lệ.
    """
    agent_pos, box_positions = state

    directions = {
        "North": (-1, 0),
        "South": (1, 0),
        "West":  (0, -1),
        "East":  (0, 1),
    }

    successors = []

    for action, (dr, dc) in directions.items():
        new_agent_r = agent_pos[0] + dr
        new_agent_c = agent_pos[1] + dc
        new_agent_pos = (new_agent_r, new_agent_c)

        if new_agent_pos in walls:
            continue

        if new_agent_pos in box_positions:
            new_box_r = new_agent_r + dr
            new_box_c = new_agent_c + dc
            new_box_pos = (new_box_r, new_box_c)

            if new_box_pos in walls or new_box_pos in box_positions:
                continue

            new_box_positions = (box_positions - {new_agent_pos}) | {new_box_pos}
            new_state = (new_agent_pos, new_box_positions)
            successors.append((action, new_state))
        else:
            new_state = (new_agent_pos, box_positions)
            successors.append((action, new_state))

    return successors


# ------------------- Khu vực tự kiểm tra (test) -------------------
if __name__ == "__main__":
    # Dữ liệu map giả lập nhỏ để test nhanh, không cần đọc file thật
    map_data = {
        "walls": frozenset({(0, 0), (0, 2), (2, 0), (2, 1), (2, 2)}),
        "agent_start": (0, 1),
        "boxes_start": frozenset({(1, 2)}),
        "targets": frozenset({(1, 0)}),
    }

    initial_state = (map_data["agent_start"], map_data["boxes_start"])
    print("State ban đầu:", initial_state)

    print("Đã là goal chưa?", is_goal(initial_state, map_data["targets"]))

    print("\nCác bước đi hợp lệ từ state ban đầu:")
    for action, new_state in get_successors(initial_state, map_data["walls"]):
        print(f"  {action} -> {new_state}")

    # Test đọc file thật khi bạn đã có example_map.txt
    # real_map = read_map("example_map.txt")
    # print(real_map)