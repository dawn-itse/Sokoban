def read_map(filepath):
    """
    Đọc file layout, trả về:
    - walls: set các tọa độ (r, c) là tường
    - agent_start: tuple (r, c)
    - boxes_start: frozenset các tọa độ box
    - targets: frozenset các tọa độ đích
    - height, width: kích thước lưới (để in ra sau này)
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
            elif ch == 'C': # C tượng trưng cho cái box đã ở nay target.
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