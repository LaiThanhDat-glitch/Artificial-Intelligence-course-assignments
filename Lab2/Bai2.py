from simpleai.search import (
    SearchProblem,
    breadth_first,
    uniform_cost,
    depth_first,
    limited_depth_first,
    iterative_limited_depth_first
)

# 1. Dữ liệu bản đồ Rumani theo slide (Slide 6)
COSTS = {
    ('Arad', 'Zerind'): 75, ('Arad', 'Sibiu'): 140, ('Arad', 'Timisoara'): 118,
    ('Zerind', 'Oradea'): 71,
    ('Oradea', 'Sibiu'): 151,
    ('Sibiu', 'Fagaras'): 99, ('Sibiu', 'Rimnicu Vilcea'): 80,
    ('Fagaras', 'Bucharest'): 211,
    ('Rimnicu Vilcea', 'Pitesti'): 97, ('Rimnicu Vilcea', 'Craiova'): 146,
    ('Pitesti', 'Craiova'): 138, ('Pitesti', 'Bucharest'): 101,
    ('Timisoara', 'Lugoj'): 111,
    ('Lugoj', 'Mehadia'): 70,
    ('Mehadia', 'Dobreta'): 75,
    ('Dobreta', 'Craiova'): 120,
    ('Bucharest', 'Giurgiu'): 90, ('Bucharest', 'Urziceni'): 85,
    ('Urziceni', 'Hirsova'): 98, ('Urziceni', 'Vaslui'): 142,
    ('Hirsova', 'Eforie'): 86,
    ('Vaslui', 'Iasi'): 92,
    ('Iasi', 'Neamt'): 87
}

# Tạo đồ thị 2 chiều
GRAPH = {}
for (c1, c2), cost in list(COSTS.items()):
    GRAPH.setdefault(c1, {})[c2] = cost
    GRAPH.setdefault(c2, {})[c1] = cost


# 2. Định nghĩa SearchProblem
class RomaniaProblem(SearchProblem):
    def __init__(self, initial_state='Arad', goal_state='Bucharest'):
        super().__init__(initial_state=initial_state)
        self.goal_state = goal_state

    # Các hành động có thể: đi tới thành phố lân cận
    def actions(self, state):
        return list(GRAPH.get(state, {}).keys())

    # Kết quả của hành động là thành phố đích đến
    def result(self, state, action):
        return action

    # Kiểm tra đạt trạng thái đích chưa
    def is_goal(self, state):
        return state == self.goal_state

    # Chi phí bước c(x, a, y)
    def cost(self, state, action, state2):
        return GRAPH[state][state2]


# 3. Chạy thử nghiệm 5 thuật toán có sẵn của SimpleAI
if __name__ == '__main__':
    problem = RomaniaProblem(initial_state='Arad', goal_state='Bucharest')

    # Danh sách các hàm tìm kiếm có sẵn
    algorithms = [
        ("Breadth-First Search (BFS)", lambda prob: breadth_first(prob, graph_search=True)),
        ("Uniform-Cost Search (UCS)", lambda prob: uniform_cost(prob, graph_search=True)),
        ("Depth-First Search (DFS)", lambda prob: depth_first(prob, graph_search=True)),
        ("Depth-Limited Search (DLS, limit=3)", lambda prob: limited_depth_first(prob, depth_limit=3, graph_search=True)),
        ("Iterative Deepening Search (IDS)", lambda prob: iterative_limited_depth_first(prob, graph_search=True))
    ]

    print("===== KẾT QUẢ CHẠY BẰNG SIMPLEAI =====\n")
    for name, run_algo in algorithms:
        result = run_algo(problem)
        if result:
            # result.path() trả về danh sách các cặp (action, state)
            path = [state for _, state in result.path()]
            print(f"[{name}]")
            print(f" - Đường đi: {' -> '.join(path)}")
            print(f" - Tổng chi phí: {result.cost}\n")
        else:
            print(f"[{name}]")
            print(" - Không tìm thấy đường đi (Cutoff hoặc No solution)\n")