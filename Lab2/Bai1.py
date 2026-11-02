import heapq
from collections import deque

# Biểu diễn đồ thị Rumani (Slide 6)
# Mỗi cạnh gồm: (đỉnh kề, chi phí bước)
ROMANIA_MAP = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Pitesti', 97), ('Craiova', 146)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Dobreta', 75)],
    'Dobreta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Dobreta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucharest', 90)],
    'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)]
}

# -------------------------------------------------------------
# 1. BREADTH-FIRST SEARCH (BFS) - Cài đặt theo Graph Search (Slide 31, 32, 63)
# Fringe: Hàng đợi FIFO (deque)
# -------------------------------------------------------------
def bfs(graph, start, goal):
    fringe = deque([(start, [start], 0)])  # (nút hiện tại, đường đi, tổng chi phí)
    closed = set()

    while fringe:
        node, path, cost = fringe.popleft()
        if node == goal:
            return path, cost

        if node not in closed:
            closed.add(node)
            for neighbor, step_cost in graph.get(node, []):
                if neighbor not in closed:
                    fringe.append((neighbor, path + [neighbor], cost + step_cost))
    return None, float('inf')


# -------------------------------------------------------------
# 2. UNIFORM-COST SEARCH (UCS) (Slide 38, 39, 40)
# Fringe: Hàng đợi ưu tiên (Priority Queue - Min Heap)
# -------------------------------------------------------------
def ucs(graph, start, goal):
    # (tổng chi phí g, nút hiện tại, đường đi)
    fringe = [(0, start, [start])]
    closed = set()

    while fringe:
        cost, node, path = heapq.heappop(fringe)
        if node == goal:
            return path, cost

        if node not in closed:
            closed.add(node)
            for neighbor, step_cost in graph.get(node, []):
                if neighbor not in closed:
                    heapq.heappush(fringe, (cost + step_cost, neighbor, path + [neighbor]))
    return None, float('inf')


# -------------------------------------------------------------
# 3. DEPTH-FIRST SEARCH (DFS) (Slide 41, 42, 63)
# Fringe: Ngăn xếp LIFO
# -------------------------------------------------------------
def dfs(graph, start, goal):
    fringe = [(start, [start], 0)]  # LIFO stack
    closed = set()

    while fringe:
        node, path, cost = fringe.pop()
        if node == goal:
            return path, cost

        if node not in closed:
            closed.add(node)
            # Đảo ngược thứ tự duyệt để duyệt các nhánh theo thứ tự trực quan
            for neighbor, step_cost in reversed(graph.get(node, [])):
                if neighbor not in closed:
                    fringe.append((neighbor, path + [neighbor], cost + step_cost))
    return None, float('inf')


# -------------------------------------------------------------
# 4. DEPTH-LIMITED SEARCH (DLS) (Slide 50, 51)
# Đệ quy với cờ cắt tỉa (cutoff)
# -------------------------------------------------------------
def recursive_dls(node, goal, limit, path, current_cost, graph, visited_on_path):
    if node == goal:
        return path, current_cost

    if limit == 0:
        return "cutoff", None

    cutoff_occurred = False
    for neighbor, step_cost in graph.get(node, []):
        if neighbor not in visited_on_path:  # Tránh chu trình trên nhánh đang xét
            visited_on_path.add(neighbor)
            result, cost = recursive_dls(
                neighbor, goal, limit - 1, 
                path + [neighbor], current_cost + step_cost, 
                graph, visited_on_path
            )
            visited_on_path.remove(neighbor)

            if result == "cutoff":
                cutoff_occurred = True
            elif result != "failure":
                return result, cost

    return ("cutoff", None) if cutoff_occurred else ("failure", None)

def dls(graph, start, goal, limit):
    return recursive_dls(start, goal, limit, [start], 0, graph, {start})


# -------------------------------------------------------------
# 5. ITERATIVE DEEPENING SEARCH (IDS) (Slide 52, 53, 58)
# Tăng dần giới hạn l từ 0 cho đến khi tìm thấy đích
# -------------------------------------------------------------
def ids(graph, start, goal, max_depth=50):
    for depth in range(max_depth):
        result, cost = dls(graph, start, goal, depth)
        if result != "cutoff" and result != "failure":
            return result, cost, depth
    return None, float('inf'), max_depth


# =============================================================
# THỰC THI & KIỂM TRA
# =============================================================
if __name__ == '__main__':
    start_city = 'Arad'
    goal_city = 'Bucharest'

    print("=== SO SÁNH KẾT QUẢ 5 THUẬT TOÁN (TỪ ARAD ĐẾN BUCHAREST) ===\n")

    # 1. BFS
    path, cost = bfs(ROMANIA_MAP, start_city, goal_city)
    print(f"[1] BFS : Đường đi = {' -> '.join(path)} | Chi phí = {cost}")

    # 2. UCS
    path, cost = ucs(ROMANIA_MAP, start_city, goal_city)
    print(f"[2] UCS : Đường đi = {' -> '.join(path)} | Chi phí = {cost}")

    # 3. DFS
    path, cost = dfs(ROMANIA_MAP, start_city, goal_city)
    print(f"[3] DFS : Đường đi = {' -> '.join(path)} | Chi phí = {cost}")

    # 4. DLS (Thử nghiệm với limit = 3)
    path, cost = dls(ROMANIA_MAP, start_city, goal_city, limit=3)
    print(f"[4] DLS (limit=3): Đường đi = {path} | Chi phí = {cost}")

    # 5. IDS
    path, cost, depth_found = ids(ROMANIA_MAP, start_city, goal_city)
    print(f"[5] IDS : Đường đi = {' -> '.join(path)} | Chi phí = {cost} (Tìm thấy tại độ sâu l = {depth_found})")