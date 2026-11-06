import random

def fitness(chromosome):
    """
    Tính số cặp hậu KHÔNG tấn công lẫn nhau.
    Với bàn cờ N quân, tổng số cặp là N*(N-1)//2.
    Fitness cực đại = N*(N-1)//2 (nghĩa là 0 xung đột).
    """
    n = len(chromosome)
    clashes = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Kiểm tra cùng hàng hoặc cùng đường chéo
            if chromosome[i] == chromosome[j] or abs(chromosome[i] - chromosome[j]) == abs(i - j):
                clashes += 1
    max_non_attacking = n * (n - 1) // 2
    return max_non_attacking - clashes

def init_population(pop_size, n):
    """Khởi tạo quần thể với các cấu hình hoán vị để tránh trùng hàng ngay từ đầu."""
    return [random.sample(range(n), n) for _ in range(pop_size)]

def selection(population, fitnesses):
    """Chọn lọc theo Tournament Selection (k=3)."""
    tournament = random.sample(list(zip(population, fitnesses)), 3)
    tournament.sort(key=lambda x: x[1], reverse=True)
    return tournament[0][0]

def order_crossover(parent1, parent2):
    """Order Crossover (OX1) bảo toàn tính hoán vị của cá thể."""
    n = len(parent1)
    a, b = sorted(random.sample(range(n), 2))
    child = [-1] * n
    
    # Sao chép đoạn gen giữa
    child[a:b+1] = parent1[a:b+1]
    
    # Điền phần còn lại từ parent2 theo thứ tự vòng tròn
    p2_idx = (b + 1) % n
    c_idx = (b + 1) % n
    while -1 in child:
        val = parent2[p2_idx]
        if val not in child:
            child[c_idx] = val
            c_idx = (c_idx + 1) % n
        p2_idx = (p2_idx + 1) % n
    return child

def mutate_swap(chromosome, mutation_rate=0.2):
    """Đột biến tráo đổi (Swap Mutation) vị trí 2 quân hậu."""
    mutant = chromosome[:]
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(chromosome)), 2)
        mutant[i], mutant[j] = mutant[j], mutant[i]
    return mutant

def print_board(solution):
    n = len(solution)
    for r in range(n):
        line = ["Q " if solution[c] == r else ". " for c in range(n)]
        print("".join(line))
    print("-" * (2 * n))

def solve_n_queens_ga(n=8, pop_size=100, max_generations=1000, mutation_rate=0.2):
    max_fitness = n * (n - 1) // 2
    pop = init_population(pop_size, n)
    
    for gen in range(max_generations):
        fits = [fitness(ind) for ind in pop]
        best_fit = max(fits)
        best_ind = pop[fits.index(best_fit)]
        
        if best_fit == max_fitness:
            print(f" Tìm thấy lời giải ở thế hệ {gen}!")
            print(f"Cấu hình (cột -> hàng): {best_ind}")
            print_board(best_ind)
            return best_ind
            
        new_pop = [best_ind]  # Elitism: giữ lại cá thể tốt nhất
        while len(new_pop) < pop_size:
            p1 = selection(pop, fits)
            p2 = selection(pop, fits)
            child = order_crossover(p1, p2)
            child = mutate_swap(child, mutation_rate)
            new_pop.append(child)
        pop = new_pop
        
    print(" Không tìm thấy nghiệm tối ưu trong số thế hệ giới hạn.")
    return None

if __name__ == "__main__":
    print("=== BÀI 1: N-QUEENS BẰNG GA (N = 8) ===")
    solve_n_queens_ga(n=8)