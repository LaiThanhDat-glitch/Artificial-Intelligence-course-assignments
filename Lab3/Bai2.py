import random

# ==========================================
# PHẦN 1: CSP BACKTRACKING (MRV + LCV + FC)
# ==========================================

def is_consistent(var, val, assignment):
    for prev_var, prev_val in assignment.items():
        if prev_val == val or abs(prev_val - val) == abs(prev_var - var):
            return False
    return True

def select_unassigned_variable_mrv(assignment, domains, n):
    """Heuristic MRV: Chọn biến có miền giá trị còn lại nhỏ nhất."""
    unassigned = [v for v in range(n) if v not in assignment]
    return min(unassigned, key=lambda v: len(domains[v]))

def order_domain_values_lcv(var, domains, assignment, n):
    """Heuristic LCV: Ưu tiên giá trị ít loại bỏ lựa chọn của các biến khác nhất."""
    def count_conflicts(val):
        conflicts = 0
        for other_var in range(n):
            if other_var not in assignment and other_var != var:
                for other_val in domains[other_var]:
                    if other_val == val or abs(other_val - val) == abs(other_var - var):
                        conflicts += 1
        return conflicts
    return sorted(domains[var], key=count_conflicts)

def forward_checking(var, val, domains, assignment, n):
    new_domains = {v: list(domains[v]) for v in domains}
    new_domains[var] = [val]
    for other_var in range(n):
        if other_var not in assignment and other_var != var:
            valid_vals = [
                d for d in new_domains[other_var]
                if d != val and abs(d - val) != abs(other_var - var)
            ]
            if not valid_vals:
                return None  # Nhánh cụt (rỗng miền giá trị)
            new_domains[other_var] = valid_vals
    return new_domains

def backtrack(assignment, domains, n):
    if len(assignment) == n:
        return assignment
        
    var = select_unassigned_variable_mrv(assignment, domains, n)
    for val in order_domain_values_lcv(var, domains, assignment, n):
        if is_consistent(var, val, assignment):
            assignment[var] = val
            pruned_domains = forward_checking(var, val, domains, assignment, n)
            if pruned_domains is not None:
                result = backtrack(assignment, pruned_domains, n)
                if result is not None:
                    return result
            del assignment[var]
    return None

def solve_5_queens_csp_backtrack():
    n = 5
    domains = {i: list(range(n)) for i in range(n)}
    res = backtrack({}, domains, n)
    ordered_res = [res[i] for i in range(n)]
    print(f"Nghiệm CSP (Backtracking + MRV + LCV): {ordered_res}")
    return ordered_res


# ==========================================
# PHẦN 2: CHUYỂN CSP SANG SEARCH VÀ GIẢI BẰNG GA
# ==========================================

def fitness(chromosome):
    n = len(chromosome)
    clashes = 0
    for i in range(n):
        for j in range(i + 1, n):
            if chromosome[i] == chromosome[j] or abs(chromosome[i] - chromosome[j]) == abs(i - j):
                clashes += 1
    max_non_attacking = n * (n - 1) // 2
    return max_non_attacking - clashes

def init_population(pop_size, n):
    return [random.sample(range(n), n) for _ in range(pop_size)]

def selection(population, fitnesses):
    tournament = random.sample(list(zip(population, fitnesses)), 3)
    tournament.sort(key=lambda x: x[1], reverse=True)
    return tournament[0][0]

def order_crossover(parent1, parent2):
    n = len(parent1)
    a, b = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[a:b+1] = parent1[a:b+1]
    
    p2_idx = (b + 1) % n
    c_idx = (b + 1) % n
    while -1 in child:
        val = parent2[p2_idx]
        if val not in child:
            child[c_idx] = val
            c_idx = (c_idx + 1) % n
        p2_idx = (p2_idx + 1) % n
    return child

def mutate_swap(chromosome, mutation_rate=0.3):
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

def solve_n_queens_ga(n=5, pop_size=30, max_generations=200, mutation_rate=0.3):
    max_fitness = n * (n - 1) // 2
    pop = init_population(pop_size, n)
    
    for gen in range(max_generations):
        fits = [fitness(ind) for ind in pop]
        best_fit = max(fits)
        best_ind = pop[fits.index(best_fit)]
        
        if best_fit == max_fitness:
            print(f"-> GA tìm thấy lời giải ở thế hệ {gen}!")
            print(f"Cấu hình nghiệm: {best_ind}")
            print_board(best_ind)
            return best_ind
            
        new_pop = [best_ind]
        while len(new_pop) < pop_size:
            p1 = selection(pop, fits)
            p2 = selection(pop, fits)
            child = order_crossover(p1, p2)
            child = mutate_swap(child, mutation_rate)
            new_pop.append(child)
        pop = new_pop
        
    print("GA không tìm thấy nghiệm trong số thế hệ giới hạn.")
    return None


# ==========================================
# HÀM CHẠY CHÍNH
# ==========================================
if __name__ == "__main__":
    print("=== BÀI 2: 5-QUEENS (CSP BACKTRACK VS GA) ===")
    solve_5_queens_csp_backtrack()
    
    print("\nChạy 5-Queens chuyển sang Search giải bằng GA:")
    solve_n_queens_ga(n=5, pop_size=30, max_generations=200, mutation_rate=0.3)