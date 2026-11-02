from simpleai.search import (
    SearchProblem,
    breadth_first,
    uniform_cost,
    depth_first,
    limited_depth_first,
    iterative_limited_depth_first,
    greedy,
    astar
)

# 1. Định nghĩa trạng thái Initial và Goal dưới dạng tuple của tuple (để hashable trong set/dict của SimpleAI)
INITIAL_STATE = (
    (2, 1, 0),
    (3, 4, 5),
    (7, 8, 6)
)

GOAL_STATE = (
    (1, 2, 3),
    (8, 0, 4),
    (7, 6, 5)
)

# Bảng tra cứu tọa độ đích (r, c) của từng số để tính nhanh Manhattan Distance
GOAL_POSITIONS = {}
for r in range(3):
    for c in range(3):
        val = GOAL_STATE[r][c]
        if val != 0:
            GOAL_POSITIONS[val] = (r, c)


class EightPuzzleProblem(SearchProblem):
    def __init__(self, initial_state=INITIAL_STATE, heuristic_type='h2'):
        super().__init__(initial_state=initial_state)
        self.heuristic_type = heuristic_type

    # Tìm vị trí ô trống (giá trị 0)
    def _find_blank(self, state):
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    return r, c

    # Các hành động có thể di chuyển ô trống: UP, DOWN, LEFT, RIGHT
    def actions(self, state):
        r, c = self._find_blank(state)
        valid_actions = []
        if r > 0: valid_actions.append('UP')
        if r < 2: valid_actions.append('DOWN')
        if c > 0: valid_actions.append('LEFT')
        if c < 2: valid_actions.append('RIGHT')
        return valid_actions

    # Trả về ma trận mới sau khi di chuyển ô trống
    def result(self, state, action):
        r, c = self._find_blank(state)
        grid = [list(row) for row in state]

        dr, dc = 0, 0
        if action == 'UP':      dr = -1
        elif action == 'DOWN':  dr = 1
        elif action == 'LEFT':  dc = -1
        elif action == 'RIGHT': dc = 1

        nr, nc = r + dr, c + dc
        # Hoán đổi ô trống với ô kề
        grid[r][c], grid[nr][nc] = grid[nr][nc], grid[r][c]
        return tuple(tuple(row) for row in grid)

    def is_goal(self, state):
        return state == GOAL_STATE

    def cost(self, state, action, state2):
        return 1

    # Hàm Heuristic h1: Số ô đặt sai vị trí
    def heuristic_h1(self, state):
        misplaced = 0
        for r in range(3):
            for c in range(3):
                val = state[r][c]
                if val != 0 and val != GOAL_STATE[r][c]:
                    misplaced += 1
        return misplaced

    # Hàm Heuristic h2: Tổng khoảng cách Manhattan |x - x*| + |y - y*|
    def heuristic_h2(self, state):
        dist = 0
        for r in range(3):
            for c in range(3):
                val = state[r][c]
                if val != 0:
                    gr, gc = GOAL_POSITIONS[val]
                    dist += abs(r - gr) + abs(c - gc)
        return dist

    # SimpleAI sẽ tự động gọi phương thức heuristic(self, state)
    def heuristic(self, state):
        if self.heuristic_type == 'h1':
            return self.heuristic_h1(state)
        return self.heuristic_h2(state)


# In trạng thái ma trận ra màn hình
def print_grid(state):
    for row in state:
        print("  " + " ".join(str(x) if x != 0 else "_" for x in row))
    print()

# Hàm tự bọc IDS có giới hạn độ sâu (depth_limit) để tránh treo máy
def run_ids(problem, max_depth=8):
    for depth in range(max_depth + 1):
        result = limited_depth_first(problem, depth_limit=depth, graph_search=True)
        if result is not None:
            return result
    return None

if __name__ == '__main__':
    print("Trạng thái bắt đầu:")
    print_grid(INITIAL_STATE)
    print("Trạng thái đích:")
    print_grid(GOAL_STATE)

    # 1. Nhóm 5 thuật toán cơ bản (Uninformed Search)
    base_problem = EightPuzzleProblem(heuristic_type='h2')

    print("=================== 5 THUẬT TOÁN CƠ BẢN ===================")
    # Với DLS, giới hạn độ sâu được đặt là 6 để quan sát hành vi cắt tỉa
    algos_uninformed = [
        ("1. Breadth-First Search (BFS)", lambda p: breadth_first(p, graph_search=True)),
        ("2. Uniform-Cost Search (UCS)", lambda p: uniform_cost(p, graph_search=True)),
        ("3. Depth-First Search (DFS)", lambda p: depth_first(p, graph_search=True)),
        ("4. Depth-Limited Search (DLS, limit=6)", lambda p: limited_depth_first(p, depth_limit=6, graph_search=True)),
        ("5. Iterative Deepening Search (IDS, limit=8)", lambda p: run_ids(p, max_depth=8))
    ]

    for name, run_algo in algos_uninformed:
        print(f"\n--- Đang chạy: {name} ---")
        try:
            res = run_algo(base_problem)
            if res:
                print(f"-> Số bước: {res.cost}")
                print(f"-> Chuỗi hành động: {res.path()}")
            else:
                print("-> Không tìm thấy nghiệm (Cutoff / No Solution)")
        except RecursionError:
            print("-> Lỗi vượt giới hạn đệ quy bộ nhớ.")

    # 2. Nhóm 2 thuật toán tìm kiếm có thông tin (Heuristic: h1 & h2)
    print("\n=================== 2 THUẬT TOÁN HEURISTIC ===================")
    
    # Chạy h2 trước (Manhattan mạnh hơn rất nhiều so với h1, ra kết quả nhanh hơn)
    for h_type in ['h2', 'h1']:
        h_desc = "Khoảng cách Manhattan (h2)" if h_type == 'h2' else "Sai vị trí (h1)"
        prob = EightPuzzleProblem(heuristic_type=h_type)
        
        # 6. Greedy Best-First Search
        print(f"\n[6. Greedy Best-First Search] Sử dụng Heuristic: {h_desc}")
        print("  -> Đang tìm kiếm...")
        res_greedy = greedy(prob, graph_search=True)
        if res_greedy:
            print(f"  -> Hoàn thành! Số bước: {res_greedy.cost}")
            actions = [act for act, _ in res_greedy.path() if act]
            print(f"  -> Các bước di chuyển: {' -> '.join(actions)}")
        else:
            print("  -> Không tìm thấy lời giải.")
        
        # 7. A* Search
        print(f"\n[7. A* Search] Sử dụng Heuristic: {h_desc}")
        print("  -> Đang tìm kiếm...")
        res_astar = astar(prob, graph_search=True)
        if res_astar:
            print(f"  -> Hoàn thành! Số bước tối ưu: {res_astar.cost}")
            actions = [act for act, _ in res_astar.path() if act]
            print(f"  -> Các bước di chuyển: {' -> '.join(actions)}")
        else:
            print("  -> Không tìm thấy lời giải.")