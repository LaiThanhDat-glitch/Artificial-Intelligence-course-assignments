import time
from simpleai.search import (
    SearchProblem,
    breadth_first,
    uniform_cost,
    depth_first,
    limited_depth_first,
    greedy,
    astar
)

# 1. Biểu diễn trạng thái dưới dạng chuỗi (String) 9 ký tự
# Hàng 1: 2 1 0 | Hàng 2: 3 4 5 | Hàng 3: 7 8 6
INITIAL_STR = "210345786"

# Hàng 1: 1 2 3 | Hàng 2: 8 0 4 | Hàng 3: 7 6 5
GOAL_STR    = "123804765"

# Bảng các bước di chuyển hợp lệ tương ứng với từng vị trí index (0 đến 8) của ô trống '0'
MOVES = {
    0: [('DOWN', 3), ('RIGHT', 1)],
    1: [('LEFT', 0), ('DOWN', 4), ('RIGHT', 2)],
    2: [('LEFT', 1), ('DOWN', 5)],
    3: [('UP', 0), ('DOWN', 6), ('RIGHT', 4)],
    4: [('UP', 1), ('LEFT', 3), ('DOWN', 7), ('RIGHT', 5)],
    5: [('UP', 2), ('LEFT', 4), ('DOWN', 8)],
    6: [('UP', 3), ('RIGHT', 7)],
    7: [('UP', 4), ('LEFT', 6), ('RIGHT', 8)],
    8: [('UP', 5), ('LEFT', 7)]
}

# Tiền tính toán tọa độ đích của từng số để tra cứu Manhattan không cần tính toán lại
GOAL_COORDS = {val: (i // 3, i % 3) for i, val in enumerate(GOAL_STR)}

# Bảng tra cứu trước khoảng cách Manhattan: MANHATTAN_TABLE[kí_tự][vị_trí_index]
MANHATTAN_TABLE = {}
for ch in "12345678":
    gr, gc = GOAL_COORDS[ch]
    MANHATTAN_TABLE[ch] = [abs(idx // 3 - gr) + abs(idx % 3 - gc) for idx in range(9)]


# 2. Định nghĩa lớp bài toán kế thừa SearchProblem
class FastEightPuzzle(SearchProblem):
    def __init__(self, initial_state=INITIAL_STR, heuristic_type='h2'):
        super().__init__(initial_state=initial_state)
        self.heuristic_type = heuristic_type

    def actions(self, state):
        zero_idx = state.index('0')
        return [act for act, _ in MOVES[zero_idx]]

    def result(self, state, action):
        zero_idx = state.index('0')
        target_idx = -1
        for act, dest in MOVES[zero_idx]:
            if act == action:
                target_idx = dest
                break

        # Hoán đổi 2 ký tự trong chuỗi
        chars = list(state)
        chars[zero_idx], chars[target_idx] = chars[target_idx], chars[zero_idx]
        return "".join(chars)

    def is_goal(self, state):
        return state == GOAL_STR

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        if self.heuristic_type == 'h1':
            # h1: Số ô sai vị trí so với trạng thái đích
            return sum(1 for i in range(9) if state[i] != '0' and state[i] != GOAL_STR[i])
        else:
            # h2: Tổng khoảng cách Manhattan tra nhanh từ bảng
            return sum(MANHATTAN_TABLE[ch][i] for i, ch in enumerate(state) if ch != '0')


# 3. Hàm chạy thuật toán IDS có chặn độ sâu lặp tối đa
def run_ids(problem, max_depth=8):
    for depth in range(max_depth + 1):
        res = limited_depth_first(problem, depth_limit=depth, graph_search=True)
        if res is not None:
            return res
    return None


# 4. Hàm đo thời gian và in kết quả một dòng
def execute_and_measure(name, func, problem):
    t_start = time.perf_counter()
    res = func(problem)
    t_elapsed = (time.perf_counter() - t_start) * 1000  # đơn vị milliseconds (ms)

    if res:
        steps_str = f"{res.cost} bước"
    else:
        steps_str = "Không tìm thấy"

    print(f"{name:<42} | {steps_str:<16} | {t_elapsed:>9.2f} ms")


# In ma trận hiển thị trực quan
def print_grid_str(s):
    for i in range(0, 9, 3):
        print("  " + " ".join(s[i+j] if s[i+j] != '0' else "_" for j in range(3)))
    print()


# 5. Khối điều khiển chính
if __name__ == '__main__':
    print("Trạng thái bắt đầu:")
    print_grid_str(INITIAL_STR)
    print("Trạng thái đích:")
    print_grid_str(GOAL_STR)

    prob_default = FastEightPuzzle(heuristic_type='h2')
    prob_h1 = FastEightPuzzle(heuristic_type='h1')
    prob_h2 = FastEightPuzzle(heuristic_type='h2')

    print("=" * 73)
    print(f"{'Thuật toán':<42} | {'Kết quả':<16} | {'Thời gian':>12}")
    print("=" * 73)

    # --- Nhóm 5 thuật toán cơ bản (Uninformed Search) ---
    execute_and_measure("1. BFS", lambda p: breadth_first(p, graph_search=True), prob_default)
    execute_and_measure("2. UCS", lambda p: uniform_cost(p, graph_search=True), prob_default)
    execute_and_measure("3. DFS", lambda p: depth_first(p, graph_search=True), prob_default)
    execute_and_measure("4. DLS (limit=100)", lambda p: limited_depth_first(p, depth_limit=100, graph_search=True), prob_default)
    execute_and_measure("5. IDS (limit=100)", lambda p: run_ids(p, max_depth=100), prob_default)

    print("-" * 73)
    # --- Nhóm 2 thuật toán Heuristic (Greedy & A*) với h1 và h2 ---
    execute_and_measure("6. Greedy (h1: Misplaced)", lambda p: greedy(p, graph_search=True), prob_h1)
    execute_and_measure("6. Greedy (h2: Manhattan)", lambda p: greedy(p, graph_search=True), prob_h2)
    execute_and_measure("7. A* (h1: Misplaced)", lambda p: astar(p, graph_search=True), prob_h1)
    execute_and_measure("7. A* (h2: Manhattan)", lambda p: astar(p, graph_search=True), prob_h2)
    print("=" * 73)